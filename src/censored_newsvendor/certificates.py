"""Certificate upper bound on the worst exclusion gap for arbitrary shares.

Symmetric absolute loss, expected grand cost L = 1, charges a = w, standalone
floor rho >= r (so c(e_j) <= a_j/r) and integer excess B. Fix a face F (the
producers not excluded at the given depth) and a membership z on F. By
positive homogeneity a maximizer with positive excess can be scaled until its
largest coordinate equals one; call that producer the unit u and order the
others decreasingly. For every coalition S inside F and every scale nu = z_t
with t in F, the triangle inequality and the caps give

    nu c(1_S) <= c(z) + sum_{i in S} (a_i/r) |z_i - nu| + sum_{i in F\\S} (a_i/r) z_i,

and c(1_S) >= a(S) - B. Since nu <= 1, B only weakens the resulting bound on
the excess. For a fixed ordering every certificate is linear in z, so
"maximize the minimum of all certificates and of a'z" is one LP; the bound is
the largest value over faces, units and orderings. It is valid for every
demand law. Whether it is attained is checked separately (explicit laws).

With asymmetric penalties (``kappa > 1``, see docs/asymmetric_penalties.md)
the cost is sublinear with c(-e_i) <= kappa c(e_i), so a coordinate where
z_i exceeds nu, and every coordinate outside S, is charged kappa a_i/r
instead of a_i/r. Nothing else changes.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import linprog


def certificate_bound(shares, r, depth=1, kappa=1.0):
    """Upper bound on sup (D_depth - B)/L; returns (bound, maximizing membership)."""
    a = np.asarray(shares, dtype=float)
    n = len(a)
    if not 0 < r <= 1:
        raise ValueError("0 < r <= 1 required")
    if not 1 <= depth <= n - 2:
        raise ValueError("depth must lie in 1..n-2")
    if kappa < 1:
        raise ValueError("kappa must be at least 1")
    cap = a / r
    best, argbest = 0.0, np.zeros(n)
    for excluded in itertools.combinations(range(n), depth):
        face = [j for j in range(n) if j not in excluded]
        subsets = [s for size in range(1, len(face) + 1)
                   for s in itertools.combinations(face, size)]
        for unit in face:
            others = [j for j in face if j != unit]
            for order in itertools.permutations(others):
                value, z = _ordered_lp(a, cap, face, subsets, unit, order, kappa)
                if value > best:
                    best, argbest = value, z
    return best, argbest


def _ordered_lp(a, cap, face, subsets, unit, order, kappa=1.0):
    n, k = len(a), len(order)
    width = k + 1                       # z of the ordered producers, then w
    position = {j: p for p, j in enumerate(order)}

    def linear(j):
        """z_j as (constant, coefficient vector)."""
        coefficient = np.zeros(width)
        if j == unit:
            return 1.0, coefficient
        coefficient[position[j]] = 1.0
        return 0.0, coefficient

    rank = {unit: -1, **position}       # smaller rank means larger coordinate
    rows, rhs = [], []
    for p in range(k):                  # 1 >= z_order[0] >= ... >= z_order[-1] >= 0
        row = np.zeros(width)
        row[p] = 1.0
        if p > 0:
            row[p - 1] = -1.0
        rows.append(row)
        rhs.append(1.0 if p == 0 else 0.0)
    row = np.zeros(width)
    row[k - 1] = -1.0
    rows.append(row)
    rhs.append(0.0)

    base_const, base = 0.0, np.zeros(width)
    for j in face:
        c, v = linear(j)
        base_const += a[j] * c
        base = base + a[j] * v
    forms = [(base_const, base)]
    for s in subsets:
        weight = a[list(s)].sum()
        for t in face:
            tc, tv = linear(t)
            const, coef = base_const - weight * tc, base - weight * tv
            for i in face:
                ic, iv = linear(i)
                if i in s:
                    # z_i >= nu: the difference nu - z_i is a shortfall
                    # direction, charged at the larger cap kappa a_i/r.
                    if rank[i] <= rank[t]:
                        charge = kappa * cap[i]
                    else:
                        charge = -cap[i]
                    const += charge * (ic - tc)
                    coef = coef + charge * (iv - tv)
                else:
                    const += kappa * cap[i] * ic
                    coef = coef + kappa * cap[i] * iv
            forms.append((const, coef))
    for const, coef in forms:
        row = -coef.copy()
        row[-1] = 1.0
        rows.append(row)
        rhs.append(const)
    objective = np.zeros(width)
    objective[-1] = -1.0
    result = linprog(objective, A_ub=np.array(rows), b_ub=np.array(rhs),
                     bounds=[(None, None)] * width, method="highs")
    if result.status != 0:
        return -np.inf, None
    z = np.zeros(n)
    z[unit] = 1.0
    for j in order:
        z[j] = result.x[position[j]]
    return float(-result.fun), z
