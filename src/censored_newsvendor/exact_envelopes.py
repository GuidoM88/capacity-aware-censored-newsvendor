"""Explicit worst-case demand laws for the exclusion gap under a standalone floor.

Two families, both with symmetric absolute loss and normalized grand cost
L = 1, are constructed here and proved optimal in docs/exact_envelopes.md:

* equal shares, any n, depth one: the C31 ceiling (1-r)(n-1)/n on explicit
  intervals of r, and (n-2)(1-r^2)/(2nr) for r >= (n-2)/n;
* arbitrary positive shares, any n, the last nonterminal depth n-2: the
  four-inequality value (three regimes per ordered pair of free players).

Every law is a finite centrally symmetric law, described by zonotope
generators g: its optimized cost is c(x) = sum_g |g'x|. All arithmetic in
this module is exact (fractions); ``verify_generators`` checks every
coalition constraint directly.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

F = Fraction


def _vec(n, entries):
    v = [F(0)] * n
    for index, value in entries.items():
        v[index] = F(value)
    return tuple(v)


def zonotope_cost(generators, x):
    """c(x) = sum_g |g'x| for the law with these generators."""
    return sum(abs(sum(g_i * x_i for g_i, x_i in zip(g, x))) for g in generators)


# ---------------------------------------------------------------------------
# Equal shares, depth one
# ---------------------------------------------------------------------------

def configuration_intervals(n, depth=1):
    """Intervals I_p = [max(0,(q-p)/(q+p)), q/(q+2p)] with p + q = n - depth.

    p is the number of unit coordinates and q the number of fractional
    coordinates of the witness; p runs over 1..n-depth-1.
    """
    free = n - depth
    out = []
    for p in range(1, free):
        q = free - p
        out.append((p, max(F(0), F(q - p, q + p)), F(q, q + 2 * p)))
    return out


def high_threshold(n, depth=1):
    """(m-1)/(m+1) with m = n - depth free producers; (n-2)/n at depth one."""
    free = n - depth
    return F(free - 1, free + 1)


def windows(n, depth=1):
    """Open subintervals of [0, high threshold] covered by no configuration interval."""
    covered = sorted((lo, hi) for _, lo, hi in configuration_intervals(n, depth))
    gaps, reach = [], F(0)
    for lo, hi in covered:
        if lo > reach:
            gaps.append((reach, lo))
        reach = max(reach, hi)
    if reach < high_threshold(n, depth):
        gaps.append((reach, high_threshold(n, depth)))
    return gaps


def equal_share_value(n, r, depth=1):
    """Exact worst gap (D_depth-B)/L for n equal shares, or None in a window."""
    r = F(r)
    free = n - depth
    if r >= high_threshold(n, depth):
        return (free - 1) * (1 - r * r) / (2 * n * r)
    for _, lo, hi in configuration_intervals(n, depth):
        if lo <= r <= hi:
            return (1 - r) * free / n
    return None


def equal_share_construction(n, r, depth=1):
    """Generators, membership and value attaining the worst gap at this depth.

    Labels: unit coordinates 0..p-1, fractional coordinates p..m-1 with
    m = n - depth, excluded producers m..n-1. Returns None inside a window.
    """
    r = F(r)
    if not 0 < r <= 1:
        raise ValueError("0 < r <= 1 required")
    if not 1 <= depth <= n - 2:
        raise ValueError("depth must lie in 1..n-2")
    a, cap = F(1, n), F(1, n) / r
    free = n - depth
    excluded = [_vec(n, {k: a}) for k in range(free, n)]
    if r >= high_threshold(n, depth):
        q = free - 1
        delta = (cap - a) / 2
        beta = a - q * (cap - a) / 2
        t = (1 - r) / 2
        generators = [_vec(n, {0: beta})] + excluded
        generators += [_vec(n, {0: delta, j: -cap}) for j in range(1, free)]
        z = _vec(n, {0: 1, **{j: t for j in range(1, free)}})
        return {"regime": "high", "p": 1, "generators": generators, "membership": z,
                "value": q * (1 - r * r) / (2 * n * r)}
    for p, lo, hi in configuration_intervals(n, depth):
        if lo <= r <= hi:
            q = free - p
            t = (1 - r) - p * r / q
            unit = {i: cap * t / p for i in range(p)}
            generators = list(excluded)
            generators += [_vec(n, {**unit, j: -cap}) for j in range(p, free)]
            z = _vec(n, {**{i: 1 for i in range(p)}, **{j: t for j in range(p, free)}})
            return {"regime": "c31", "p": p, "generators": generators, "membership": z,
                    "value": (1 - r) * free / n}
    return None


