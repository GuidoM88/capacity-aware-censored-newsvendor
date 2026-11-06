"""Deterministic checks of the three-player standalone-ratio envelope.

Matching examples, strict mixtures and off-family falsification checks are
kept separate. LP/MILP solves here verify values; they are not a speed benchmark.
"""

import hashlib
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

import numpy as np
import scipy

from censored_newsvendor.coalition_audit import (
    FiniteLaw, FrozenRule, coalition_table, forecast_rule, loss, optimal_offer,
)
from censored_newsvendor.exclusion import ExclusionEnvelope
from check_exclusion_robustness import primal_face


ROOT = Path(__file__).resolve().parents[1]
THIRD = F(1, 3)


def envelope(r):
    return 2 * THIRD * (1 - r) if r <= THIRD else (1 - r * r) / (6 * r)


def coefficients(r):
    m = THIRD / r
    if r <= THIRD:
        return [m - 2 * THIRD, F(0), -m], [F(0), F(1), F(0)]
    return [THIRD, THIRD, -m], [2 * THIRD - m, THIRD, m]


def raw_states(r):
    u, v = coefficients(r)
    return [[s * x + t * y for x, y in zip(u, v)]
            for s, t in product([-1, 1], repeat=2)]


def normalized_law(raw, probabilities):
    radius = max(abs(x) for row in raw for x in row)
    states = .5 + np.array(raw, dtype=float) / (2 * float(radius))
    return FiniteLaw(states, probabilities), radius


def check_law(law, rule, category, expected_rho=None, exact_gap=None, strict=False):
    total = law.states.sum(axis=1)
    grand = float(law.probabilities @ loss(rule.offer, total))
    singleton = [optimal_offer(law.states[:, j], law.probabilities)[1] for j in range(3)]
    rho = min([1.] + [grand / (3 * c) for c in singleton if c > 0])
    table = coalition_table(rule, law)
    largest_integer = max(row["excess"] for row in table)
    integer = max(0., largest_integer)
    if strict:
        assert largest_integer < 0, largest_integer
    if expected_rho is not None:
        np.testing.assert_allclose(rho, float(expected_rho), atol=1e-10, rtol=0)
        np.testing.assert_allclose(integer, 0., atol=1e-10, rtol=0)

    env = ExclusionEnvelope.population(rule, law)
    faces = []
    for excluded in range(3):
        primal, membership = primal_face(rule, law, grand, excluded)
        dual, _ = env._face((excluded,), grand)
        np.testing.assert_allclose(primal, dual, atol=1e-9, rtol=0)
        faces.append({"excluded": excluded + 1, "primal": primal, "dual": dual,
                      "membership": membership})
    d1 = max(row["primal"] for row in faces)
    milp = env.binary_reference()
    np.testing.assert_allclose(milp, integer, atol=1e-9, rtol=0)
    gap = max(0., d1 - integer) / grand
    ceiling = float(envelope(rho))
    assert gap <= ceiling + 1e-9, (rho, gap, ceiling)
    if exact_gap is not None:
        np.testing.assert_allclose(gap, float(exact_gap), atol=1e-9, rtol=0)
    centered = law.states - (law.probabilities @ law.states)
    covariance = centered.T @ (law.probabilities[:, None] * centered)
    return {
        "category": category, "rho": rho, "grand_loss": grand,
        "grand_to_maximum_ratio": grand / rule.loss_range,
        "singleton_costs": singleton, "integer_excess": integer,
        "largest_unclipped_integer_excess": largest_integer,
        "d1": d1, "gap_over_L": gap, "envelope": ceiling,
        "minimum_covariance_eigenvalue": float(np.linalg.eigvalsh(covariance)[0]),
        "milp_excess": milp, "faces": faces,
    }


