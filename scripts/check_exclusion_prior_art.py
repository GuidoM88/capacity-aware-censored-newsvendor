"""Check the fixed-allocation reduction and distinguish two fuzzy extensions.

These deterministic checks corroborate the algebra in exclusion_prior_art.md.
They cannot establish bibliographic priority or publication significance.
"""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from censored_newsvendor.coalition_audit import FiniteLaw, exact_excess, forecast_rule
from censored_newsvendor.exclusion import ExclusionEnvelope


ROOT = Path(__file__).resolve().parents[1]


def rank_one_root(difference, charges, minimum_mass):
    """Independent primal LP: minimize t/2 - a.z, with t >= |d.z|."""
    n = len(charges)
    rows = [np.r_[difference, -1.], np.r_[-difference, -1.],
            np.r_[np.ones(n), 0.]]
    rhs = [0., 0., n - 1.]
    if minimum_mass:
        rows.append(np.r_[-np.ones(n), 0.])
        rhs.append(-float(minimum_mass))
    result = linprog(np.r_[-charges, .5], A_ub=rows, b_ub=rhs,
                     bounds=[(0., 1.)] * n + [(0., None)], method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return max(0., -float(result.fun)), result.x[:n], float(result.fun)


def check_family(units, size):
    n = len(units)
    fractions = [Fraction(x, sum(units)) for x in units]
    weights = np.array(fractions, dtype=float)
    total = size + 2 * (n - 2)
    states = np.array([[0.] * (n - 1) + [total - 1.],
                       [float(size)] + [2.] * (n - 2) + [0.]]) / total
    truth = FiniteLaw(states, [.5, .5])
    forecast = FiniteLaw(states.sum(axis=1)[:, None] * weights, [.5, .5])
    rule = forecast_rule(forecast, np.ones(n))
    grand_loss = 1 / (2 * total)
    difference = states[1] - states[0]
    charges = grand_loss * weights
    integer = exact_excess(rule, truth)
    assert integer["excess"] == 0
    assert integer["worst_coalition"]["excess"] < 0

    root, membership, _ = rank_one_root(difference, charges, 0)
    burer, _, raw_minimum = rank_one_root(difference, charges, 1)
    dual_root = ExclusionEnvelope.population(rule, truth).level(0)["upper"]
    np.testing.assert_allclose([root, root], [burer, dual_root], atol=1e-10, rtol=0)
    ceiling = 1 - min(fractions)
    depth_one_witness = ceiling - fractions[-1] / (total - 1)
    assert float(depth_one_witness) - 1e-9 <= root / grand_loss
    assert root / grand_loss <= float(ceiling) + 1e-9

    # The Euclidean-norm cost is identical at every vertex, and at the LP maximizer.
    memberships = np.array([[(mask >> j) & 1 for j in range(n)]
                            for mask in range(1, 2 ** n)], dtype=float)
    memberships = np.vstack([memberships, membership])
    physical_cost = np.abs(memberships @ difference) / 2
    rank_one_matrix = difference[None, :] / 2
    norm_cost = np.linalg.norm(memberships @ rank_one_matrix.T, axis=1)
    np.testing.assert_allclose(norm_cost, physical_cost, atol=1e-12, rtol=0)
    return {"n": n, "size": size, "share_units": units, "grand_loss": grand_loss,
            "integer_excess": integer["excess"],
            "largest_unclipped_integer_excess": integer["worst_coalition"]["excess"],
            "root_primal": root, "root_dual": dual_root,
            "burer_fixed_allocation_minimum": raw_minimum,
            "burer_positive_negative_part": burer,
            "root_gap_over_L": root / grand_loss,
            "depth_one_witness_ratio": str(depth_one_witness),
            "root_supremum": str(ceiling),
            "cost_identity_points": len(memberships)}


def canonical_example():
    # Unscaled n=3, m=2 instance: high=(2,2,0), low=(0,0,3).
    difference = np.array([2., 2., -3.])
    membership = np.array([1., 0., 2 / 3])
    charges = np.ones(3) / 6
    coalitions = np.array([[(mask >> j) & 1 for j in range(3)]
                           for mask in range(1, 8)], dtype=float)
    costs = np.abs(coalitions @ difference) / 2
    result = linprog(costs, A_eq=coalitions.T, b_eq=membership,
                     bounds=(0., None), method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    physical = abs(difference @ membership) / 2
    assigned = charges @ membership
    np.testing.assert_allclose([physical, assigned, result.fun],
                               [0., 5 / 18, 2 / 3], atol=1e-12, rtol=0)
    assert (costs[:-1] - coalitions[:-1] @ charges > 0).all()
    return {"scope": "Unscaled exact three-producer illustration, not a Gaussian sample",
            "membership": ["1", "0", "2/3"],
            "physical_cost": float(physical), "exact_physical_cost": "0",
            "assigned_charge": float(assigned), "exact_assigned_charge": "5/18",
            "canonical_cost": float(result.fun), "exact_canonical_cost": "2/3",
            "positive_physical_excess": float(assigned - physical),
            "positive_canonical_excess": max(0., float(assigned - result.fun)),
            "nonzero_cover": [{"coalition": [j + 1 for j, x in enumerate(coalitions[i]) if x],
                                "coefficient": float(x)} for i, x in enumerate(result.x) if x > 1e-12]}


def clipping_example():
    # Algebra-only example c(z)=sum(z), a_j=1/2: budget balance is deliberately
    # absent. Every nonempty coalition has negative excess, requiring clipping.
    root, _, _ = rank_one_root(np.array([2., 2., 2.]), np.ones(3) / 2, 0)
    clipped, _, raw_minimum = rank_one_root(np.array([2., 2., 2.]), np.ones(3) / 2, 1)
    np.testing.assert_allclose([root, clipped, raw_minimum], [0., 0., .5], atol=1e-12)
    return {"scope": "Homogeneous objective algebra only; charges are not budget balanced",
            "root": root, "burer_raw_minimum": raw_minimum,
            "clipped_negative_minimum": clipped}


def main():
    instances = []
    for n in (3, 6, 8):
        for units in ([1] * n, [n, *range(1, n - 1), n - 1]):
            instances.extend(check_family(units, size) for size in (2, 20, 200))
    example = canonical_example()
    clipped = clipping_example()
    inputs = [Path(__file__), ROOT / "src/censored_newsvendor/coalition_audit.py",
              ROOT / "src/censored_newsvendor/exclusion.py"]
    payload = {"date": "2026-11-05", "scope": "Deterministic reductions, not a novelty test",
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
               "instances": instances, "canonical_example": example, "clipping_example": clipped}
    folder = ROOT / "results/exclusion"
    (folder / "prior_art_checks.json").write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    rows = ["# Checks for the prior-art comparison", "", "2026-11-05. Deterministic algebra checks; no bibliographic-priority inference.", "",
            f"All {len(instances)} bounded two-state instances match the independent root LP, the existing dual implementation and the sign-clipped fixed-allocation program from Burer and Dror (2005), equation 19.", "",
            f"The rank-one norm and physical costs agree at {sum(x['cost_identity_points'] for x in instances)} membership points (all nonempty vertices plus each root LP maximizer).",
            "", "| n | m | Share units | Root gap / L | Sharp supremum |", "| ---: | ---: | --- | ---: | ---: |"]
    for item in instances:
        rows.append(f"| {item['n']} | {item['size']} | {item['share_units']} | {item['root_gap_over_L']:.9f} | {item['root_supremum']} |")
    rows.extend(["", "All actual proper coalitions are strictly stable in these 18 laws.", "",
                 "For the separate exact three-producer example, z=(1,0,2/3): physical cost 0, assigned charge 5/18, canonical extension cost 2/3. Both extensions agree on every actual coalition.", "",
                 "An additional algebra-only case checks positive-part clipping when the unmodified minimum is +1/2. Its charges are deliberately not budget balanced; it is not an additional calibrated example.", "",
                 "Reproduce with `python scripts/check_exclusion_prior_art.py`. The proof and scope are in [the comparison](../../docs/exclusion_prior_art.md).", ""])
    (folder / "prior_art_checks.md").write_text("\n".join(rows))
    print(f"Passed {len(instances)} three-way root comparisons, {sum(x['cost_identity_points'] for x in instances)} cost identities, canonical-extension LP and clipping case.")


if __name__ == "__main__":
    main()
