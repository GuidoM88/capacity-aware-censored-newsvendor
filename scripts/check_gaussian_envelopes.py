"""Worst-case overstatement of fractional audits under Gaussian demand.

Part A: equal shares, n = 4, 5, 6, every depth, a grid of floors r, three
covariance structures (any, nonnegative correlations, independent), against
the exact worst case over all laws.
Part B: the shares and floors of the 24 wind audits of
results/illustration/wind_audit.json at depth one, Gaussian worst case (any
and nonnegative correlations) against the observed overstatement and the
worst case over all laws.
Part C: the independent closed form a(1 - sqrt(1 - H_m)),
H_m = sum_{i=2}^m 1/(2i-1), against the computed plateau.

Every reported value is attained by the Gaussian law returned by the SDP
(constraints re-checked with check_gaussian_law); the maximization over the
membership is a grid search with local refinement, so values are lower
bounds on the Gaussian worst case that we expect, but have not proved, to be
tight. Outcomes go to results/gaussian/gaussian_envelopes.json; the summary is
generated from that file.
"""

import json
import time
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from pathlib import Path

import numpy as np

from censored_newsvendor.exact_envelopes import equal_share_exact_value
from censored_newsvendor.gaussian import check_gaussian_law, gaussian_envelope

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/gaussian"
RS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
STRUCTURES = ["any", "nonnegative", "independent"]


def closed_form(n, depth):
    """Theorem G for equal shares; attained (proved) for r <= 1/sqrt(2n-1)."""
    m = n - depth
    H = sum(1 / (2 * i - 1) for i in range(2, m + 1))
    return (1 / n) * (1 - np.sqrt(1 - H)) if H < 1 else None, 1 / np.sqrt(2 * n - 1)


def build_plateau(equal):
    plateau = []
    for n in (4, 5, 6):
        for depth in range(1, n - 1):
            value, r_max = closed_form(n, depth)
            on = [row["value"] for row in equal if row["n"] == n and row["depth"] == depth
                  and row["structure"] in ("independent", "nonnegative") and row["r"] <= r_max]
            above = [(row["r"], row["value"]) for row in equal if row["n"] == n and row["depth"] == depth
                     and row["structure"] == "nonnegative" and row["r"] > r_max]
            plateau.append({"n": n, "depth": depth, "closed_form": value, "r_max": r_max,
                            "computed": on, "nonnegative_above": above})
    return plateau


def one_equal(task):
    n, depth, r, structure = task
    step = 0.1 if n - depth >= 5 else 0.05
    res = gaussian_envelope([1 / n] * n, r, depth=depth, step=step, structure=structure, starts=5)
    row = {"n": n, "depth": depth, "r": r, "structure": structure, "value": res["value"]}
    if res["value"] is not None:
        check = check_gaussian_law(res["G"], [1 / n] * n, r, res["membership"])
        row.update({"valid": bool(check["valid"]), "membership": [round(x, 5) for x in res["membership"]],
                    "variances": [round(float(np.asarray(res["G"])[i, i]), 6) for i in range(n)]})
    return row


def one_wind(task):
    index, shares, r, structure = task
    res = gaussian_envelope(shares, r, depth=1, step=0.05, structure=structure, starts=4,
                            symmetric=False)
    row = {"index": index, "structure": structure, "value": res["value"]}
    if res["value"] is not None:
        row["valid"] = bool(check_gaussian_law(res["G"], shares, r, res["membership"])["valid"])
    return row


def main():
    start = time.time()
    tasks = [(n, depth, r, s) for n in (4, 5, 6) for depth in range(1, n - 1)
             for r in RS for s in STRUCTURES]
    wind = json.loads((ROOT / "results/illustration/wind_audit.json").read_text())["rows"]
    wind_tasks = [(i, row["shares"], row["r"], s) for i, row in enumerate(wind)
                  for s in ("any", "nonnegative")]
    with ProcessPoolExecutor(max_workers=4) as pool:
        equal = list(pool.map(one_equal, tasks))
        gauss_wind = list(pool.map(one_wind, wind_tasks))
    for row in equal:
        row["all_laws"] = float(equal_share_exact_value(row["n"], F(row["r"]).limit_denominator(100),
                                                        row["depth"]))
    wind_rows = []
    for i, row in enumerate(wind):
        g = {r["structure"]: r for r in gauss_wind if r["index"] == i}
        wind_rows.append({"panel": row["panel"], "year": row["year"], "kappa": row["kappa"],
                          "allocation": row["allocation"], "r": row["r"], "observed": row["gap1"],
                          "all_laws": [row["depth1_lower"], row["depth1_upper"]],
                          "gaussian_any": g["any"]["value"], "gaussian_nonnegative": g["nonnegative"]["value"],
                          "valid": bool(g["any"].get("valid", True) and g["nonnegative"].get("valid", True))})
    plateau = build_plateau(equal)
    data = {"date": "2026-11-07", "equal_shares": equal, "wind": wind_rows, "plateau": plateau,
            "seconds": round(time.time() - start, 1)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "gaussian_envelopes.json").write_text(json.dumps(data, indent=1) + "\n")
    summary(json.loads((OUT / "gaussian_envelopes.json").read_text()))
    print("done in", data["seconds"], "s")


