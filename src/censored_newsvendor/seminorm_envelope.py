"""Seminorm relaxation of the depth-one exclusion gap.

This is an exploratory oracle for structural envelopes such as C39. Under
symmetric absolute loss the optimized cost

    c(x) = min_q E|q - x'Y|

is a seminorm on signed membership vectors. Normalize the expected grand cost
of the implemented offer to L = 1 and write a = w for the charges. Every game
with standalone ratio rho >= r and integer excess B then satisfies

    c(e_j) <= a_j / r,   c(1) <= L,   c(1_S) >= a(S) - B  (proper S).

For a fixed membership z, ``minimal_cost`` returns the smallest value of c(z)
over *all* seminorms satisfying these constraints (gauge duality, see
docs/seminorm_envelope.md). Hence ``depth_one_envelope`` computes an upper
bound on the worst normalized depth-one gap over actual demand laws. Whether a
demand law realizes that bound is a separate question and is not checked here.

The maximization over z uses a grid and local refinement. Its value is a
feasible point of the relaxation, so strict gaps below a proved bound are
numerical observations, not certificates. Equality with a proved upper bound
does certify the relaxation's value.
"""

from __future__ import annotations

import itertools
from math import inf, sqrt

import numpy as np
from scipy.optimize import linprog, minimize, minimize_scalar


def proper_coalitions(n):
    """All nonempty proper coalitions of {0, ..., n-1}."""
    return [s for k in range(1, n) for s in itertools.combinations(range(n), k)]


def minimal_cost(z, shares, r, *, integer_excess=0.0, grand_cost=1.0,
                 pinned_singletons=False):
    """Smallest c(z) over seminorms obeying the depth-one game constraints.

    Constraints: c(e_j) <= a_j/r (none if r == 0), c(1) <= grand_cost and
    c(1_S) >= a(S) - integer_excess for every proper coalition S. With
    ``pinned_singletons`` the singleton costs are also bounded below by a_j/r,
    i.e. charges are proportional to standalone costs.

    Returns ``(value, coalition)``, where ``coalition`` attains the outer
    maximum. ``value`` is ``inf`` when no seminorm satisfies the constraints.
    """
    z = np.asarray(z, dtype=float)
    a = np.asarray(shares, dtype=float)
    n = len(a)
    if r < 0 or r > 1:
        raise ValueError("r must lie in [0, 1]")
    if pinned_singletons and r == 0:
        raise ValueError("pinned singletons need r > 0")
    caps = [(None, None)] * n if r == 0 else [(-x / r, x / r) for x in a]
    objective = np.zeros(n + 1)
    objective[-1] = 1.0
    base_rows = [np.r_[z, -1.0], np.r_[-z, -1.0],
                 np.r_[np.ones(n), 0.0], np.r_[-np.ones(n), 0.0]]
    base_rhs = [0.0, 0.0, grand_cost, grand_cost]
    best, argbest = 0.0, None
    for coalition in proper_coalitions(n):
        lower = a[list(coalition)].sum() - integer_excess
        if pinned_singletons and len(coalition) == 1:
            lower = max(lower, a[coalition[0]] / r)
        row = np.zeros(n + 1)
        row[list(coalition)] = -1.0
        result = linprog(objective, A_ub=np.array(base_rows + [row]),
                         b_ub=np.array(base_rhs + [-lower]),
                         bounds=caps + [(0, None)], method="highs")
        if result.status == 2:
            return inf, coalition
        if result.status != 0:
            raise RuntimeError(f"LP failed for {coalition}: {result.message}")
        if result.fun > best:
            best, argbest = float(result.fun), coalition
    return best, argbest


def face_gap(z, shares, r, **kwargs):
    """Relaxed normalized excess a'z - B - min c(z) at one membership."""
    excess = kwargs.get("integer_excess", 0.0)
    cost, _ = minimal_cost(z, shares, r, **kwargs)
    return float(np.dot(shares, z)) - excess - cost


def _orientations(n, symmetric):
    if symmetric:
        return [(n - 1, 0, list(range(1, n - 1)))]
    out = []
    for excluded in range(n):
        free = [j for j in range(n) if j != excluded]
        for unit in free:
            out.append((excluded, unit, [j for j in free if j != unit]))
    return out


