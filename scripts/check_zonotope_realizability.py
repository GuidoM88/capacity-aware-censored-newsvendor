"""Realizability of relaxed envelope values by explicit finite demand laws.

For each case the seminorm oracle supplies a maximizing membership z. The
zonotope LP then searches finite centrally symmetric laws, and the resulting
explicit law on the unit box is evaluated independently with the original
ExclusionEnvelope and coalition_table code. A case is "realized" when that
independent evaluation reproduces the relaxed value at z.
"""

import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, coalition_table
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.seminorm_envelope import (
    c31_ceiling, depth_one_envelope, minimal_cost, proportional_three_player_bound,
    separable_bound, symmetric_unit_law, three_player_bound, zonotope_minimal_cost,
)

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-6
SOLVER_TOL = 1e-6  # normalized solver tolerance (HiGHS works at about 1e-7)
CASES = [
    ("three equal shares, C39 low regime", [1 / 3] * 3, .2, False),
    ("three equal shares, C39 high regime", [1 / 3] * 3, .5, False),
    ("three unequal shares", [.6, .25, .15], .2, False),
    ("three unequal shares", [.7, .2, .1], .3, False),
    ("three proportional charges", [1 / 3] * 3, .17, True),
    ("three proportional charges", [1 / 3] * 3, .3, True),
    ("four equal shares, C31 regime", [.25] * 4, .15, False),
    ("four equal shares, window", [.25] * 4, .25, False),
    ("four equal shares, window", [.25] * 4, .3, False),
    ("four equal shares, high regime", [.25] * 4, .6, False),
    ("four proportional charges, strong pooling", [.25] * 4, .04, True),
    ("four proportional charges", [.25] * 4, .14, True),
]


def proved_bound(shares, r, pinned):
    n = len(shares)
    if n == 3:
        return proportional_three_player_bound(r) if pinned else three_player_bound(shares, r)
    return min(c31_ceiling(shares, r), separable_bound(n, r))


def run(case):
    label, shares, r, pinned = case
    shares = np.asarray(shares, dtype=float)
    n = len(shares)
    found = depth_one_envelope(shares, r, step=.01 if n == 3 else .025, pinned_singletons=pinned)
    z = np.asarray(found["membership"])
    relaxed = float(shares @ z) - minimal_cost(z, shares, r, pinned_singletons=pinned)[0]
    zono = zonotope_minimal_cost(z, shares, r, pinned_singletons=pinned,
                                 samples=400_000 if n == 3 else 2_000_000)
    states, probabilities, offer, scale = symmetric_unit_law(zono["generators"], shares)
    law = FiniteLaw(states, probabilities)
    rule = FrozenRule(offer, shares, np.ones(n))
    grand = float(probabilities @ np.abs(offer - states.sum(axis=1)))
    assert abs(grand / scale - 1) < 1e-6, (grand, scale)  # LP tolerance on c(1) <= L
    d1 = ExclusionEnvelope.population(rule, law).level(1)["upper"]
    table = coalition_table(rule, law)
    integer = max(0., max(row["excess"] for row in table))
    singles = [row["cost"] for row in table if len(row["coalition"]) == 1]
    rho = min([1.] + [grand * w / c for w, c in zip(shares, singles) if c > 1e-15])
    verified = (d1 - integer) / grand
    zonotope_gap = float(shares @ z) - zono["value"]
    assert abs(verified - zonotope_gap) < TOL, (label, verified, zonotope_gap)
    assert integer / grand < SOLVER_TOL and rho >= r - SOLVER_TOL, (label, integer, rho)
    if pinned:
        assert max(abs(grand * w / c - r) for w, c in zip(shares, singles)) < SOLVER_TOL
    bound = proved_bound(shares, r, pinned)
    return {"label": label, "shares": shares.tolist(), "r": r, "proportional": pinned,
            "membership": z.tolist(), "relaxed_gap": relaxed, "zonotope_gap": zonotope_gap,
            "verified_gap": verified, "integer_excess_over_L": integer / grand, "rho": rho,
            "realized": bool(abs(verified - relaxed) < TOL), "proved_bound": bound,
            "exact_at_this_r": bool(abs(verified - bound) < TOL),
            "chambers": zono["chambers"], "chambers_stable": zono["stable"],
            "atoms": len(probabilities), "states": states.tolist(),
            "probabilities": probabilities.tolist(), "offer": offer}


def main():
    with ProcessPoolExecutor() as pool:
        rows = list(pool.map(run, CASES))
    sources = [ROOT / "src/censored_newsvendor/seminorm_envelope.py", Path(__file__).resolve()]
    payload = {"date": "2026-11-06", "tolerance": TOL,
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
               "cases": rows}
    output = ROOT / "results/exclusion/zonotope_realizability.json"
    output.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    lines = ["# Realizability of relaxed envelope values", "",
             "2026-11-06, branch `pulp-fiction`. For each case the seminorm oracle gives a maximizing "
             "membership; a zonotope LP finds a finite centrally symmetric law on the unit box; that "
             "law is evaluated independently with `ExclusionEnvelope` and `coalition_table`. "
             "See [docs/seminorm_envelope.md](../../docs/seminorm_envelope.md), Section 6.", "",
             "| case | shares | r | relaxed gap | verified law gap | atoms | proved bound | exact at r |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |"]
    for row in rows:
        shares = "(" + ", ".join(f"{x:.3g}" for x in row["shares"]) + ")"
        lines.append(f"| {row['label']} | {shares} | {row['r']:.2f} | {row['relaxed_gap']:.6f} | "
                     f"{row['verified_gap']:.6f} | {row['atoms']} | {row['proved_bound']:.6f} | "
                     f"{'yes' if row['exact_at_this_r'] else 'no'} |")
    realized = sum(row["realized"] for row in rows)
    exact = sum(row["exact_at_this_r"] for row in rows)
    lines += ["", f"{realized} of {len(rows)} relaxed values are attained by an explicit law with "
              f"zero integer excess and rho = r, both up to the solver tolerance {SOLVER_TOL:g}. In {exact} cases the attained value equals a proved "
              "upper bound, so it is the exact worst gap at that ratio. Elsewhere it is a lower bound "
              "on the exact worst gap; the relaxation's own maximum there is not certified.", "",
              "Reproduce: `python scripts/check_zonotope_realizability.py`. The "
              "[JSON](zonotope_realizability.json) stores each law (states, probabilities, offer).", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"Realized {realized} of {len(rows)} cases; {exact} exact at their ratio.")


if __name__ == "__main__":
    main()
