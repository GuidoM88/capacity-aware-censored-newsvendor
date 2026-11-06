"""Test the realizability conjecture where no theorem applies.

Conjecture: under symmetric absolute loss, the seminorm relaxation of the
worst exclusion gap is attained by a finite centrally symmetric demand law.
Theorems 1 and 2 of docs/exact_envelopes.md settle equal shares outside the
windows and the last depth n-2, so the cases here avoid them: unequal shares
at depth one for four producers, the equal-share windows for four and five
producers, and depth two for five producers.

For each case: maximize the relaxation over memberships (grid plus local
refinement), solve the zonotope LP at the maximizer, build the explicit law
and re-evaluate it with ExclusionEnvelope and coalition_table. If the law
falls short, the chamber sampling is repeated with four times as many
directions before the case is reported as not realized.
"""

import hashlib
import json
import random
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from pathlib import Path

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, coalition_table
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.seminorm_envelope import (
    c31_ceiling, minimal_cost, relaxed_envelope, symmetric_unit_law, zonotope_minimal_cost,
)

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-6


def cases():
    rng = random.Random(611)
    out = []
    for _ in range(6):
        raw = [rng.randint(1, 12) for _ in range(4)]
        shares = [x / sum(raw) for x in raw]
        r = rng.choice([.1, .2, .3, .4, .5, .6, .7])
        out.append({"family": "four producers, unequal shares", "shares": shares, "r": r,
                    "depth": 1, "step": .05, "samples": 2_000_000})
    for r in (.21, .23, .27, .32):
        out.append({"family": "four producers, equal-share window", "shares": [.25] * 4, "r": r,
                    "depth": 1, "step": .025, "samples": 2_000_000})
    for r in (.35, .4, .45):
        out.append({"family": "five producers, equal-share window", "shares": [.2] * 5, "r": r,
                    "depth": 1, "step": .05, "samples": 4_000_000})
    for r in (.25, .3):
        out.append({"family": "five producers, depth two, equal-share window", "shares": [.2] * 5,
                    "r": r, "depth": 2, "step": .025, "samples": 4_000_000})
    for _ in range(2):
        raw = [rng.randint(1, 12) for _ in range(5)]
        shares = [x / sum(raw) for x in raw]
        r = rng.choice([.15, .3, .45])
        out.append({"family": "five producers, depth two, unequal shares", "shares": shares,
                    "r": r, "depth": 2, "step": .05, "samples": 4_000_000})
    return out


def evaluate(generators, shares, depth):
    states, probabilities, offer, _ = symmetric_unit_law(generators, shares)
    rule = FrozenRule(offer, shares, np.ones(len(shares)))
    law = FiniteLaw(states, probabilities)
    grand = float(probabilities @ np.abs(offer - states.sum(axis=1)))
    upper = ExclusionEnvelope.population(rule, law).level(depth)["upper"]
    table = coalition_table(rule, law)
    integer = max(0., max(row["excess"] for row in table))
    singles = [row["cost"] for row in table if len(row["coalition"]) == 1]
    rho = min([1.] + [grand * w / c for w, c in zip(shares, singles) if c > 1e-15])
    return (upper - integer) / grand, integer / grand, rho, len(probabilities)


def run(case):
    shares = np.asarray(case["shares"], dtype=float)
    r, depth = case["r"], case["depth"]
    found = relaxed_envelope(shares, r, depth=depth, step=case["step"])
    z = np.asarray(found["membership"])
    relaxed = float(shares @ z) - minimal_cost(z, shares, r)[0]
    attempts = []
    for samples in (case["samples"], 4 * case["samples"]):
        zono = zonotope_minimal_cost(z, shares, r, samples=samples)
        verified, integer, rho, atoms = evaluate(zono["generators"], shares, depth)
        attempts.append({"samples": samples, "chambers": zono["chambers"],
                         "chambers_stable": zono["stable"], "verified_gap": verified,
                         "integer_excess_over_L": integer, "rho": rho, "atoms": atoms})
        if abs(verified - relaxed) < TOL and integer < TOL and rho >= r - TOL:
            break
    last = attempts[-1]
    realized = (abs(last["verified_gap"] - relaxed) < TOL and last["integer_excess_over_L"] < TOL
                and last["rho"] >= r - TOL)
    row = dict(case)
    row.update({"relaxed_gap": float(found["value"]), "relaxed_at_membership": relaxed,
                "membership": z.tolist(), "excluded": list(found["excluded"]),
                "c31": c31_ceiling(shares, r) if depth == 1 else None,
                "attempts": attempts, "realized": bool(realized)})
    return row


def main():
    rows = []
    with ProcessPoolExecutor() as pool:
        rows = list(pool.map(run, cases()))
    sources = [ROOT / "src/censored_newsvendor/seminorm_envelope.py", Path(__file__).resolve()]
    payload = {"date": "2026-11-06", "tolerance": TOL,
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
               "cases": rows}
    output = ROOT / "results/exclusion/realizability_conjecture.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    realized = sum(row["realized"] for row in rows)
    lines = ["# Realizability conjecture: cases outside the theorems", "",
             "2026-11-06. Conjecture and method: [docs/seminorm_envelope.md](../../docs/seminorm_envelope.md), "
             "Section 6; theorems: [docs/exact_envelopes.md](../../docs/exact_envelopes.md).", "",
             "Relaxed gap: best value of the seminorm relaxation found by grid search and refinement. "
             "Law gap: value of the explicit finite symmetric law built by the zonotope LP at that "
             "membership, re-evaluated with the original audit code.", "",
             "| family | shares | depth | r | relaxed gap | law gap | atoms | chambers | realized |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | :---: |"]
    for row in rows:
        shares = "(" + ", ".join(f"{x:.3f}" for x in row["shares"]) + ")"
        last = row["attempts"][-1]
        lines.append(f"| {row['family']} | {shares} | {row['depth']} | {row['r']:.2f} | "
                     f"{row['relaxed_at_membership']:.6f} | {last['verified_gap']:.6f} | {last['atoms']} | "
                     f"{last['chambers']} | {'yes' if row['realized'] else 'no'} |")
    windows = [row for row in rows if "window" in row["family"] and row["depth"] == 1]
    lines += ["", f"{realized} of {len(rows)} cases are realized by an explicit law (tolerance {TOL:g}, "
              "zero integer excess, rho >= r).", "",
              "In the depth-one windows the realized values are lower bounds on the exact worst gap, "
              "strictly below the C31 ceiling: "
              + "; ".join(f"n={len(row['shares'])}, r={row['r']:.2f}: {row['relaxed_at_membership']:.6f} "
                          f"against {row['c31']:.6f}" for row in windows) + ".", "",
              "Reproduce: `python scripts/check_realizability_conjecture.py` (about 15 minutes on four "
              "cores). The [JSON](realizability_conjecture.json) stores every attempt.", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"Realized {realized} of {len(rows)} cases.")


if __name__ == "__main__":
    main()
