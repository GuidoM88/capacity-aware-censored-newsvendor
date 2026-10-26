"""Independent numerical checks of the population reductions, not theorem proofs."""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import linprog


TOLERANCE = 1e-7
SEED = 20261026


def loss(q, marginal, b, h):
    support, probabilities = marginal
    return float(np.dot(probabilities, b * np.maximum(support - q, 0)
                        + h * np.maximum(q - support, 0)))


def cost(q, world, b, h):
    return sum(loss(q[i], marginal, b[i], h[i])
               for i, marginal in enumerate(world))


def supporting_lines(marginal, b, h):
    support, probabilities = marginal
    lines = []
    for knot in np.unique(np.r_[0.0, support]):
        slope = (b + h) * probabilities[support <= knot].sum() - b
        lines.append((slope, loss(knot, marginal, b, h) - slope * knot))
    return lines


def oracle(world, b, h, a, capacity, caps=None):
    n = len(world)
    upper = capacity / a
    if caps is not None:
        upper = np.minimum(upper, caps)
    rows, rhs = [np.r_[a, np.zeros(n)]], [capacity]
    for i, marginal in enumerate(world):
        for slope, intercept in supporting_lines(marginal, b[i], h[i]):
            row = np.zeros(2 * n)
            row[i], row[n + i] = slope, -1
            rows.append(row)
            rhs.append(-intercept)
    result = linprog(np.r_[np.zeros(n), np.ones(n)], A_ub=rows, b_ub=rhs,
                     bounds=[(0, value) for value in upper] + [(None, None)] * n,
                     method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    q = result.x[:n]
    actual = cost(q, world, b, h)
    if abs(actual - result.fun) > TOLERANCE:
        raise AssertionError("Oracle epigraph disagrees with direct expected loss")
    return q, actual


def minimax(worlds, b, h, a, capacity):
    n, m = len(a), len(worlds)
    dim = n + m * n + 1
    values = [oracle(w, b, h, a, capacity)[1] for w in worlds]
    row = np.zeros(dim)
    row[:n] = a
    rows, rhs = [row], [capacity]
    for w, world in enumerate(worlds):
        for i, marginal in enumerate(world):
            index = n + w * n + i
            for slope, intercept in supporting_lines(marginal, b[i], h[i]):
                row = np.zeros(dim)
                row[i], row[index] = slope, -1
                rows.append(row)
                rhs.append(-intercept)
        row = np.zeros(dim)
        row[n + w * n:n + (w + 1) * n], row[-1] = 1, -1
        rows.append(row)
        rhs.append(values[w])
    objective = np.zeros(dim)
    objective[-1] = 1
    bounds = ([(0, value) for value in capacity / a]
              + [(None, None)] * (m * n) + [(0, None)])
    result = linprog(objective, A_ub=rows, b_ub=rhs, bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    q = result.x[:n]
    actual = max(cost(q, w, b, h) - v for w, v in zip(worlds, values))
    if abs(actual - result.fun) > TOLERANCE or np.dot(a, q) > capacity + TOLERANCE:
        raise AssertionError("Minimax epigraph disagrees with direct regret")
    return q, actual, values


def atomic_checks():
    rng = np.random.default_rng(SEED)
    records = []
    for case in range(24):
        n = 1 + case % 3
        c = rng.integers(2, 7, n).astype(float)
        a = rng.integers(1, 4, n).astype(float)
        b = rng.integers(1, 7, n).astype(float)
        h = rng.integers(1, 5, n).astype(float)
        ratio = [0.0, 0.3, 0.8, 1.0, 1.4, 2.2][case // 4]
        capacity = float(ratio * np.dot(a, c))
        upper = np.maximum(c, capacity / a) + 1
        marginal_options = []
        for i in range(n):
            probabilities = rng.dirichlet([2, 2, 3])
            if case % 7 == 0 and i == 0:
                probabilities[-1] = 0
                probabilities /= probabilities.sum()
            middle = c[i] + 0.3 * (upper[i] - c[i])
            options = [(np.array([0, c[i] / 2, tail]), probabilities.copy())
                       for tail in [c[i], middle, upper[i]]]
            mixture = (np.array([0, c[i] / 2, c[i], middle, upper[i]]),
                       np.r_[probabilities[:2], probabilities[-1]
                             * np.array([0.2, 0.5, 0.3])])
            options.append(mixture)
            marginal_options.append(options)
        endpoints = [tuple(marginal_options[i][e[i]] for i in range(n))
                     for e in itertools.product([0, 2], repeat=n)]
        expanded = [tuple(marginal_options[i][e[i]] for i in range(n))
                    for e in itertools.product(range(4), repeat=n)]
        upper_world = tuple(options[2] for options in marginal_options)
        _, upper_value = oracle(upper_world, b, h, a, capacity)
        candidate, capped_value = oracle(upper_world, b, h, a, capacity, c)
        gap = capped_value - upper_value
        q, endpoint_value, _ = minimax(endpoints, b, h, a, capacity)
        _, expanded_value, expanded_oracles = minimax(expanded, b, h, a, capacity)
        if abs(endpoint_value - expanded_value) > TOLERANCE:
            raise AssertionError("Interior tails changed the minimax value")
        common = gap <= TOLERANCE
        if common != (expanded_value <= TOLERANCE):
            raise AssertionError("Common-action characterization disagrees")
        candidate_regret = max(cost(candidate, w, b, h) - value
                               for w, value in zip(expanded, expanded_oracles))
        if common and candidate_regret > TOLERANCE:
            raise AssertionError("Certificate failed on an interior-tail completion")
        # Check equality of the two worst-case regret functions away from optima.
        action_error = 0.0
        endpoint_oracles = [oracle(w, b, h, a, capacity)[1] for w in endpoints]
        for _ in range(5):
            fractions = rng.dirichlet(np.ones(n + 1))[:n]
            action = capacity * fractions / a
            worst_endpoint = max(cost(action, w, b, h) - v
                                 for w, v in zip(endpoints, endpoint_oracles))
            worst_expanded = max(cost(action, w, b, h) - v
                                 for w, v in zip(expanded, expanded_oracles))
            action_error = max(action_error, abs(worst_endpoint - worst_expanded))
        if action_error > TOLERANCE:
            raise AssertionError("Endpoint reduction failed at a held-out action")
        records.append({"case": case, "products": n, "stock": c.tolist(),
                        "weights": a.tolist(), "underage": b.tolist(),
                        "overage": h.tolist(), "capacity": capacity,
                        "endpoint_scenarios": len(endpoints),
                        "expanded_scenarios": len(expanded),
                        "common_action_exists": bool(common),
                        "certificate_gap": gap, "minimax_regret": endpoint_value,
                        "minimax_action": q.tolist(),
                        "expanded_value_error": abs(endpoint_value - expanded_value),
                        "action_regret_error": action_error})
    return records


def continuous_toy_checks():
    # Direct integration, independent of the production marginal implementation.
    def single(q, tail):
        kink = [q] if 0 < q < 40 else None
        prefix = quad(lambda d: (4 * max(d - q, 0) + max(q - d, 0)) / 100,
                      0, 40, points=kink, epsabs=1e-10)[0]
        return prefix + 0.6 * (4 * max(tail - q, 0) + max(q - tail, 0))

    worlds = list(itertools.product([40.0, 121.0], repeat=2))
    grid = np.array([(x, y) for x in range(121) for y in range(121 - x)])
    values = {tail: np.array([single(q, tail) for q in range(121)])
              for tail in [40.0, 121.0]}
    table = np.column_stack([values[x][grid[:, 0]] + values[y][grid[:, 1]]
                             for x, y in worlds])
    oracles = table.min(axis=0)
    regrets = table - oracles
    worst = regrets.max(axis=1)
    best = int(np.argmin(worst))
    expected_oracles = [(40, 40), (40, 80), (80, 40), (60, 60)]
    for j, q in enumerate(expected_oracles):
        expected_cost = sum(single(q[i], worlds[j][i]) for i in range(2))
        if abs(expected_cost - oracles[j]) > TOLERANCE:
            raise AssertionError("Analytical toy oracle disagrees with grid")
    at_60 = regrets[np.all(grid == [60, 60], axis=1)][0]
    at_40 = regrets[np.all(grid == [40, 40], axis=1)][0]
    if not np.allclose(at_60, [40, 60, 60, 0], atol=TOLERANCE, rtol=0):
        raise AssertionError("Full-class toy regrets disagree with formula")
    if abs(worst[best] - 60) > TOLERANCE or abs(at_40.max() - 80) > TOLERANCE:
        raise AssertionError("Full-class toy optimum disagrees with formula")
    s = 160 / 3
    restricted_regrets = np.array([single(s, x) + single(s, y)
                                   for x, y in worlds]) - oracles
    if not np.allclose(restricted_regrets, [80/3, 200/3, 200/3, 80/3],
                       atol=TOLERANCE, rtol=0):
        raise AssertionError("Mixed-endpoint counterexample failed")
    return {"capacity": 120, "upper_endpoint": 121,
            "integer_grid_actions": len(grid), "grid_minimax_action": grid[best].tolist(),
            "full_class_minimax_value": float(worst[best]),
            "regrets_at_60_60": at_60.tolist(),
            "sales_as_demand_worst_regret": float(at_40.max()),
            "all_low_all_high_only_value": float(restricted_regrets[[0, 3]].max()),
            "that_actions_full_class_regret": float(restricted_regrets.max())}


def main():
    atomic = atomic_checks()
    toy = continuous_toy_checks()
    report = {"scope": "Numerical checks; proofs are in docs/population_reduction.md",
              "seed": SEED, "tolerance": TOLERANCE,
              "python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "atomic_cases": atomic, "continuous_toy": toy}
    output = Path(__file__).resolve().parents[1] / "results/audit/population_reduction.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    common_count = sum(item["common_action_exists"] for item in atomic)
    print(f"PASS: {len(atomic)} atomic cases ({common_count} common-action cases), "
          f"120 additional actions, and {toy['integer_grid_actions']} toy grid actions.")
    print(f"Full-class toy minimax regret: {toy['full_class_minimax_value']:.8f}")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
