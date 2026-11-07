"""Checks for asymmetric imbalance penalties (docs/asymmetric_penalties.md).

A. Last depth, arbitrary shares: the closed form for every penalty ratio,
   its explicit law (exact arithmetic, pinball loss evaluated directly) and
   the certificate LP as an independent upper bound.
B. Equal shares, every depth: the ceiling and high families, exact
   verification of every construction and of explicit laws on a subsample;
   with kappa = 1 the values must coincide with Theorem 1.
C. Certificate LP against the closed form outside the windows.
D. The windows that survive for 1 < kappa < 2(m-1)/m: certificate bound,
   exact relaxation at its maximizer and the best explicit law found.
E. Window lengths as a function of kappa.

Outcomes are written to results/asymmetric/asymmetric_checks.json first;
the markdown summary is generated from that file.
"""

import itertools
import json
import random
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from censored_newsvendor.asymmetric import (
    _vec, asymmetric_equal_share_construction, asymmetric_equal_share_value,
    asymmetric_high_threshold, asymmetric_high_value, asymmetric_last_depth_construction,
    asymmetric_windows, asymmetric_zonotope_minimal_cost, level_for_ratio, pinball_cost,
    segment_cost, three_point_law, verify_segments)
from censored_newsvendor.certificates import certificate_bound
from censored_newsvendor.exact_envelopes import equal_share_value, last_depth_value
from censored_newsvendor.seminorm_envelope import minimal_cost

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/asymmetric"
KAPPAS = [F(1), F(6, 5), F(4, 3), F(3, 2), F(2), F(3), F(10)]


def law_matches(segments, n, membership, kappa):
    """Pinball cost of the explicit law equals scale * segment cost on every coalition."""
    tau = level_for_ratio(kappa)
    states, probabilities, scale = three_point_law(segments, tau)
    vectors = [_vec(n, {j: 1 for j in s}) for size in range(1, n + 1)
               for s in itertools.combinations(range(n), size)] + [membership]
    return all(pinball_cost(states, probabilities, x, tau) == scale * segment_cost(segments, x)
               for x in vectors), len(states)


def slacks_ok(check):
    return all(v >= 0 for v in check.values()) and check["witness"] == 0


def part_a(count=300, seed=7):
    rng = random.Random(seed)
    rows = []
    for _ in range(count):
        n = rng.choice([3, 4, 5])
        raw = [rng.randint(1, 15) for _ in range(n)]
        shares = [F(x, sum(raw)) for x in raw]
        r = F(rng.randint(1, 19), 20)
        kappa = rng.choice(KAPPAS)
        con = asymmetric_last_depth_construction(shares, r, kappa)
        check = verify_segments(con["segments"], shares, r, kappa, con["membership"], con["value"])
        bound, _ = certificate_bound([float(x) for x in shares], float(r), n - 2, kappa=float(kappa))
        law_ok, atoms = law_matches(con["segments"], n, con["membership"], kappa)
        rows.append({
            "n": n, "shares": [str(x) for x in shares], "r": str(r), "kappa": str(kappa),
            "regime": con["regime"], "value": str(con["value"]), "value_float": float(con["value"]),
            "exact_ok": slacks_ok(check), "certificate": bound,
            "certificate_matches": abs(bound - float(con["value"])) < 1e-9,
            "law_ok": law_ok, "law_atoms": atoms,
            "symmetric_value_ok": (kappa != 1 or con["value"] == last_depth_value(shares, r)),
        })
    return rows


def part_b():
    rows = []
    for n in range(3, 9):
        for depth in range(1, n - 1):
            for kappa in KAPPAS:
                for k in range(1, 40):
                    r = F(k, 40)
                    value = asymmetric_equal_share_value(n, r, depth, kappa)
                    row = {"n": n, "depth": depth, "kappa": str(kappa), "r": str(r),
                           "value": None if value is None else str(value)}
                    if kappa == 1:
                        row["matches_theorem_1"] = value == equal_share_value(n, r, depth)
                    con = asymmetric_equal_share_construction(n, r, depth, kappa)
                    if value is None:
                        row["window"] = True
                        row["construction"] = con is not None
                        rows.append(row)
                        continue
                    check = verify_segments(con["segments"], [F(1, n)] * n, r, kappa,
                                            con["membership"], value)
                    row.update({"window": False, "family": con["family"], "p": con["p"],
                                "exact_ok": slacks_ok(check) and con["value"] == value})
                    if n <= 6 and k % 2 == 0:
                        row["law_ok"], row["law_atoms"] = law_matches(
                            con["segments"], n, con["membership"], kappa)
                    rows.append(row)
    return rows


