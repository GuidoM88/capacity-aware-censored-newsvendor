"""Separable convex allocation using the shared capacity multiplier."""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq

from .distributions import PiecewiseUniform


@dataclass(frozen=True)
class Allocation:
    quantities: np.ndarray
    multiplier: float
    expected_cost: float
    capacity_used: float
    kkt_residual: float


def _vector(value, n, name):
    array = np.broadcast_to(np.asarray(value, dtype=float), (n,)).copy()
    if not np.all(np.isfinite(array)) or np.any(array <= 0):
        raise ValueError(f"{name} must be finite and strictly positive.")
    return array


def total_cost(distributions, quantities, underage=4.0, overage=1.0):
    n = len(distributions)
    q = np.asarray(quantities, dtype=float)
    if q.shape != (n,):
        raise ValueError("One quantity is required per product.")
    b, h = _vector(underage, n, "underage"), _vector(overage, n, "overage")
    return float(sum(d.expected_cost(x, bi, hi) for d, x, bi, hi in zip(distributions, q, b, h)))


def cost_gradient(distributions, quantities, underage, overage):
    """Right derivative; a gradient when no marginal has an atom at q."""
    n = len(distributions)
    b, h = _vector(underage, n, "underage"), _vector(overage, n, "overage")
    return np.array([(bi + hi) * d.cdf(q) - bi for d, q, bi, hi in zip(distributions, quantities, b, h)])


def solve_allocation(
    distributions: tuple[PiecewiseUniform, ...] | list[PiecewiseUniform],
    capacity: float,
    underage=4.0,
    overage=1.0,
    resource_weights=1.0,
) -> Allocation:
    """Minimize expected loss subject to q >= 0 and a @ q <= capacity.

    This is an oracle for the *supplied* marginals. Passing censored sales
    distributions implements the sales-as-demand population baseline. It is
    not an estimator of the latent demand distribution.
    """
    n = len(distributions)
    if n == 0 or not all(isinstance(d, PiecewiseUniform) for d in distributions):
        raise ValueError("At least one PiecewiseUniform marginal is required.")
    if not np.isfinite(capacity) or capacity < 0:
        raise ValueError("Capacity must be finite and nonnegative.")
    b = _vector(underage, n, "underage")
    h = _vector(overage, n, "overage")
    a = _vector(resource_weights, n, "resource_weights")

    def quantities(multiplier):
        probabilities = np.clip((b - multiplier * a) / (b + h), 0, 1)
        return np.array([d.ppf(p) for d, p in zip(distributions, probabilities)])

    independent = quantities(0.0)
    if capacity == 0:
        multiplier = float(np.max(b / a))
        q = np.zeros(n)
    elif a @ independent <= capacity:
        multiplier, q = 0.0, independent
    else:
        multiplier = brentq(
            lambda lam: float(a @ quantities(lam) - capacity),
            0.0,
            float(np.max(b / a)),
            xtol=1e-13,
            rtol=1e-14,
        )
        q = quantities(multiplier)

    lo = np.array([(bi + hi) * d.cdf_left(qi) - bi for d, qi, bi, hi in zip(distributions, q, b, h)])
    hi = cost_gradient(distributions, q, b, h)
    stationarity = np.maximum.reduce([lo + multiplier * a, -hi - multiplier * a, np.zeros(n)])
    at_zero = q <= 1e-12
    stationarity[at_zero] = np.maximum(0.0, -(hi + multiplier * a)[at_zero])
    used = float(a @ q)
    residual = float(max(
        np.max(stationarity), max(0.0, used - capacity),
        abs(multiplier * (used - capacity)),
    ))
    if residual > 1e-7:
        raise RuntimeError(f"Allocation failed the KKT check: residual={residual:g}")
    return Allocation(q, float(multiplier), total_cost(distributions, q, b, h), used, residual)
