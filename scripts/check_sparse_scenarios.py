"""Falsification checks for the sparse-tail theorem; not a novelty certificate.

Compare every endpoint world against the proposed rank-bounded subset, using
direct expected losses and exact piecewise-linear epigraph LPs. No production
solver is called. Run from the repository root.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linprog

from check_population_reduction import cost, oracle, supporting_lines


SEED = 2026102602
TOLERANCE = 1e-7


def coordinate_bounds(matrix, capacity):
    ratios = np.full_like(matrix, np.inf, dtype=float)
    np.divide(capacity[:, None], matrix, out=ratios, where=matrix > 0)
    upper = ratios.min(axis=0)
    if not np.isfinite(upper).all():
        raise ValueError("The packing region must be bounded")
    return upper


def packing_oracle(world, b, h, matrix, capacity):
    n = len(world)
    rows = [np.r_[row, np.zeros(n)] for row in matrix]
    rhs = list(capacity)
    for i, marginal in enumerate(world):
        for slope, intercept in supporting_lines(marginal, b[i], h[i]):
            row = np.zeros(2 * n)
            row[i], row[n + i] = slope, -1
            rows.append(row)
            rhs.append(-intercept)
    result = linprog(
        np.r_[np.zeros(n), np.ones(n)], A_ub=rows, b_ub=rhs,
        bounds=[(0, u) for u in coordinate_bounds(matrix, capacity)]
        + [(None, None)] * n, method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    q = result.x[:n]
    actual = cost(q, world, b, h)
    if abs(actual - result.fun) > TOLERANCE:
        raise AssertionError("Oracle LP disagrees with direct expected cost")
    if np.max(matrix @ q - capacity) > TOLERANCE:
        raise AssertionError("Oracle is infeasible")
    return q, actual


def packing_minimax(worlds, values, b, h, matrix, capacity):
    n, count = len(b), len(worlds)
    dim = n + count * n + 1
    rows, rhs = [], []
    for resource, limit in zip(matrix, capacity):
        row = np.zeros(dim)
        row[:n] = resource
        rows.append(row)
        rhs.append(limit)
    for j, world in enumerate(worlds):
        for i, marginal in enumerate(world):
            for slope, intercept in supporting_lines(marginal, b[i], h[i]):
                row = np.zeros(dim)
                row[i], row[n + j * n + i] = slope, -1
                rows.append(row)
                rhs.append(-intercept)
        row = np.zeros(dim)
        row[n + j * n:n + (j + 1) * n], row[-1] = 1, -1
        rows.append(row)
        rhs.append(values[j])
    objective = np.zeros(dim)
    objective[-1] = 1
    result = linprog(
        objective, A_ub=rows, b_ub=rhs,
        bounds=[(0, u) for u in coordinate_bounds(matrix, capacity)]
        + [(None, None)] * (count * n) + [(0, None)], method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    q = result.x[:n]
    actual = worst_regret(q, worlds, values, b, h)
    if abs(actual - result.fun) > TOLERANCE:
        raise AssertionError("Minimax LP disagrees with direct regret")
    if np.max(matrix @ q - capacity) > TOLERANCE:
        raise AssertionError("Minimax decision is infeasible")
    return q, actual


def worst_regret(q, worlds, values, b, h):
    return max(cost(q, world, b, h) - value
               for world, value in zip(worlds, values))


def shared_epigraph_minimax(lower_world, upper_world, masks, values,
                           b, h, matrix, capacity):
    """Compact LP: only two cost epigraphs per product, shared by all scenarios."""
    n = len(b)
    dim = 3 * n + 1
    rows, rhs = [], []
    for resource, limit in zip(matrix, capacity):
        row = np.zeros(dim)
        row[:n] = resource
        rows.append(row)
        rhs.append(limit)
    for endpoint, world in enumerate([lower_world, upper_world]):
        for i, marginal in enumerate(world):
            for slope, intercept in supporting_lines(marginal, b[i], h[i]):
                row = np.zeros(dim)
                row[i], row[n + endpoint * n + i] = slope, -1
                rows.append(row)
                rhs.append(-intercept)
    for mask, value in zip(masks, values):
        row = np.zeros(dim)
        for i, endpoint in enumerate(mask):
            row[n + endpoint * n + i] = 1
        row[-1] = -1
        rows.append(row)
        rhs.append(value)
    objective = np.zeros(dim)
    objective[-1] = 1
    result = linprog(
        objective, A_ub=rows, b_ub=rhs,
        bounds=[(0, u) for u in coordinate_bounds(matrix, capacity)]
        + [(None, None)] * (2 * n) + [(0, None)], method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    q = result.x[:n]
    worlds = [tuple((upper_world if mask[i] else lower_world)[i]
                    for i in range(n)) for mask in masks]
    actual = worst_regret(q, worlds, values, b, h)
    if abs(actual - result.fun) > TOLERANCE:
        raise AssertionError("Shared epigraph LP disagrees with direct regret")
    if np.max(matrix @ q - capacity) > TOLERANCE:
        raise AssertionError("Shared epigraph decision is infeasible")
    return q, actual


def scenarios(c, upper, probabilities):
    n = len(c)
    masks = list(itertools.product([0, 1], repeat=n))
    worlds = [tuple((np.array([0, c[i] / 2, upper[i] if mask[i] else c[i]]),
                     probabilities[i].copy()) for i in range(n))
              for mask in masks]
    return masks, worlds


def random_checks():
    rng = np.random.default_rng(SEED)
    records = []
    designs = (["one_resource"] * 12 + ["two_resources"] * 8
               + ["three_resources"] * 6 + ["redundant_rows"] * 4
               + ["individual_caps"] * 3)
    for case, design in enumerate(designs):
        n = 3 + case % 4
        rank = {"one_resource": 1, "two_resources": 2,
                "three_resources": 3, "redundant_rows": 1,
                "individual_caps": n}[design]
        if design == "individual_caps":
            matrix = np.eye(n)
        else:
            # Small positive integer matrices, rejecting exact rank deficiency;
            # the stored matrices make the tested ranks independently checkable.
            while True:
                matrix = rng.integers(1, 6, (rank, n)).astype(float)
                if np.linalg.matrix_rank(matrix) == rank:
                    break
        c = rng.integers(1, 6, n).astype(float)
        b = rng.integers(1, 8, n).astype(float)
        h = rng.integers(1, 5, n).astype(float)
        ratio = [0.0, 0.4, 0.9, 1.3, 2.0, 3.0][case % 6]
        capacity = (matrix @ c) * ratio * rng.uniform(0.8, 1.2, rank)
        if design == "redundant_rows":
            matrix = np.vstack([matrix, 2 * matrix, 3 * matrix])
            capacity = np.r_[capacity, 2 * capacity, 3 * capacity]
        upper = np.maximum(c, coordinate_bounds(matrix, capacity)) + 1
        probabilities = [rng.dirichlet([1, 2, 4]) for _ in range(n)]
        if case % 5 == 0:
            probabilities[0] = np.array([0.4, 0.6, 0.0])  # no hidden mass
        if case % 5 == 1:
            probabilities[0] = np.array([0.0, 0.0, 1.0])  # all censored
        if case % 5 == 2:
            p = h[0] / (b[0] + h[0])  # exactly zero upper-tail slope
            probabilities[0] = np.array([(1 - p) / 2, (1 - p) / 2, p])
        masks, worlds = scenarios(c, upper, probabilities)
        values = [packing_oracle(w, b, h, matrix, capacity)[1] for w in worlds]
        selected = [j for j, mask in enumerate(masks) if sum(mask) <= rank]
        sparse_worlds = [worlds[j] for j in selected]
        sparse_values = [values[j] for j in selected]
        q_full, value_full = packing_minimax(worlds, values, b, h, matrix, capacity)
        q_sparse, value_sparse = packing_minimax(
            sparse_worlds, sparse_values, b, h, matrix, capacity)
        q_compact, value_compact = shared_epigraph_minimax(
            worlds[0], worlds[-1], [masks[j] for j in selected], sparse_values,
            b, h, matrix, capacity)
        # Check the sparse optimizer against ALL worlds, including ties in the LP.
        sparse_actual = worst_regret(q_sparse, worlds, values, b, h)
        compact_actual = worst_regret(q_compact, worlds, values, b, h)
        errors = [abs(value_full - value_sparse), abs(sparse_actual - value_sparse),
                  abs(value_full - value_compact), abs(compact_actual - value_compact)]
        actions = [np.zeros(n), q_full, q_sparse, q_compact]
        for _ in range(20):
            direction = rng.uniform(0.01, 1, n)
            scale = float(np.min(capacity / (matrix @ direction)))
            actions.append(direction * scale * rng.uniform(0, 1))
        for q in actions:
            errors.append(abs(worst_regret(q, worlds, values, b, h)
                              - worst_regret(q, sparse_worlds, sparse_values, b, h)))
        crosscheck = 0.0
        if rank == 1:
            # Separate pre-existing resource-oracle implementation.
            crosscheck = max(abs(v - oracle(w, b, h, matrix[0], capacity[0])[1])
                             for w, v in zip(worlds, values))
            errors.append(crosscheck)
        if max(errors) > TOLERANCE:
            raise AssertionError((case, design, max(errors)))
        records.append({
            "case": case, "design": design, "products": n, "rank": rank,
            "resource_matrix": matrix.tolist(), "capacity": capacity.tolist(),
            "censoring_levels": c.tolist(), "upper_completion": upper.tolist(),
            "underage_costs": b.tolist(), "overage_costs": h.tolist(),
            "sales_probabilities": [p.tolist() for p in probabilities],
            "full_scenarios": len(worlds), "sparse_scenarios": len(selected),
            "checked_actions": len(actions), "minimax_full": value_full,
            "minimax_sparse": value_sparse, "sparse_action": q_sparse.tolist(),
            "full_regret_at_sparse_action": sparse_actual,
            "minimax_compact": value_compact, "compact_action": q_compact.tolist(),
            "full_regret_at_compact_action": compact_actual,
            "full_lp_variables": n + len(worlds) * n + 1,
            "compact_lp_variables": 3 * n + 1,
            "maximum_error": max(errors), "separate_oracle_error": crosscheck,
        })
    return records


def cap_counterexample():
    # Three independently capped products: treating this as one resource fails.
    n = 3
    c = b = h = np.ones(n)
    matrix, capacity = np.eye(n), np.full(n, 2.0)
    masks, worlds = scenarios(c, np.full(n, 3.0), [np.array([0., 0., 1.])] * n)
    values = [packing_oracle(w, b, h, matrix, capacity)[1] for w in worlds]
    selected = [j for j, mask in enumerate(masks) if sum(mask) <= 1]
    _, correct_value = packing_minimax(worlds, values, b, h, matrix, capacity)
    wrong_q, wrong_value = packing_minimax(
        [worlds[j] for j in selected], [values[j] for j in selected],
        b, h, matrix, capacity)
    full_regret = worst_regret(wrong_q, worlds, values, b, h)
    assert abs(correct_value - 1.5) < TOLERANCE
    assert abs(wrong_value - 1.0) < TOLERANCE
    assert abs(full_regret - 3.0) < TOLERANCE
    return {"products": n, "rank": n, "correct_minimax": correct_value,
            "incorrect_one_upper_minimax": wrong_value,
            "incorrect_action": wrong_q.tolist(), "actual_regret": full_regret,
            "interpretation": "Individual caps count as resource constraints."}


def main():
    records = random_checks()
    counterexample = cap_counterexample()
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), Path(__file__).with_name("check_population_reduction.py")]
    report = {
        "seed": SEED, "tolerance": TOLERANCE,
        "purpose": "Exploratory falsification of a population theorem; not a novelty or finite-sample claim.",
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__},
        "source_sha256": {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
        "cases": records, "cap_counterexample": counterexample,
        "summary": {"cases": len(records),
                    "checked_actions": sum(r["checked_actions"] for r in records),
                    "maximum_error": max(r["maximum_error"] for r in records)},
    }
    destination = root / "results/audit/sparse_scenarios.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n")
    # Generate the human-readable record from the same saved outcomes.
    summary = ["# Sparse-scenario check results", "",
               "Exploratory synthetic population checks; not proof of novelty.", "",
               f"Seed: `{SEED}`. Tolerance: `{TOLERANCE}`.", "",
               f"Cases: **{len(records)}**. Decisions checked: "
               f"**{report['summary']['checked_actions']}**. "
               f"Maximum discrepancy: **{report['summary']['maximum_error']:.3e}**.", "",
               "All endpoint worlds, the rank-bounded subset, and the compact shared",
               "epigraph LP agree within tolerance on these cases. Both reduced",
               "optimizers are also evaluated against every endpoint world.", "",
               "| Case | Design | n | Rank | Full worlds | Selected worlds | Minimax | Max error |",
               "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in records:
        summary.append(f"| {r['case']} | {r['design']} | {r['products']} | {r['rank']} | "
                       f"{r['full_scenarios']} | {r['sparse_scenarios']} | "
                       f"{r['minimax_full']:.8f} | {r['maximum_error']:.3e} |")
    summary.extend(["", "## Counterexample to ignoring individual caps", "",
                    f"Three independently capped products have true minimax regret "
                    f"**{counterexample['correct_minimax']:.1f}**. Incorrectly retaining "
                    f"only one-upper worlds gives **{counterexample['incorrect_one_upper_minimax']:.1f}** "
                    f"and a decision whose actual regret is **{counterexample['actual_regret']:.1f}**.",
                    "", "See [JSON](sparse_scenarios.json) for inputs, source hashes and versions."])
    destination.with_suffix(".md").write_text("\n".join(summary) + "\n")
    print(json.dumps(report["summary"]))
    print("PASS: the individual-cap counterexample is preserved in the report.")


if __name__ == "__main__":
    main()