def part_c():
    rows = []
    cases = [(4, 1), (4, 2), (5, 1), (5, 2), (5, 3), (6, 2), (6, 3), (6, 4)]
    for (n, depth), kappa, r in itertools.product(cases, [F(3, 2), F(2), F(3), F(10)],
                                                  [F(k, 10) for k in range(1, 10)]):
        value = asymmetric_equal_share_value(n, r, depth, kappa)
        if value is None:
            continue
        bound, _ = certificate_bound([1 / n] * n, float(r), depth, kappa=float(kappa))
        rows.append({"n": n, "depth": depth, "kappa": str(kappa), "r": str(r),
                     "value": float(value), "certificate": bound,
                     "matches": abs(bound - float(value)) < 1e-9})
    return rows


def best_law_near(z, shares, r, kappa, iterations=150):
    """Best explicit asymmetric-zonotope law at z and after a local search in z."""
    def gap(point):
        found = asymmetric_zonotope_minimal_cost(point, shares, r, kappa)
        return -np.inf if found["value"] is None else float(np.dot(shares, point)) - found["value"]

    start = gap(z)
    free = [i for i in range(len(z)) if 1e-12 < z[i] < 1 - 1e-12]
    if not free:
        return start, start

    def objective(s):
        point = z.copy()
        point[free] = np.clip(s, 0, 1)
        return -gap(point)

    result = minimize(objective, z[free], method="Nelder-Mead",
                      options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": iterations})
    return start, max(start, -result.fun)


def part_d():
    rows = []
    n, depth = 4, 1
    m = n - depth
    for kappa in [F(11, 10), F(6, 5), F(13, 10)]:
        for lo, hi in asymmetric_windows(n, depth, kappa):
            for frac in (F(1, 4), F(1, 2), F(3, 4)):
                r = lo + frac * (hi - lo)
                shares = [1 / n] * n
                bound, z = certificate_bound(shares, float(r), depth, kappa=float(kappa))
                relaxed, _ = minimal_cost(z, shares, float(r), kappa=float(kappa))
                at_z, searched = best_law_near(z, shares, float(r), float(kappa))
                rows.append({
                    "n": n, "depth": depth, "kappa": str(kappa), "r": float(r),
                    "window": [float(lo), float(hi)], "certificate": bound,
                    "relaxation_at_maximizer": float(np.dot(shares, z)) - relaxed,
                    "law_at_maximizer": at_z, "best_law_found": searched,
                    "ceiling": float((1 - r) * m / n),
                    "h2": float(asymmetric_high_value(n, r, depth, kappa, p=2)),
                    "membership": [round(float(x), 6) for x in z]})
    return rows


def part_e():
    rows = []
    for m in range(3, 11):
        for kappa in [F(1), F(11, 10), F(5, 4), F(3, 2), F(7, 4), F(2)]:
            gaps = asymmetric_windows(m + 1, 1, kappa)
            rows.append({"m": m, "kappa": str(kappa), "closing_ratio": str(F(2 * (m - 1), m)),
                         "windows": [[str(lo), str(hi)] for lo, hi in gaps],
                         "total_length": float(sum(hi - lo for lo, hi in gaps)),
                         "high_threshold": str(asymmetric_high_threshold(m + 1, 1, kappa))})
    return rows


def summary(data):
    a, b, c, d, e = (data[k] for k in ("last_depth", "equal_shares", "certificate_crosscheck",
                                       "windows_probe", "window_lengths"))
    regimes = {}
    for row in a:
        regimes[row["regime"]] = regimes.get(row["regime"], 0) + 1
    built = [row for row in b if not row["window"]]
    laws = [row for row in built if "law_ok" in row]
    sym = [row for row in b if "matches_theorem_1" in row]
    lines = [
        "# Asymmetric imbalance penalties: checks", "",
        f"{data['date']}. Generated by `scripts/check_asymmetric_penalties.py` from "
        "[asymmetric_checks.json](asymmetric_checks.json). Theory: "
        "[docs/asymmetric_penalties.md](../../docs/asymmetric_penalties.md).", "",
        "## A. Last depth, arbitrary shares", "",
        f"- Random instances: {len(a)} (n = 3, 4, 5; r = k/20; kappa in "
        f"{{{', '.join(str(k) for k in KAPPAS)}}}). Regimes: "
        + ", ".join(f"{k} {v}" for k, v in sorted(regimes.items())) + ".",
        f"- Construction verified in exact arithmetic: {sum(r['exact_ok'] for r in a)} / {len(a)}.",
        f"- Explicit three-point law reproduces every coalition cost and the witness under "
        f"pinball loss: {sum(r['law_ok'] for r in a)} / {len(a)}.",
        f"- Certificate LP equals the closed form (1e-9): "
        f"{sum(r['certificate_matches'] for r in a)} / {len(a)}.",
        f"- kappa = 1 instances equal Theorem 2: {sum(r['symmetric_value_ok'] for r in a)} / {len(a)}.", "",
        "## B. Equal shares, every depth", "",
        f"- Grid: n = 3..8, every depth, the seven ratios above, r = k/40: {len(b)} points, "
        f"{len(b) - len(built)} inside windows, {len(built)} with a closed form.",
        f"- Constructions verified in exact arithmetic: {sum(r['exact_ok'] for r in built)} / {len(built)}"
        f" (ceiling family {sum(r['family'] == 'ceiling' for r in built)}, high family "
        f"{sum(r['family'] == 'high' for r in built)}).",
        f"- Explicit laws checked (n <= 6, r = k/20): {sum(r['law_ok'] for r in laws)} / {len(laws)}.",
        f"- kappa = 1 values equal Theorem 1 (windows included): "
        f"{sum(r['matches_theorem_1'] for r in sym)} / {len(sym)}.",
        f"- Window points without a construction, as expected: "
        f"{sum(not r['construction'] for r in b if r['window'])} / {len(b) - len(built)}.", "",
        "## C. Certificate LP outside the windows", "",
        f"- {sum(r['matches'] for r in c)} / {len(c)} cases equal the closed form to 1e-9 "
        "(n = 4, 5, 6; kappa = 3/2, 2, 3, 10; r = 0.1..0.9).", "",
        "## D. Inside the surviving windows (n = 4, depth 1)", "",
        "The certificate bound coincides with the exact relaxation at its maximizer, so it is the "
        "value of the relaxation there. The best explicit law found (asymmetric zonotopes, local "
        "search in z) stays below it: the windows are the one place where the answer is open.", "",
        "| kappa | r | certificate | relaxation at maximizer | best law found | difference | H_2 (law) | ceiling |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in d:
        lines.append(f"| {row['kappa']} | {row['r']:.4f} | {row['certificate']:.6f} | "
                     f"{row['relaxation_at_maximizer']:.6f} | {row['best_law_found']:.6f} | "
                     f"{row['certificate'] - row['best_law_found']:.1e} | {row['h2']:.6f} | "
                     f"{row['ceiling']:.6f} |")
    lines += ["", "## E. Total window length at depth one", "",
              "| m | closing ratio 2(m-1)/m | " + " | ".join(
                  f"kappa = {k}" for k in ["1", "11/10", "5/4", "3/2", "7/4", "2"]) + " |",
              "| --- | --- |" + " ---: |" * 6]
    for m in sorted({row["m"] for row in e}):
        cells = [row for row in e if row["m"] == m]
        lines.append(f"| {m} | {cells[0]['closing_ratio']} | "
                     + " | ".join(f"{row['total_length']:.4f}" for row in cells) + " |")
    lines.append("")
    return "\n".join(lines)


def main():
    start = time.time()
    data = {"date": "2026-11-07", "kappas": [str(k) for k in KAPPAS]}
    data["last_depth"] = part_a()
    data["equal_shares"] = part_b()
    data["certificate_crosscheck"] = part_c()
    data["windows_probe"] = part_d()
    data["window_lengths"] = part_e()
    data["seconds"] = round(time.time() - start, 1)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "asymmetric_checks.json").write_text(json.dumps(data, separators=(",", ":")) + "\n")
    saved = json.loads((OUT / "asymmetric_checks.json").read_text())
    (OUT / "asymmetric_checks.md").write_text(summary(saved))
    failures = (
        [r for r in saved["last_depth"] if not (r["exact_ok"] and r["law_ok"] and r["certificate_matches"]
                                                and r["symmetric_value_ok"])]
        + [r for r in saved["equal_shares"] if not r["window"] and not r["exact_ok"]]
        + [r for r in saved["equal_shares"] if r.get("law_ok") is False]
        + [r for r in saved["equal_shares"] if r.get("matches_theorem_1") is False]
        + [r for r in saved["certificate_crosscheck"] if not r["matches"]])
    print(f"done in {data['seconds']} s; failures: {len(failures)}")
    return failures


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
