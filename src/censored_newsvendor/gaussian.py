"""Worst-case overstatement of fractional audits under Gaussian demand.

For Y ~ N(mu, Sigma) the optimal expected pinball loss of a membership x is
phi(Phi^{-1}(tau)) * sqrt(x' Sigma x): a Euclidean norm of x, symmetric in x
whatever the penalty ratio. All normalized quantities are therefore the same
for every kappa, and we may write c(x) = sqrt(x' G x) with G a scaled
covariance matrix. The game constraints are linear in G:

    standalone floor   G_jj <= (a_j / r)^2
    stability          1_S' G 1_S >= (a(S) - B)^2   for proper S with a(S) > B
    grand cost         1' G 1 <= L^2 (L = 1)
    optional           G_ij >= 0 (nonnegative correlations), or G diagonal.

So for a fixed membership z the least favourable Gaussian law minimizes
z' G z over a convex set: one semidefinite program, solved to global
optimality. The worst case is the maximum over memberships of a'z - B minus
that minimal cost; it is searched on a grid with local refinement, exactly as
for general laws (seminorm_envelope.relaxed_envelope). Every value returned
is attained by the Gaussian law with the returned G, up to solver tolerance.
"""

from __future__ import annotations

import itertools

import cvxpy as cp
import numpy as np
from scipy.optimize import minimize, minimize_scalar

from .seminorm_envelope import _orientations, proper_coalitions


class GaussianOracle:
    """Smallest Gaussian cost at a membership, for fixed shares, floor and structure."""

    def __init__(self, shares, r, *, integer_excess=0.0, grand_cost=1.0,
                 structure="any"):
        a = np.asarray(shares, dtype=float)
        n = len(a)
        self.n = n
        G = cp.Variable((n, n), symmetric=True)
        self.P = cp.Parameter((n, n), symmetric=True)
        constraints = [G >> 0, cp.sum(G) <= grand_cost ** 2]
        if r > 0:
            constraints += [G[j, j] <= (a[j] / r) ** 2 for j in range(n)]
        for s in proper_coalitions(n):
            need = a[list(s)].sum() - integer_excess
            if need > 0:
                idx = list(s)
                constraints.append(cp.sum(G[np.ix_(idx, idx)]) >= need ** 2)
        if structure == "nonnegative":
            constraints += [G[i, j] >= 0 for i in range(n) for j in range(i)]
        elif structure == "independent":
            constraints += [G[i, j] == 0 for i in range(n) for j in range(i)]
        elif structure != "any":
            raise ValueError("structure must be 'any', 'nonnegative' or 'independent'")
        self.G = G
        self.problem = cp.Problem(cp.Minimize(cp.trace(self.P @ G)), constraints)

    def cost(self, z):
        """(minimal sqrt(z'Gz), minimizing G) or (inf, None) if infeasible."""
        z = np.asarray(z, dtype=float)
        self.P.value = np.outer(z, z)
        try:
            self.problem.solve(solver=cp.CLARABEL)
        except cp.error.SolverError:
            self.problem.solve(solver=cp.SCS, eps=1e-9, max_iters=200000)
        if self.problem.status not in ("optimal", "optimal_inaccurate"):
            return np.inf, None
        return float(np.sqrt(max(self.problem.value, 0.0))), np.array(self.G.value)


def gaussian_envelope(shares, r, *, depth=1, step=0.05, structure="any", starts=4,
                      integer_excess=0.0, symmetric=None):
    """Worst overstatement (D_depth - B)/L over Gaussian laws with floor r.

    Same search as relaxed_envelope: every face of the given depth, a unit
    coordinate, the other free coordinates on a grid (sorted when shares are
    equal), then local refinement of the best grid points.
    """
    a = np.asarray(shares, dtype=float)
    n = len(a)
    if symmetric is None:
        symmetric = bool(np.allclose(a, a[0]))
    oracle = GaussianOracle(a, r, integer_excess=integer_excess, structure=structure)
    grid = np.arange(0.0, 1.0 + 1e-12, step)

    def gap(z):
        c, _ = oracle.cost(z)
        return float(a @ z) - integer_excess - c if np.isfinite(c) else -1e9

    candidates = []
    for excluded, unit, others in _orientations(n, symmetric, depth):
        def membership(t, unit=unit, others=others):
            z = np.zeros(n)
            z[unit] = 1.0
            z[others] = np.clip(t, 0.0, 1.0)
            return z

        for t in itertools.product(grid, repeat=len(others)):
            if symmetric and list(t) != sorted(t, reverse=True):
                continue
            candidates.append((gap(membership(np.array(t))), np.array(t), membership))
    candidates.sort(key=lambda item: item[0], reverse=True)
    best_value, best_z = -np.inf, None
    for value, t, membership in candidates[:starts]:
        if len(t) == 1:
            result = minimize_scalar(lambda s: -gap(membership(np.array([s]))),
                                     bounds=(max(0.0, t[0] - step), min(1.0, t[0] + step)),
                                     method="bounded", options={"xatol": 1e-9})
            refined, t_ref = -result.fun, np.array([result.x])
        elif len(t) > 1:
            result = minimize(lambda s: -gap(membership(s)), t, method="Nelder-Mead",
                              options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 600})
            refined, t_ref = -result.fun, np.clip(result.x, 0.0, 1.0)
        else:
            refined, t_ref = value, t
        if value >= refined:
            refined, t_ref = value, t
        if np.isfinite(refined) and refined > best_value:
            best_value, best_z = refined, membership(t_ref)
    if best_z is None or best_value <= -1e8:
        return {"value": None, "membership": None, "G": None, "cost": None}
    cost, G = oracle.cost(best_z)
    return {"value": float(max(0.0, best_value)), "membership": best_z.tolist(),
            "G": None if G is None else G.tolist(), "cost": cost}


def check_gaussian_law(G, shares, r, membership, *, integer_excess=0.0, tol=1e-6):
    """Slacks of every constraint for the cost sqrt(x'Gx) (floats)."""
    G = np.asarray(G, dtype=float)
    a = np.asarray(shares, dtype=float)
    n = len(a)
    c = lambda x: float(np.sqrt(max(np.asarray(x) @ G @ np.asarray(x), 0.0)))
    caps = min(a[j] / r - c(np.eye(n)[j]) for j in range(n))
    stability = min(c(np.isin(np.arange(n), s).astype(float)) - (a[list(s)].sum() - integer_excess)
                    for s in proper_coalitions(n))
    grand = 1.0 - c(np.ones(n))
    psd = float(np.linalg.eigvalsh((G + G.T) / 2).min())
    z = np.asarray(membership, dtype=float)
    return {"cap": caps, "stability": stability, "grand": grand, "psd": psd,
            "excess": float(a @ z) - integer_excess - c(z),
            "valid": min(caps, stability, grand, psd) >= -tol}
