"""Deterministic checks of the continuous-law and fixed-scale constructions.

The proofs are in docs/exclusion_robustness.md. Midpoint grids below are
discrete approximations, not samples from the continuous law or empirical
coverage experiments. Independent primal LPs are compared to existing duals.
"""

import hashlib
import json
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, eye, hstack, vstack

from censored_newsvendor.coalition_audit import (
    FiniteLaw, FrozenRule, coalition_table, forecast_rule, optimal_offer,
)
from censored_newsvendor.exclusion import ExclusionEnvelope


ROOT = Path(__file__).resolve().parents[1]


def midpoint_noise(order, dimension):
    nodes = -1 + (2 * np.arange(order) + 1) / order
    return np.array(list(product(nodes, repeat=dimension)))


def primal_face(rule, law, grand, excluded):
    """Membership/offer/absolute-loss primal, independent of the dual code."""
    free = [j for j in range(len(rule.weights)) if j != excluded]
    states = law.states[:, free]
    count = len(states)
    positive = hstack([csr_matrix(states), csr_matrix(-np.ones((count, 1))),
                       -eye(count, format="csr")], format="csr")
    negative = hstack([csr_matrix(-states), csr_matrix(np.ones((count, 1))),
                       -eye(count, format="csr")], format="csr")
    objective = np.r_[-grand * rule.weights[free], 0., law.probabilities]
    result = linprog(
        objective, A_ub=vstack([positive, negative]), b_ub=np.zeros(2 * count),
        bounds=[(0., 1.)] * len(free) + [(0., float(rule.rated[free].sum()))]
        + [(0., None)] * count, method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    z = np.zeros(len(rule.weights))
    z[free] = result.x[:len(free)]
    _, cost = optimal_offer(law.states @ z, law.probabilities)
    value = max(0., float(grand * (rule.weights @ z) - cost))
    np.testing.assert_allclose(value, max(0., -result.fun), atol=1e-10, rtol=0)
    return value, z.tolist()


def continuous_sharpness_checks():
    """Rational checks of the conditions used in the general proof."""
    records = []
    for n in (3, 6, 8):
        for units in ([1] * n, [n, *range(1, n - 1), n - 1]):
            w = [F(x, sum(units)) for x in units]
            for m in (2, 20, 200):
                h = m + 2 * (n - 2)
                delta = min(F(1, 8 * n * h * h),
                            (1 - max(w)) / (4 * (n - 1) * max(w)))
                scale = 1 - 2 * delta
                grand = scale / (2 * h)
                assert n * delta < grand
                assert max(w) * (1 + 2 * delta * (n - 1)) < 1
                differences = [F(m, h)] + [F(2, h)] * (n - 2) + [F(1 - h, h)]
                margins = []
                for size in range(1, n):
                    for coalition in combinations(range(n), size):
                        cost = scale * abs(sum(differences[j] for j in coalition)) / 2
                        assert size * delta < cost
                        margin = cost - grand * sum(w[j] for j in coalition)
                        assert margin > 0
                        margins.append(margin)
                levels = []
                for k in range(1, n - 1):
                    ceiling = sum(sorted(w, reverse=True)[:n-k])
                    atomic_witness = ceiling - w[-1] * F(2 * k - 1, h - 1)
                    smoothing_loss = n * delta / grand
                    assert smoothing_loss <= 1 / (4 * h * scale)
                    levels.append({
                        "k": k, "supremum": str(ceiling),
                        "continuous_witness_ratio_lower": str(atomic_witness - smoothing_loss),
                        "smoothing_loss_bound": str(smoothing_loss),
                    })
                records.append({
                    "n": n, "m": m, "share_units": units,
                    "noise_radius": str(delta), "grand_loss": str(grand),
                    "minimum_covariance_eigenvalue": str(delta * delta / 3),
                    "minimum_integer_margin": str(min(margins)),
                    "coalitions_checked": len(margins), "levels": levels,
                })
    return records


def fixed_scale_checks():
    base = [[F(4, 5), F(4, 5), F(1, 20)],
            [F(1, 5), F(1, 5), F(19, 20)]]
    shares = [F(9, 20), F(1, 10), F(9, 20)]
    delta, grand, maximum = F(1, 25), F(3, 20), F(3, 2)
    z = [F(1), F(0), F(2, 3)]
    charge = grand * sum(x * y for x, y in zip(shares, z))
    noise_cost = delta * F(31, 54)
    witness = charge - noise_cost
    assert charge == F(9, 80)
    assert witness == F(967, 10800)
    assert witness / maximum == F(967, 16200) > F(1, 20)
    assert grand / maximum == F(1, 10)
    assert sum(a * b for a, b in zip(base[0], z)) == sum(a * b for a, b in zip(base[1], z))
    exact_rows = []
    for size in (1, 2):
        for indices in combinations(range(3), size):
            difference = sum(base[0][j] - base[1][j] for j in indices)
            cost = abs(difference) / 2
            assigned = grand * sum(shares[j] for j in indices)
            assert size * delta < cost and cost > assigned
            exact_rows.append({"coalition": [j + 1 for j in indices],
                               "cost": str(cost), "assigned_charge": str(assigned),
                               "strict_margin": str(cost - assigned)})

    # Integrate both independent uniforms, splitting the inner absolute-value kink.
    def outer(v):
        return quad(lambda u: abs(u + 2 * v / 3) / 2, -1, 1,
                    points=[-2 * v / 3], epsabs=1e-12, epsrel=1e-12)[0] / 2
    quadrature, integration_error = quad(outer, -1, 1, epsabs=1e-12, epsrel=1e-12)
    np.testing.assert_allclose(quadrature, float(F(31, 54)), atol=1e-12, rtol=0)
    covariance = np.outer([.3, .3, -.45], [.3, .3, -.45]) + float(delta**2 / 3) * np.eye(3)
    eigenvalues = np.linalg.eigvalsh(covariance)
    np.testing.assert_allclose(eigenvalues[:2], float(F(1, 1875)), atol=1e-14, rtol=0)

    rule = FrozenRule(float(maximum), np.array(shares, dtype=float), np.ones(3))
    base_array = np.array(base, dtype=float)
    grids = []
    for order in (3, 7, 15):
        noise = midpoint_noise(order, 3)
        full_states = np.vstack([b + float(delta) * noise for b in base_array])
        mass = np.full(len(full_states), 1 / len(full_states))
        law = FiniteLaw(full_states, mass)
        table = coalition_table(rule, law)
        for observed, exact in zip(table, exact_rows):
            assert observed["coalition"] == exact["coalition"]
            np.testing.assert_allclose(observed["cost"], float(F(exact["cost"])),
                                       atol=1e-12, rtol=0)
            assert observed["excess"] < 0
        forecast = FiniteLaw(.5 + (full_states.sum(axis=1)[:, None] - 1.5) * rule.weights, mass)
        np.testing.assert_allclose(mass @ forecast.states, mass @ full_states, atol=1e-12, rtol=0)
        recovered_rule = forecast_rule(forecast, np.ones(3))
        np.testing.assert_allclose(recovered_rule.weights, rule.weights, atol=1e-12, rtol=0)
        np.testing.assert_allclose(recovered_rule.offer, rule.offer, atol=1e-12, rtol=0)
        discrete_grand = mass @ np.abs(full_states.sum(axis=1) - rule.offer)
        np.testing.assert_allclose(discrete_grand, float(grand), atol=1e-12, rtol=0)
        _, discrete_witness_cost = optimal_offer(full_states @ np.array(z, dtype=float), mass)
        assert abs(discrete_witness_cost - float(noise_cost)) <= float(delta) * sum(z) / order
        faces = []
        for excluded in range(3):
            free = [j for j in range(3) if j != excluded]
            two_noise = midpoint_noise(order, 2)
            projected = np.zeros((2 * len(two_noise), 3))
            projected[:, free] = np.vstack([b[free] + float(delta) * two_noise for b in base_array])
            face_law = FiniteLaw(projected, np.full(len(projected), 1 / len(projected)))
            primal, membership = primal_face(rule, face_law, float(grand), excluded)
            # Only free coordinates enter the face optimization. Keep the actual
            # grand-cost endpoint; projected dummy coordinates do not define it.
            envelope = ExclusionEnvelope(rule, face_law, [float(grand)], np.zeros(3))
            dual, _ = envelope._face((excluded,), float(grand))
            np.testing.assert_allclose(primal, dual, atol=1e-9, rtol=0)
            faces.append({"excluded": excluded + 1, "primal": primal, "dual": dual,
                          "membership": membership})
        grid_d1 = max(x["primal"] for x in faces)
        # Coupling a uniform to its midpoint gives per-coordinate error <= delta/order.
        radius = 2 * float(delta) / order
        assert grid_d1 + radius >= float(witness) - 1e-12
        grids.append({
            "midpoints_per_coordinate": order, "full_states": len(full_states),
            "states_per_projected_face": 2 * order**2,
            "integer_excess": 0.0, "grid_d1": grid_d1,
            "continuous_d1_discretization_radius": radius,
            "continuous_d1_lower": max(float(witness), grid_d1 - radius),
            "continuous_d1_upper": min(float(grand) * .9, grid_d1 + radius),
            "faces": faces,
        })
    return {
        "noise_radius": str(delta), "grand_loss": str(grand), "maximum_loss": str(maximum),
        "grand_to_maximum_ratio": str(grand / maximum), "integer_excess": "0",
        "membership": [str(x) for x in z], "witness_cost": str(noise_cost),
        "witness_charge": str(charge), "gap_lower": str(witness),
        "gap_over_maximum_lower": str(witness / maximum),
        "minimum_covariance_eigenvalue": "1/1875",
        "quadrature_noise_absolute_mean": quadrature,
        "quadrature_reported_error": integration_error,
        "coalitions": exact_rows, "midpoint_checks": grids,
    }


def main():
    general = continuous_sharpness_checks()
    fixed = fixed_scale_checks()
    sources = [Path(__file__), ROOT / "docs/exclusion_robustness.md",
               ROOT / "src/censored_newsvendor/coalition_audit.py",
               ROOT / "src/censored_newsvendor/exclusion.py"]
    payload = {
        "date": "2026-11-06",
        "scope": "Deterministic proof checks; no new statistical experiment or priority claim",
        "versions": {"numpy": np.__version__, "scipy": scipy.__version__},
        "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        "continuous_sharpness_checks": general, "fixed_scale": fixed,
        "execution": {"general_instances": len(general),
                      "nonterminal_levels": sum(len(x["levels"]) for x in general),
                      "integer_margin_checks": sum(x["coalitions_checked"] for x in general),
                      "primal_dual_face_comparisons": 9, "lp_solves": 18},
    }
    target = ROOT / "results/exclusion/robustness.json"
    target.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    lines = [
        "# Continuous-law and fixed-scale checks", "",
        "2026-11-06. Deterministic checks of the [proof](../../docs/exclusion_robustness.md).",
        "The midpoint laws below are discrete approximations, not iid experimental samples.", "",
        f"General construction: {len(general)} instances, {payload['execution']['nonterminal_levels']} "
        f"nonterminal levels and {payload['execution']['integer_margin_checks']} exact rational "
        "coalition-margin checks.", "",
        "Fixed continuous example: L/A = 1/10, B = 0, and minimum covariance eigenvalue "
        "1/1875. A feasible fractional membership proves (D1-B)/A >= 967/16200 "
        f"= {float(F(fixed['gap_over_maximum_lower'])):.9f}. This is a lower bound, not an exact optimum.",
        "", "| Midpoints per coordinate | Discrete D1 | Continuous D1 lower | Continuous D1 upper |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for row in fixed["midpoint_checks"]:
        lines.append(f"| {row['midpoints_per_coordinate']} | {row['grid_d1']:.9f} | "
                     f"{row['continuous_d1_lower']:.9f} | {row['continuous_d1_upper']:.9f} |")
    lines.extend([
        "", "Each row uses three independent membership/offer primal LPs and three existing "
        "dual LPs; all nine comparisons agree to 1e-9. The intervals use the proved "
        "midpoint coupling error 2*epsilon/order, intersected with analytical bounds; "
        "they are deterministic enclosures, not confidence intervals.", "",
        "Adaptive two-dimensional quadrature agrees with E|U1+(2/3)U3| = 31/54 "
        "to 1e-12. Exact scalar coalition costs agree with each discrete grid. "
        "Forecast-derived shares and the grand offer agree with the specified rule; "
        "individual forecast means also equal the true means.", "",
        "Reproduce: python scripts/check_exclusion_robustness.py. Source hashes and "
        "unrounded outputs are in [robustness.json](robustness.json). "
        "These checks do not establish the general proofs, originality or publication readiness.", "",
    ])
    target.with_suffix(".md").write_text("\n".join(lines))
    print(f"Passed {len(general)} regularization checks and 9 primal/dual comparisons "
          f"(18 LP solves); continuous gap/A lower bound = {float(F(fixed['gap_over_maximum_lower'])):.9f}.")


if __name__ == "__main__":
    main()
