"""Conjecture C is false: a three-level law beats every two-block law at kappa = 10.

Part 1 verifies the counterexample in exact arithmetic: four producers with
shares (1, 24, 24, 1)/50, depth one, r = 33/50, kappa = 10. An LP over
kappa-segment laws (with a safety margin, then rationalized) gives segments
whose costs are checked on every coalition (caps, strict stability, grand
cost, segment ratios) and turned into an explicit finite law whose pinball
costs are evaluated directly. Its excess is compared with the best
two-block value max_{K, I} Psi_kappa(a(I), A_J) and with the certificate bound.

Part 2 measures how often this happens on random four-producer instances
with uneven shares (one share drawn small): for each, the certificate bound,
the two-block value and the best segment law found (LP at the certificate's
maximizer plus a short local search over the membership).

Outcomes go to results/asymmetric/conjecture_c.json; the summary is
generated from that file.
"""

import itertools
import json
import random
import time
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from censored_newsvendor.asymmetric import (_vec, asymmetric_best_block,
                                            asymmetric_zonotope_minimal_cost, level_for_ratio,
                                            pinball_cost, segment_cost, three_point_law,
                                            verify_segments)
from censored_newsvendor.certificates import certificate_bound

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/asymmetric"


def best_segment_law(shares, r, kappa, depth, start, margin=0.0, iterations=120):
    """Local search over the free coordinates of the membership; returns (value, z, segments)."""
    a = np.asarray(shares, dtype=float)
    free = [i for i in range(len(a)) if 1e-9 < start[i] < 1 - 1e-9]

    def solve(point):
        found = asymmetric_zonotope_minimal_cost(point, a, r * (1 + margin), kappa,
                                                 integer_excess=-margin, grand_cost=1 - margin)
        if found["value"] is None:
            return -np.inf, found
        return float(a @ point) - found["value"], found

    def objective(s):
        point = np.array(start, dtype=float)
        point[free] = np.clip(s, 0, 1)
        return -solve(point)[0]

    point = np.array(start, dtype=float)
    if free:
        result = minimize(objective, point[free], method="Nelder-Mead",
                          options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": iterations})
        candidate = point.copy()
        candidate[free] = np.clip(result.x, 0, 1)
        if solve(candidate)[0] > solve(point)[0]:
            point = candidate
    value, found = solve(point)
    return value, point, found["segments"]


def part_one():
    shares = [F(1, 50), F(24, 50), F(24, 50), F(1, 50)]
    r, kappa = F(33, 50), F(10)
    floats = [float(x) for x in shares]
    bound, z_cert = certificate_bound(floats, float(r), 1, kappa=float(kappa))
    _, point, segments = best_segment_law(floats, float(r), float(kappa), 1,
                                          [1.0, 0.41, 0.10, 0.0], margin=1e-6, iterations=300)
    z = tuple(F(float(x)).limit_denominator(10**6) for x in point)
    exact = []
    for d, alpha, beta in segments:
        al, be = F(float(alpha)).limit_denominator(10**12), F(float(beta)).limit_denominator(10**12)
        exact.append((tuple(F(float(x)).limit_denominator(10**11) for x in d),
                      min(al, kappa * be), min(be, kappa * al)))
    value = sum(x * y for x, y in zip(shares, z)) - segment_cost(exact, z)
    check = verify_segments(exact, shares, r, kappa, z, value)
    tau = level_for_ratio(kappa)
    states, probabilities, scale = three_point_law(exact, tau)
    vectors = [_vec(4, {j: 1 for j in s}) for size in range(1, 5)
               for s in itertools.combinations(range(4), size)] + [z]
    law_ok = all(pinball_cost(states, probabilities, x, tau) == scale * segment_cost(exact, x)
                 for x in vectors)
    block = asymmetric_best_block(shares, r, 1, kappa)
    return {"shares": [str(x) for x in shares], "r": str(r), "kappa": str(kappa), "depth": 1,
            "membership": [str(x) for x in z], "value": str(value), "value_float": float(value),
            "slacks": {k: float(v) for k, v in check.items()},
            "all_constraints_exact": all(v >= 0 for v in check.values()),
            "explicit_law_atoms": len(states), "explicit_law_matches": law_ok,
            "two_block_value": float(block["value"]), "two_block_regime": block["regime"],
            "certificate_bound": float(bound), "certificate_membership": [round(float(x), 6) for x in z_cert]}


def one(seed):
    rng = random.Random(seed)
    raw = [rng.randint(1, 3)] + [rng.randint(5, 40) for _ in range(3)]
    rng.shuffle(raw)
    shares = [F(x, sum(raw)) for x in raw]
    r = F(rng.randint(10, 45), 50)
    kappa = rng.choice([F(2), F(3), F(10)])
    floats = [float(x) for x in shares]
    block = float(asymmetric_best_block(shares, r, 1, kappa)["value"])
    bound, z = certificate_bound(floats, float(r), 1, kappa=float(kappa))
    row = {"seed": seed, "shares": [str(x) for x in shares], "r": str(r), "kappa": str(kappa),
           "two_block": block, "certificate": float(bound),
           "pinned": bool(abs(bound - block) < 1e-7)}
    if not row["pinned"]:
        law, point, _ = best_segment_law(floats, float(r), float(kappa), 1, z)
        row.update({"best_law": float(law), "membership": [round(float(x), 6) for x in point],
                    "law_beats_two_block": bool(law > block + 1e-7)})
    return row


def main():
    start = time.time()
    data = {"date": "2026-11-07", "counterexample": part_one()}
    with ProcessPoolExecutor(max_workers=4) as pool:
        data["sample"] = list(pool.map(one, range(9000, 9200)))
    data["seconds"] = round(time.time() - start, 1)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "conjecture_c.json").write_text(json.dumps(data, indent=1, default=lambda o: o.item()) + "\n")
    saved = json.loads((OUT / "conjecture_c.json").read_text())
    c, rows = saved["counterexample"], saved["sample"]
    beaten = [r for r in rows if r.get("law_beats_two_block")]
    lines = ["# Conjecture C is false", "",
             f"{saved['date']}. Generated by `scripts/refute_conjecture_c.py` from "
             "[conjecture_c.json](conjecture_c.json).", "",
             "## The counterexample", "",
             f"Shares {', '.join(c['shares'])}, depth {c['depth']}, r = {c['r']}, kappa = {c['kappa']}.", "",
             f"- Explicit law ({c['explicit_law_atoms']} atoms, exact rational arithmetic, pinball loss "
             f"evaluated directly): pinball costs equal the segment costs on every coalition: "
             f"{c['explicit_law_matches']}; all constraints hold exactly: {c['all_constraints_exact']} "
             f"(minimal slacks: cap {c['slacks']['cap']:.2e}, stability {c['slacks']['stability']:.2e}, "
             f"grand {c['slacks']['grand']:.3f}).",
             f"- Membership z = ({', '.join(c['membership'])}), excess **{c['value_float']:.6f}**.",
             f"- Best two-block value: {c['two_block_value']:.6f} ({c['two_block_regime']} regime).",
             f"- Certificate bound: {c['certificate_bound']:.6f}. The true worst case of this instance lies "
             f"between {c['value_float']:.4f} and {c['certificate_bound']:.4f}.", "",
             "## How often (random four-producer instances with one small share)", "",
             f"{len(rows)} instances, depth one, one share drawn from 1..3 and three from 5..40, "
             "r = k/50 in [0.2, 0.9], kappa in {2, 3, 10}.", "",
             "| kappa | instances | two-block = certificate | certificate above two-block | "
             "of these, an explicit law beats two-block | largest excess over two-block |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for kappa in ("2", "3", "10"):
        group = [r for r in rows if r["kappa"] == kappa]
        above = [r for r in group if not r["pinned"]]
        wins = [r for r in above if r.get("law_beats_two_block")]
        largest = max((r["best_law"] - r["two_block"] for r in wins), default=0.0)
        lines.append(f"| {kappa} | {len(group)} | {len(group) - len(above)} | {len(above)} | "
                     f"{len(wins)} | {largest:.4f} |")
    lines += ["", f"In total an explicit law beats the two-block value in {len(beaten)} of {len(rows)} "
              "instances.", ""]
    (OUT / "conjecture_c.md").write_text("\n".join(lines))
    print(f"done in {data['seconds']} s; counterexample exact: {c['all_constraints_exact']}, "
          f"law matches: {c['explicit_law_matches']}; beaten in sample: {len(beaten)}")


if __name__ == "__main__":
    main()
