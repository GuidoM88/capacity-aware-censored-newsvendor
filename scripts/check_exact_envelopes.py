"""Checks for the explicit worst-case laws of docs/exact_envelopes.md.

Two independent checks per construction:
1. exact rational arithmetic on every constraint (caps, all proper
   coalitions, grand cost, witness value), via verify_generators;
2. for a subset, the explicit law is mapped to the unit box and evaluated
   with the original ExclusionEnvelope and coalition_table code.
The closed forms are also compared with the proved upper bounds.
"""

import hashlib
import json
import random
from fractions import Fraction as F
from pathlib import Path

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, coalition_table
from censored_newsvendor.exact_envelopes import (
    equal_share_construction, four_line_bound, high_threshold, last_depth_construction,
    last_depth_value, verify_generators, windows,
)
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.seminorm_envelope import symmetric_unit_law

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-7


def separable_bound_depth(n, depth, r):
    """Proved equal-share bound U at a given depth (Proposition 2 of the note)."""
    free = n - depth
    if r <= (free - 1) / (free + 1):
        return (1 - r) * free / n
    return (free - 1) * (1 - r * r) / (2 * n * r)


def exact_ok(check, r):
    return (check["cap"] >= 0 and check["stability"] >= 0 and check["grand"] >= 0
            and check["witness"] == 0 and check["rho"] == r)


def independent(construction, shares, r, depth):
    generators = np.array([[float(x) for x in g] for g in construction["generators"]])
    shares = np.array([float(x) for x in shares])
    states, probabilities, offer, _ = symmetric_unit_law(generators, shares)
    rule = FrozenRule(offer, shares, np.ones(len(shares)))
    law = FiniteLaw(states, probabilities)
    grand = float(probabilities @ np.abs(offer - states.sum(axis=1)))
    upper = ExclusionEnvelope.population(rule, law).level(depth)["upper"]
    table = coalition_table(rule, law)
    integer = max(0., max(row["excess"] for row in table))
    singles = [row["cost"] for row in table if len(row["coalition"]) == 1]
    rho = min([1.] + [grand * w / c for w, c in zip(shares, singles) if c > 1e-15])
    return {"gap": (upper - integer) / grand, "integer_over_L": integer / grand, "rho": rho,
            "atoms": len(probabilities)}