def fmt(x):
    return "infeasible" if x is None else f"{x:.4f}"


def summary(data):
    lines = ["# Fractional audits under Gaussian demand", "",
             f"{data['date']}. Generated by `scripts/check_gaussian_envelopes.py` from "
             "[gaussian_envelopes.json](gaussian_envelopes.json). Gaussian costs are Euclidean norms "
             "sqrt(x'Gx); for a fixed membership the least favourable covariance is an SDP, solved to "
             "optimality, and the membership is searched on a grid with local refinement. Values are "
             "attained by the returned laws (all constraints re-checked) and are lower bounds on the "
             "Gaussian worst case. They do not depend on the penalty ratio.", "",
             "## Equal shares", "",
             "| n | depth | r | all laws (exact) | Gaussian | nonnegative correlations | independent |",
             "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    rows = data["equal_shares"]
    keys = sorted({(r["n"], r["depth"], r["r"]) for r in rows})
    for n, depth, r in keys:
        cell = {row["structure"]: row for row in rows if (row["n"], row["depth"], row["r"]) == (n, depth, r)}
        lines.append(f"| {n} | {depth} | {r} | {cell['any']['all_laws']:.4f} | {fmt(cell['any']['value'])} | "
                     f"{fmt(cell['nonnegative']['value'])} | {fmt(cell['independent']['value'])} |")
    invalid = [row for row in rows if row.get("valid") is False]
    lines += ["", f"Laws failing the constraint re-check: {len(invalid)}.", "",
              "## Theorem G for equal shares", "",
              "Upper bound a(1 - sqrt(1 - H_m)), H_m = 1/3 + 1/5 + ... + 1/(2m-1), for every r under "
              "nonnegative correlations; proved to be attained for r <= 1/sqrt(2n-1). Computed values "
              "(independent and nonnegative structures) on that range, and the nonnegative worst case above it.", "",
              "| n | depth | m | closed form | proved for r up to | computed on that range | nonnegative above it (r: value) |",
              "| ---: | ---: | ---: | ---: | ---: | --- | --- |"]
    for p in data["plateau"]:
        vals = ", ".join(f"{v:.6f}" for v in p["computed"] if v is not None) or "-"
        above = ", ".join(f"{r}: {fmt(v)}" for r, v in p["nonnegative_above"])
        lines.append(f"| {p['n']} | {p['depth']} | {p['n'] - p['depth']} | {fmt(p['closed_form'])} | "
                     f"{p['r_max']:.3f} | {vals} | {above} |")
    lines += ["", "## The wind audits (depth one)", "",
              "| panel | year | kappa | allocation | r | observed | all laws | Gaussian | nonnegative correlations |",
              "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |"]
    for w in data["wind"]:
        lo, hi = w["all_laws"]
        lines.append(f"| {w['panel']} | {w['year']} | {w['kappa']} | {w['allocation']} | {w['r']:.3f} | "
                     f"{w['observed']:.4f} | {lo:.4f}-{hi:.4f} | {fmt(w['gaussian_any'])} | "
                     f"{fmt(w['gaussian_nonnegative'])} |")
    lines.append("")
    (OUT / "gaussian_envelopes.md").write_text("\n".join(lines))


if __name__ == "__main__":
    import sys
    if "--summary-only" in sys.argv:
        path = OUT / "gaussian_envelopes.json"
        saved = json.loads(path.read_text())
        saved["plateau"] = build_plateau(saved["equal_shares"])
        path.write_text(json.dumps(saved, indent=1) + "\n")
        summary(saved)
    else:
        main()