def main():
    ratios = [F(1, 20), F(1, 10), F(1, 5), F(1, 3), F(2, 5),
              F(1, 2), F(4, 5), F(9, 10), F(1)]
    matching = []
    for r in ratios:
        raw = raw_states(r)
        u, v = coefficients(r)
        t = 1 - 2 * r if r <= THIRD else (1 - r) / 2
        z = [F(1), F(0), t]
        cost = max(abs(sum(x * y for x, y in zip(u, z))),
                   abs(sum(x * y for x, y in zip(v, z))))
        exact = sum(z) / 3 - cost
        assert exact == envelope(r)
        law, radius = normalized_law(raw, np.ones(4) / 4)
        forecast = FiniteLaw(np.repeat((law.states.sum(axis=1) / 3)[:, None], 3, axis=1),
                             law.probabilities)
        rule = forecast_rule(forecast, np.ones(3))
        np.testing.assert_allclose(rule.weights, np.ones(3) / 3, atol=1e-12, rtol=0)
        np.testing.assert_allclose(rule.offer, 1.5, atol=1e-12, rtol=0)
        np.testing.assert_allclose(law.probabilities @ law.states,
                                   forecast.probabilities @ forecast.states, atol=1e-12, rtol=0)
        row = check_law(law, rule, "attainment", r, exact)
        row.update({"r_exact": str(r), "gap_over_L_exact": str(exact),
                    "witness": [str(x) for x in z],
                    "witness_cost_before_scaling": str(cost), "scaling_radius": str(radius)})
        matching.append(row)

    seed = [[F(9, 10) * x for x in row] for row in product([-1, 0, 1], repeat=3)]
    assert sum(abs(sum(row)) for row in seed) / 27 == 1
    assert all(sum(abs(row[j]) for row in seed) / 27 == F(3, 5) for j in range(3))
    assert all(sum(abs(row[i] + row[j]) for row in seed) / 27 == F(4, 5)
               for i, j in [(0, 1), (0, 2), (1, 2)])
    strict_rows = []
    for r in (F(1, 10), F(1, 3), F(1, 2), F(4, 5), F(19, 20)):
        for epsilon in (F(1, 100), F(1, 1000)):
            base_r = (1 - epsilon) / (1 / r - F(9, 5) * epsilon)
            assert 0 < base_r < 1
            states = raw_states(base_r) + seed
            mass = np.r_[np.full(4, float((1 - epsilon) / 4)),
                         np.full(27, float(epsilon / 27))]
            law, radius = normalized_law(states, mass)
            forecast = FiniteLaw(np.repeat((law.states.sum(axis=1) / 3)[:, None], 3, axis=1), mass)
            rule = forecast_rule(forecast, np.ones(3))
            np.testing.assert_allclose(rule.weights, np.ones(3) / 3, atol=1e-12, rtol=0)
            row = check_law(law, rule, "strict_approximation", r, strict=True)
            lower = (1 - epsilon) * envelope(base_r) - F(6, 5) * epsilon
            assert row["gap_over_L"] >= float(lower) - 1e-9
            assert row["minimum_covariance_eigenvalue"] > 0
            row.update({"r_exact": str(r), "epsilon": str(epsilon), "base_r": str(base_r),
                        "limiting_supremum": str(envelope(r)),
                        "proved_approximation_lower": str(lower), "scaling_radius": str(radius)})
            strict_rows.append(row)

    # Fixed-seed checks try to refute the upper bound on unrelated finite laws.
    # Two offers per law include an optimum and a deliberately shifted offer.
    rng = np.random.default_rng(20261106)
    off_family = []
    for number in range(4):
        law = FiniteLaw(rng.uniform(0, 1, size=(8, 3)), rng.dirichlet(np.ones(8)))
        q, _ = optimal_offer(law.states.sum(axis=1), law.probabilities)
        for offer in (q, .25 if number % 2 else 2.75):
            rule = FrozenRule(offer, np.ones(3) / 3, np.ones(3))
            row = check_law(law, rule, "off_family_upper_bound")
            row.update({"law_index": number, "offer": offer,
                        "states": law.states.tolist(), "probabilities": law.probabilities.tolist()})
            off_family.append(row)

    sources = [Path(__file__), ROOT / "docs/three_player_rho.md",
               ROOT / "scripts/check_exclusion_robustness.py",
               ROOT / "src/censored_newsvendor/coalition_audit.py",
               ROOT / "src/censored_newsvendor/exclusion.py"]
    count = len(matching) + len(strict_rows) + len(off_family)
    payload = {
        "date": "2026-11-06", "scope": "Deterministic proof checks, not a performance or priority result",
        "versions": {"numpy": np.__version__, "scipy": scipy.__version__},
        "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        "attaining_instances": matching, "strict_approximations": strict_rows,
        "off_family_checks": off_family,
        "execution": {"instances": count, "primal_dual_face_comparisons": 3 * count,
                      "lp_solves": 6 * count, "milp_solves": count},
    }
    output = ROOT / "results/exclusion/three_player_rho.json"
    output.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    lines = ["# Three-player structural-envelope checks", "",
             "2026-11-06. See the [full proof](../../docs/three_player_rho.md).",
             "These are deterministic checks of a derived theorem. No statistical or runtime advantage is claimed.",
             "", "| Exact rho | Exact gap/L | LP gap/L | Previous ceiling |",
             "| --- | --- | ---: | ---: |"]
    for row in matching:
        r = F(row["r_exact"])
        lines.append(f"| {r} | {row['gap_over_L_exact']} | {row['gap_over_L']:.9f} | {float(2 * THIRD * (1-r)):.9f} |")
    lines.extend(["", "All nine attaining laws have B=0. Ten mixture cases have strictly negative "
                  "excess for every proper coalition and positive definite covariance, while keeping "
                  "the exact prescribed rho. The eight off-family cases include optimal and shifted offers.",
                  "", f"All {3*count} independent primal/dual face comparisons and {count} "
                  "MILP/enumeration comparisons pass at 1e-9 tolerance. "
                  "The MILPs are value checks, not branch-and-bound performance measurements.",
                  "", "Reproduce: python scripts/check_three_player_rho.py. "
                  "The [JSON](three_player_rho.json) records every case, solver value, exact expression, "
                  "input law for the off-family checks, and source hashes.", ""])
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"Passed {len(matching)} attaining, {len(strict_rows)} strict and {len(off_family)} off-family cases; "
          f"{3*count} primal/dual comparisons and {count} MILP checks.")


if __name__ == "__main__":
    main()