def depth_one_envelope(shares, r, *, step=0.01, symmetric=None, starts=3, **kwargs):
    """Best relaxed depth-one gap found over all one-exclusion faces.

    By positive homogeneity a positive maximizer can be scaled until one free
    coordinate equals one, so each face is searched with a unit coordinate and
    the remaining free coordinates in [0, 1]. With equal shares the search uses
    the permutation symmetry. Returns a dictionary with the value (clipped at
    zero, the value of the empty membership), the membership and the face.
    """
    shares = np.asarray(shares, dtype=float)
    n = len(shares)
    if symmetric is None:
        symmetric = bool(np.allclose(shares, shares[0]))
    grid = np.arange(0.0, 1.0 + 1e-12, step)
    candidates = []
    for excluded, unit, others in _orientations(n, symmetric):
        def membership(t, unit=unit, others=others):
            z = np.zeros(n)
            z[unit] = 1.0
            z[others] = np.clip(t, 0.0, 1.0)
            return z

        for t in itertools.product(grid, repeat=len(others)):
            if symmetric and list(t) != sorted(t, reverse=True):
                continue
            value = face_gap(membership(np.array(t)), shares, r, **kwargs)
            candidates.append((value, np.array(t), membership, excluded))
    candidates.sort(key=lambda item: item[0], reverse=True)
    if not np.isfinite(candidates[0][0]):
        return {"value": None, "membership": None, "excluded": None,
                "grid_points": len(candidates)}
    best_value, best_z, best_face = -inf, None, None
    for value, t, membership, excluded in candidates[:starts]:
        if len(t) == 1:
            result = minimize_scalar(
                lambda s: -face_gap(membership(np.array([s])), shares, r, **kwargs),
                bounds=(max(0.0, t[0] - step), min(1.0, t[0] + step)),
                method="bounded", options={"xatol": 1e-10})
            refined, t_ref = -result.fun, np.array([result.x])
        else:
            result = minimize(
                lambda s: -face_gap(membership(s), shares, r, **kwargs), t,
                method="Nelder-Mead",
                options={"xatol": 1e-9, "fatol": 1e-11, "maxiter": 2000})
            refined, t_ref = -result.fun, np.clip(result.x, 0.0, 1.0)
        if value >= refined:
            refined, t_ref = value, t
        if refined > best_value:
            best_value, best_z, best_face = refined, membership(t_ref), excluded
    return {"value": float(max(0.0, best_value)), "membership": best_z.tolist(),
            "excluded": best_face, "grid_points": len(candidates)}


def max_min_lines(lines):
    """max over t in [0, 1] of min_k (c_k + s_k t) for lines (c_k, s_k)."""
    points = {0.0, 1.0}
    for (c1, s1), (c2, s2) in itertools.combinations(lines, 2):
        if s1 != s2:
            t = (c2 - c1) / (s1 - s2)
            if 0.0 <= t <= 1.0:
                points.add(t)
    return max(min(c + s * t for c, s in lines) for t in points)


def c39_envelope(r):
    """Proved C39 envelope for three equal shares."""
    return 2 * (1 - r) / 3 if r <= 1 / 3 else (1 - r * r) / (6 * r)


def c31_ceiling(shares, r):
    """Depth-one C31 ceiling (1-r) s_1(w) with s_1(w) = 1 - min w."""
    return (1 - r) * (float(np.sum(shares)) - float(np.min(shares)))


def separable_bound(n, r):
    """Proved depth-one upper bound for n equal shares (Proposition 2)."""
    if r <= (n - 2) / n:
        return (1 - r) * (n - 1) / n
    return (n - 2) * (1 - r * r) / (2 * n * r)


def three_player_bound(shares, r, *, fourth=True):
    """Face-inequality bound for three players and arbitrary shares.

    With ``fourth=False`` only the three inequalities of the C39 proof are
    used; with ``fourth=True`` the standalone cap of the integral coordinate
    is added (Proposition 3).
    """
    a = [float(x) for x in shares]
    if len(a) != 3:
        raise ValueError("three players only")
    if r == 0:
        return 1.0 - min(a)
    best = 0.0
    for i, j in itertools.permutations(range(3), 2):
        lines = [(a[i], a[j]),                       # nonnegative cost
                 (0.0, a[j] * (1 + 1 / r)),          # singleton i lower bound
                 (a[j] * (1 / r - 1), -a[j] * (1 / r - 1))]  # pair {i,j}
        if fourth:
            lines.append((a[i] * (1 + 1 / r), -a[i] * (1 + 1 / r)))
        best = max(best, max_min_lines(lines))
    return best


def proportional_three_player_bound(r, grand_cost=1.0):
    """Proved bound for three equal shares and equal pinned standalone costs."""
    a, m, ell = 1 / 3, (1 / 3) / r, grand_cost
    lines = [(a, a), (a - m, a + m), (m - a, a - m), (a + ell, a - m)]
    return max(0.0, max_min_lines(lines))


def proportional_three_player_closed_form(r):
    """Closed form of ``proportional_three_player_bound`` for L = 1."""
    if r >= 1 / 5:
        return (1 - r) / 3
    return max(0.0, (1 + r) / 2 - (1 - 3 * r) / (6 * r))


PROPORTIONAL_ZERO_THRESHOLD = (2 * sqrt(3) - 3) / 3


def configuration_prediction(n, r):
    """Heuristic regime label for n equal shares (not a theorem).

    'high' : r >= (n-2)/n, where the separable bound is expected to be sharp.
    'c31'  : some configuration with p unit and q = n-1-p fractional
             coordinates passes its necessary conditions
             (q-p)/(q+p) <= r <= q/(q+2p). Closed intervals: at an endpoint
             a window below C31 has zero depth (first seen at n=4, r=1/5).
    'below': no such configuration; the C31 value is not expected.
    """
    if r >= (n - 2) / n:
        return "high"
    for p in range(1, n - 1):
        q = n - 1 - p
        if (q - p) / (q + p) <= r <= q / (q + 2 * p):
            return "c31"
    return "below"
