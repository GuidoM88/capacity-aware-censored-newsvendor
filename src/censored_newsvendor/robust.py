"""A finite-scenario minimax-regret reference, not a full ambiguity-set solver."""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from .allocation import _vector, cost_gradient, solve_allocation, total_cost


@dataclass(frozen=True)
class ScenarioSolution:
    quantities: np.ndarray
    worst_regret: float
    scenario_regrets: np.ndarray
    oracle_costs: np.ndarray
    solver_iterations: int


def solve_finite_scenario_regret(
    scenarios, capacity, underage=4.0, overage=1.0, resource_weights=1.0,
):
    """Solve a convex epigraph problem for an explicitly supplied finite family.

    Each scenario must contain continuous PiecewiseUniform marginals. Every
    scenario has its own oracle under the same resource constraint. The family
    is assumed supplied by the experiment; it is not learned from censored data.
    """
    if not scenarios:
        raise ValueError("At least one scenario is required.")
    n = len(scenarios[0])
    if any(len(s) != n for s in scenarios):
        raise ValueError("All scenarios must have the same number of products.")
    if any(d.atom_mass != 0 for s in scenarios for d in s):
        raise ValueError("The smooth epigraph solver requires marginals without atoms.")
    a = _vector(resource_weights, n, "resource_weights")
    b, h = _vector(underage, n, "underage"), _vector(overage, n, "overage")
    oracles = [solve_allocation(s, capacity, b, h, a) for s in scenarios]
    oracle_costs = np.array([o.expected_cost for o in oracles])

    def regrets(q):
        return np.array([total_cost(s, q, b, h) - c for s, c in zip(scenarios, oracle_costs)])

    if capacity == 0:
        return ScenarioSolution(np.zeros(n), 0.0, np.zeros(len(scenarios)), oracle_costs, 0)

    q0 = np.mean([o.quantities for o in oracles], axis=0)
    x0 = np.r_[q0, max(0.0, float(np.max(regrets(q0))))]
    constraints = [
        {"type": "ineq", "fun": lambda x: capacity - a @ x[:-1], "jac": lambda x: np.r_[-a, 0.0]},
        {
            "type": "ineq",
            "fun": lambda x: x[-1] - regrets(x[:-1]),
            "jac": lambda x: np.array([
                np.r_[-cost_gradient(s, x[:-1], b, h), 1.0] for s in scenarios
            ]),
        },
    ]
    fit = minimize(
        lambda x: x[-1], x0, jac=lambda x: np.r_[np.zeros(n), 1.0],
        bounds=[(0.0, capacity / ai) for ai in a] + [(0.0, None)],
        constraints=constraints, method="SLSQP", options={"ftol": 1e-11, "maxiter": 1000},
    )
    q = fit.x[:-1]
    values = regrets(q)
    if not fit.success or a @ q > capacity + 1e-7 or np.max(values) > fit.x[-1] + 1e-7:
        raise RuntimeError(f"Finite-scenario optimization failed: {fit.message}")
    if np.min(values) < -1e-7:
        raise RuntimeError("Negative regret indicates an inconsistent oracle.")
    values = np.maximum(values, 0)
    return ScenarioSolution(q, float(np.max(values)), values, oracle_costs, int(fit.nit))