def main():
    ratios = [F(k, 60) for k in range(1, 61)]
    equal_rows, equal_count, windows_rows = [], 0, []
    for n in range(3, 11):
        for depth in range(1, n - 1):
            for r in ratios:
                construction = equal_share_construction(n, r, depth)
                if construction is None:
                    continue
                check = verify_generators(construction["generators"], [F(1, n)] * n, r,
                                          construction["membership"], construction["value"])
                assert exact_ok(check, r), (n, depth, r, check)
                bound = separable_bound_depth(n, depth, float(r))
                assert abs(float(construction["value"]) - bound) < TOL, (n, depth, r)
                equal_count += 1
                if n <= 6 and r.denominator in (60, 30, 20, 15, 12, 10, 6, 5, 4, 3) and r * 60 % 7 == 0:
                    found = independent(construction, [F(1, n)] * n, r, depth)
                    assert abs(found["gap"] - float(construction["value"])) < 1e-6, (n, depth, r, found)
                    assert found["integer_over_L"] < 1e-6 and found["rho"] >= float(r) - 1e-6
                    equal_rows.append({"n": n, "depth": depth, "r": str(r),
                                       "regime": construction["regime"], "p": construction["p"],
                                       "value": str(construction["value"]),
                                       "independent_gap": found["gap"], "atoms": found["atoms"]})
    for n in range(3, 31):
        gaps = windows(n)
        windows_rows.append({"n": n, "windows": [[str(lo), str(hi)] for lo, hi in gaps],
                             "total_length": str(sum((hi - lo for lo, hi in gaps), F(0))),
                             "high_threshold": str(high_threshold(n))})

    rng = random.Random(20261106)
    last_rows, last_count = [], 0
    for n in (3, 4, 5, 6):
        for _ in range(150):
            raw = [F(rng.randint(1, 40)) for _ in range(n)]
            shares = [x / sum(raw) for x in raw]
            r = F(rng.randint(1, 60), 60)
            construction = last_depth_construction(shares, r)
            check = verify_generators(construction["generators"], shares, r,
                                      construction["membership"], construction["value"])
            assert exact_ok(check, r), (shares, r, check)
            assert construction["value"] == last_depth_value(shares, r)
            assert abs(float(construction["value"]) - four_line_bound(shares, float(r))) < TOL
            last_count += 1
            if n <= 5 and len(last_rows) < 40:
                found = independent(construction, shares, r, n - 2)
                assert abs(found["gap"] - float(construction["value"])) < 1e-6, (shares, r, found)
                assert found["integer_over_L"] < 1e-6 and found["rho"] >= float(r) - 1e-6
                last_rows.append({"n": n, "shares": [str(x) for x in shares], "r": str(r),
                                  "regime": construction["regime"],
                                  "pair": list(construction["pair"]),
                                  "value": str(construction["value"]),
                                  "independent_gap": found["gap"], "atoms": found["atoms"]})

    sources = [ROOT / "src/censored_newsvendor/exact_envelopes.py", Path(__file__).resolve()]
    payload = {"date": "2026-11-06",
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
               "equal_shares": {"exact_checks": equal_count, "independent_checks": equal_rows},
               "last_depth": {"exact_checks": last_count, "independent_checks": last_rows},
               "windows_depth_one": windows_rows}
    output = ROOT / "results/exclusion/exact_envelopes.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")

    lines = ["# Explicit worst-case laws: checks", "",
             "2026-11-06. Theorems and proofs: [docs/exact_envelopes.md](../../docs/exact_envelopes.md).", "",
             f"* Equal shares, n = 3..10, every depth, r = k/60: {equal_count} constructions pass the "
             "exact rational check of every constraint (standalone caps, all proper coalitions, "
             "grand cost, witness value) and match the proved upper bound.",
             f"* Arbitrary shares at depth n-2, n = 3..6, 600 random rational instances: "
             f"{last_count} constructions pass the same exact check and equal the four-line bound.",
             f"* {len(equal_rows) + len(last_rows)} of these laws were also mapped to the unit box and "
             "re-evaluated with `ExclusionEnvelope` and `coalition_table`; all reproduce the value "
             "with zero integer excess and rho = r (tolerance 1e-6).", "",
             "## Depth-one windows for equal shares", "",
             "Ratios in these open intervals are the only ones where the depth-one value is not "
             "settled. The same windows appear at depth k for n - k + 1 producers.", "",
             "| n | windows | total length |", "| ---: | --- | ---: |"]
    for row in windows_rows:
        text = ", ".join(f"({lo}, {hi})" for lo, hi in row["windows"]) or "none"
        lines.append(f"| {row['n']} | {text} | {float(F(row['total_length'])):.4f} |")
    lines += ["", "## Sample of independently re-evaluated laws", "",
              "| family | n | depth | r | regime | value | re-evaluated | atoms |",
              "| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |"]
    for row in equal_rows[:20]:
        lines.append(f"| equal shares | {row['n']} | {row['depth']} | {row['r']} | {row['regime']} "
                     f"(p={row['p']}) | {float(F(row['value'])):.6f} | {row['independent_gap']:.6f} | {row['atoms']} |")
    for row in last_rows[:12]:
        lines.append(f"| shares {', '.join(row['shares'])} | {row['n']} | {row['n'] - 2} | {row['r']} | "
                     f"{row['regime']} | {float(F(row['value'])):.6f} | {row['independent_gap']:.6f} | {row['atoms']} |")
    lines += ["", "Reproduce: `python scripts/check_exact_envelopes.py`.", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"{equal_count} equal-share and {last_count} last-depth constructions verified exactly; "
          f"{len(equal_rows) + len(last_rows)} re-evaluated independently.")


if __name__ == "__main__":
    main()
