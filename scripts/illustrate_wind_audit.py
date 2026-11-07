"""How much does a fractional audit overstate on real wind data?

Four producers per panel (NREL WIND Toolkit sites in Texas, modeled, 2007 and
2008; the four ENGIE La Haute Borne turbines, measured, 2014 and 2015; four
distant WIND Toolkit sites in Texas, Iowa, Wyoming and New York, modeled, 2007
and 2008, configs/illustration_wind_sites.json), hourly
production, one calendar year each. The empirical joint law of the year
defines the coalition costs c(x) = min_q E l(x'Y - q), with absolute loss
(kappa = 1) or pinball loss with kappa = 2. Two allocations of the optimal grand
cost L = c(1) are audited:
  proportional: charges proportional to standalone costs, so that every
                producer pays the same fraction r = c(1)/sum_j c(e_j);
  gradient:     a_j proportional to E[Y_j g(S)], with g the derivative of the
                loss at the optimal grand offer (Aumann-Shapley/Euler).
For each, the integer excess B and the fractional excess D_k at depths one
and two are computed exactly (one LP per face over all hours), and the
overstatement (D_k - B)/L is compared with the worst case for the same
shares and the same floor r: exact at depth two (Theorems 2 and A), between
the best explicit family and the certificate bound at depth one.

Data are downloaded once and verified against the checksums in
configs/residual_wind_sources.json. Outcomes go to
results/illustration/wind_audit.json; the summary is generated from it.
"""

import argparse
import importlib.util
import itertools
import json
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.optimize import linprog

from censored_newsvendor.asymmetric import asymmetric_best_block, asymmetric_last_depth_value
from censored_newsvendor.certificates import certificate_bound
from censored_newsvendor.exact_envelopes import best_general_construction, last_depth_value

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/illustration"