# ---------------------------------------------------------------------------
# Any shares, last nonterminal depth n-2 (three players: depth one)
# ---------------------------------------------------------------------------

def pair_regime(a_i, a_j, r):
    """Regime, fractional membership t and value for unit i and fractional j."""
    a_i, a_j, r = F(a_i), F(a_j), F(r)
    x = a_i / a_j
    if x >= (1 - r) / (2 * r):
        t = (1 - r) / 2
        return "g2g3", t, a_j * (1 - r * r) / (2 * r)
    if x >= (1 - r) / (1 + r):
        t = (1 - r) - r * x
        return "g1g3", t, (1 - r) * (a_i + a_j)
    t = a_i / (r * a_j + (1 + r) * a_i)
    return "g1g4", t, a_i + t * a_j


def last_depth_value(shares, r):
    """Exact worst gap (D_{n-2}-B)/L for positive shares and 0 < r <= 1."""
    a = [F(x) for x in shares]
    return max(pair_regime(a[i], a[j], r)[2]
               for i, j in itertools.permutations(range(len(a)), 2))


def last_depth_construction(shares, r):
    """Generators, membership and value attaining the last-depth worst gap."""
    a = [F(x) for x in shares]
    r = F(r)
    n = len(a)
    best = max(((pair_regime(a[i], a[j], r), i, j)
                for i, j in itertools.permutations(range(n), 2)),
               key=lambda item: item[0][2])
    (regime, t, value), i, j = best
    m_i, m_j = a[i] / r, a[j] / r
    generators = [_vec(n, {k: a[k]}) for k in range(n) if k not in (i, j)]
    if regime == "g2g3":
        delta = (m_j - a[j]) / 2
        generators += [_vec(n, {i: a[i] - delta}), _vec(n, {i: delta, j: -m_j})]
    elif regime == "g1g3":
        generators += [_vec(n, {i: m_j * t, j: -m_j})]
    else:
        c_j = m_i / t
        generators += [_vec(n, {i: m_i, j: -c_j})]
    z = _vec(n, {i: 1, j: t})
    return {"regime": regime, "pair": (i, j), "generators": generators,
            "membership": z, "value": value}


# ---------------------------------------------------------------------------
# Exact verification
# ---------------------------------------------------------------------------

def verify_generators(generators, shares, r, membership, value):
    """Check every constraint of the extremal problem in exact arithmetic.

    Returns a dictionary of the minimal slacks. All must be >= 0 and the
    witness slack must be 0 for the law to attain ``value``:
      cap:        a_j/r - c(e_j)            (standalone floor rho >= r)
      stability:  c(1_S) - a(S)             (every proper S, so B = 0)
      grand:      1 - c(1)                  (L = 1 is feasible)
      witness:    a'z - c(z) - value        (the face membership)
    """
    a = [F(x) for x in shares]
    r = F(r)
    n = len(a)
    unit = [_vec(n, {j: 1}) for j in range(n)]
    cap = min(a[j] / r - zonotope_cost(generators, unit[j]) for j in range(n))
    stability = min(
        zonotope_cost(generators, _vec(n, {j: 1 for j in s})) - sum(a[j] for j in s)
        for size in range(1, n) for s in itertools.combinations(range(n), size))
    grand = 1 - zonotope_cost(generators, _vec(n, {j: 1 for j in range(n)}))
    witness = (sum(x * y for x, y in zip(a, membership))
               - zonotope_cost(generators, membership) - value)
    rho = min(a[j] / zonotope_cost(generators, unit[j]) for j in range(n))
    return {"cap": cap, "stability": stability, "grand": grand, "witness": witness,
            "rho": min(F(1), rho)}


def four_line_bound(shares, r):
    """Proved last-depth upper bound computed numerically from the four lines.

    For each ordered pair (i unit, j fractional) take the best point of the
    lower envelope of a_i + t a_j, t a_j (1+1/r), (1-t) a_j (1/r-1) and
    (1-t) a_i (1+1/r) on [0, 1]; maximize over pairs.
    """
    from .seminorm_envelope import max_min_lines
    r = float(r)
    best = 0.0
    for i, j in itertools.permutations(range(len(shares)), 2):
        a_i, a_j = float(shares[i]), float(shares[j])
        lines = [(a_i, a_j), (0.0, a_j * (1 + 1 / r)),
                 (a_j * (1 / r - 1), -a_j * (1 / r - 1)),
                 (a_i * (1 + 1 / r), -a_i * (1 + 1 / r))]
        best = max(best, max_min_lines(lines))
    return best