def loaders():
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("wind", ROOT / "scripts/check_wind_residuals.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def loss_weights(kappa):
    """(surplus slope, shortfall slope) of the loss, normalized to sum one."""
    tau = 1 / (1 + kappa)
    return tau, 1 - tau


def cost(values, kappa):
    """min_q mean l(v - q) for the empirical law of the values."""
    up, down = loss_weights(kappa)
    q = np.quantile(values, up, method="inverted_cdf")
    u = values - q
    return float(np.mean(np.where(u > 0, up * u, -down * u)))


def fractional_excess(Y, charges, free, kappa):
    """max over z in [0,1]^free (zero elsewhere) of a'z - c(z), as one LP."""
    up, down = loss_weights(kappa)
    T, m = len(Y), len(free)
    X = Y[:, free]
    # variables: z (m), q (1), u (T); maximize a'z - mean(u)
    c = np.r_[-charges[free], 0.0, np.full(T, 1.0 / T)]
    # u_t >= up (x_t'z - q)  ->  up x_t'z - up q - u_t <= 0
    # u_t >= -down (x_t'z - q) -> -down x_t'z + down q - u_t <= 0
    eye = -sparse.identity(T, format="csr")
    ones = np.ones((T, 1))
    A = sparse.vstack([sparse.hstack([sparse.csr_matrix(up * X), sparse.csr_matrix(-up * ones), eye]),
                       sparse.hstack([sparse.csr_matrix(-down * X), sparse.csr_matrix(down * ones), eye])],
                      format="csr")
    result = linprog(c, A_ub=A, b_ub=np.zeros(2 * T),
                     bounds=[(0, 1)] * m + [(None, None)] + [(0, None)] * T, method="highs")
    if result.status != 0:
        raise RuntimeError(result.message)
    z = np.zeros(Y.shape[1])
    z[free] = result.x[:m]
    return float(-result.fun), z


def audit(Y, charges, kappa):
    n = Y.shape[1]
    L = cost(Y.sum(axis=1), kappa)
    standalone = np.array([cost(Y[:, j], kappa) for j in range(n)])
    r = float(min(charges / standalone))
    B = max(0.0, max(charges[list(s)].sum() - cost(Y[:, list(s)].sum(axis=1), kappa)
                     for size in range(1, n) for s in itertools.combinations(range(n), size)))
    out = {"L": L, "r": r, "B_over_L": B / L, "shares": (charges / L).tolist()}
    for depth in (1, 2):
        best, arg = -np.inf, None
        for excluded in itertools.combinations(range(n), depth):
            free = [j for j in range(n) if j not in excluded]
            value, z = fractional_excess(Y, charges, free, kappa)
            if value > best:
                best, arg = value, z
        out[f"D{depth}_over_L"] = best / L
        out[f"gap{depth}"] = max(0.0, best - B) / L
        out[f"membership{depth}"] = [round(float(x), 4) for x in arg]
    return out


def worst_cases(shares, r, kappa):
    w = [F(x).limit_denominator(10**6) for x in shares]
    w = [x / sum(w) for x in w]
    rq = F(r).limit_denominator(10**6)
    floats = [float(x) for x in w]
    upper1, _ = certificate_bound(floats, float(rq), 1, kappa=float(kappa))
    if kappa == 1:
        last = float(last_depth_value(w, rq))
        lower1 = float(best_general_construction(w, rq, 1)["value"])
    else:
        last = float(asymmetric_last_depth_value(w, rq, kappa))
        lower1 = float(asymmetric_best_block(w, rq, 1, kappa)["value"])
    ceiling1 = (1 - float(rq)) * (1 - min(floats))
    return {"depth1_lower": lower1, "depth1_upper": float(upper1), "depth1_ceiling": ceiling1,
            "depth2_exact": last}


def allocations(Y, kappa):
    n = Y.shape[1]
    L = cost(Y.sum(axis=1), kappa)
    standalone = np.array([cost(Y[:, j], kappa) for j in range(n)])
    proportional = standalone * L / standalone.sum()
    up, down = loss_weights(kappa)
    S = Y.sum(axis=1)
    q = np.quantile(S, up, method="inverted_cdf")
    slope = np.where(S > q, up, np.where(S < q, -down, 0.0))
    gradient = (Y * slope[:, None]).mean(axis=0)
    gradient = gradient * L / gradient.sum()
    return {"proportional": proportional, "gradient": gradient}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path,
                        default=Path(tempfile.gettempdir()) / "censored_newsvendor_wind_cache")
    args = parser.parse_args()
    wind = loaders()
    sources = json.loads((ROOT / "configs/residual_wind_sources.json").read_text())
    distant = json.loads((ROOT / "configs/illustration_wind_sites.json").read_text())
    panels = {"Texas (modeled)": wind.texas(args.cache, sources),
              "France (measured)": wind.france(args.cache, sources),
              "Four states (modeled)": wind.texas(args.cache, {"texas_sites": distant["sites"]})}
    rows = []
    for name, (times, panel, rated, provenance) in panels.items():
        years = times.astype("datetime64[Y]").astype(int) + 1970
        for year in sorted(set(years.tolist())):
            Y = panel[years == year]
            for kappa in (1, 2):
                for rule, charges in allocations(Y, kappa).items():
                    result = audit(Y, charges, kappa)
                    result.update(worst_cases(result["shares"], result["r"], kappa))
                    result.update({"panel": name, "year": year, "hours": int(len(Y)),
                                   "kappa": kappa, "allocation": rule})
                    rows.append(result)
                    print(name, year, kappa, rule, round(result["r"], 3),
                          round(result["gap1"], 4), round(result["depth1_upper"], 4),
                          round(result["gap2"], 4), round(result["depth2_exact"], 4), flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    data = {"date": "2026-11-07", "rows": rows,
            "provenance": {k: v[3] for k, v in panels.items()}}
    (OUT / "wind_audit.json").write_text(json.dumps(data, indent=1, default=str) + "\n")
    saved = json.loads((OUT / "wind_audit.json").read_text())["rows"]
    lines = ["# Fractional audits on real wind data", "",
             "2026-11-07. Generated by `scripts/illustrate_wind_audit.py` from "
             "[wind_audit.json](wind_audit.json). Hourly production of four producers per panel, "
             "one calendar year per row; costs from the empirical joint law; L = c(1). "
             "Overstatement = (D_k - B)/L. Worst case: same shares and the same floor r "
             "(depth one: best explicit family to certificate bound; depth two: exact).", "",
             "| panel | year | kappa | allocation | r | B/L | depth 1: observed | depth 1: worst case | "
             "depth 2: observed | depth 2: worst case |",
             "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in saved:
        worst1 = (f"{r['depth1_lower']:.3f}" if abs(r['depth1_upper'] - r['depth1_lower']) < 5e-4
                  else f"{r['depth1_lower']:.3f}-{r['depth1_upper']:.3f}")
        lines.append(f"| {r['panel']} | {r['year']} | {r['kappa']} | {r['allocation']} | {r['r']:.3f} | "
                     f"{r['B_over_L']:.3f} | {r['gap1']:.3f} | {worst1} | {r['gap2']:.3f} | "
                     f"{r['depth2_exact']:.3f} |")
    lines.append("")
    (OUT / "wind_audit.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
