"""Asymmetric imbalance penalties.

A producer that offers q and delivers X pays lam_plus (X - q)^+ for a surplus
and lam_minus (q - X)^+ for a shortfall. Up to the factor lam_plus + lam_minus
this is the pinball loss of level tau = lam_plus / (lam_plus + lam_minus),

    l_tau(u) = tau u^+ + (1 - tau) u^-,        u = X - q,

and the optimized cost c(x) = min_q E l_tau(x'Y - q) is sublinear but no longer
symmetric. Because l_{1-tau} <= kappa l_tau pointwise, with
kappa = max(tau, 1 - tau) / min(tau, 1 - tau), every such cost satisfies
c(-x) <= kappa c(x). Conversely, every sum of segments [-beta d, alpha d] with
alpha / beta in [1/kappa, kappa] is the cost of a finite demand law
(``three_point_law``). The theory is in docs/asymmetric_penalties.md.

A segment is a triple (d, alpha, beta) with cost alpha (d'x)^+ + beta (d'x)^-.
Exact functions use Fractions; the LP helpers use floats.
"""

from __future__ import annotations

import itertools
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog

from .seminorm_envelope import proper_coalitions


def _vec(n, entries):
    v = [F(0)] * n
    for k, x in entries.items():
        v[k] = F(x)
    return tuple(v)


def ratio_for_level(tau):
    """Penalty ratio kappa = max(tau, 1-tau) / min(tau, 1-tau)."""
    tau = F(tau)
    if not 0 < tau < 1:
        raise ValueError("tau must lie in (0, 1)")
    return max(tau, 1 - tau) / min(tau, 1 - tau)


def level_for_ratio(kappa):
    """The level tau <= 1/2 with penalty ratio kappa (surplus is the cheaper side)."""
    kappa = F(kappa)
    if kappa < 1:
        raise ValueError("kappa must be at least 1")
    return 1 / (1 + kappa)


def pinball_cost(states, probabilities, x, tau):
    """min_q E l_tau(x'Y - q) for a finite law, evaluated at a tau-quantile."""
    tau = F(tau) if isinstance(tau, (int, F)) else tau
    values = sorted((sum(s_i * x_i for s_i, x_i in zip(state, x)), p)
                    for state, p in zip(states, probabilities))
    cumulative, quantile = 0, values[-1][0]
    for value, p in values:
        cumulative += p
        if cumulative >= tau:
            quantile = value
            break
    return sum(p * (tau * max(v - quantile, 0) + (1 - tau) * max(quantile - v, 0))
               for v, p in values)


def segment_cost(segments, x):
    """c(x) = sum alpha (d'x)^+ + beta (d'x)^- over the segments."""
    total = 0
    for d, alpha, beta in segments:
        s = sum(d_i * x_i for d_i, x_i in zip(d, x))
        total += alpha * s if s > 0 else -beta * s
    return total


# ---------------------------------------------------------------------------
# The last depth (two free producers) for every penalty ratio
# ---------------------------------------------------------------------------

def asymmetric_pair_regime(a_u, a_j, r, kappa):
    """Regime, fractional membership t and value for unit u and fractional j.

    With x = a_u / a_j the worst gap of the ordered pair is
      a_j (1-r)(r+kappa) / (r(1+kappa))          if x >= kappa(1-r)/(r(1+kappa)),
      (1-r)(a_u + a_j)                           if (1-r)/(r+kappa) <= x <= kappa(1-r)/(r(1+kappa)),
      a_u (r+kappa)(a_u+a_j) / (a_u(r+kappa) + r a_j)   if x <= (1-r)/(r+kappa).
    With kappa = 1 these are the three regimes of Theorem 2.
    """
    a_u, a_j, r, kappa = F(a_u), F(a_j), F(r), F(kappa)
    x = a_u / a_j
    if x >= kappa * (1 - r) / (r * (1 + kappa)):
        t = (1 - r) / (1 + kappa)
        return "shortfall", t, a_j * (1 - r) * (r + kappa) / (r * (1 + kappa))
    if x >= (1 - r) / (r + kappa):
        t = 1 - r - r * x
        return "ceiling", t, (1 - r) * (a_u + a_j)
    t = kappa * a_u / (a_u * (r + kappa) + r * a_j)
    return "unit-cap", t, a_u + t * a_j


def asymmetric_last_depth_value(shares, r, kappa):
    """Exact worst gap (D_{n-2} - B)/L under penalty ratio kappa."""
    a = [F(x) for x in shares]
    return max(asymmetric_pair_regime(a[i], a[j], r, kappa)[2]
               for i, j in itertools.permutations(range(len(a)), 2))


def asymmetric_last_depth_construction(shares, r, kappa):
    """Segments, membership and value attaining the last-depth worst gap."""
    a = [F(x) for x in shares]
    r, kappa = F(r), F(kappa)
    n = len(a)
    (regime, t, value), u, j = max(
        ((asymmetric_pair_regime(a[i], a[k], r, kappa), i, k)
         for i, k in itertools.permutations(range(n), 2)),
        key=lambda item: item[0][2])
    m_u, m_j = a[u] / r, a[j] / r
    segments = [(_vec(n, {k: 1}), a[k], a[k]) for k in range(n) if k not in (u, j)]
    if regime == "shortfall":
        # d'z = 0; the shortfall side of d carries kappa times the cap of j.
        weight = a[u] - kappa * m_j * t
        segments += [(_vec(n, {u: t, j: -1}), kappa * m_j, m_j),
                     (_vec(n, {u: 1}), weight, weight)]
    elif regime == "ceiling":
        low = max(a[u] / t, m_j / kappa)
        high = min(m_u / t, kappa * m_j)
        alpha = min(max(m_j, low), high)        # the symmetric choice when possible
        segments += [(_vec(n, {u: t, j: -1}), alpha, m_j)]
    else:
        segments += [(_vec(n, {u: 1, j: -1 / t}), m_u, kappa * m_u)]
    z = _vec(n, {u: 1, j: t})
    return {"regime": regime, "pair": (u, j), "segments": segments,
            "membership": z, "value": value}


def verify_segments(segments, shares, r, kappa, membership, value):
    """Minimal slacks of every constraint, in exact arithmetic.

    All must be >= 0 and the witness slack must be 0 for the law to attain
    ``value``: cap (a_j/r - c(e_j)), stability (c(1_S) - a(S) over proper S),
    grand (1 - c(1)), witness (a'z - c(z) - value) and ratio
    (kappa min(alpha, beta) - max(alpha, beta), so that the segments are the
    cost of a law with penalty ratio kappa).
    """
    a = [F(x) for x in shares]
    r, kappa = F(r), F(kappa)
    n = len(a)
    unit = [_vec(n, {j: 1}) for j in range(n)]
    cap = min(a[j] / r - segment_cost(segments, unit[j]) for j in range(n))
    stability = min(
        segment_cost(segments, _vec(n, {j: 1 for j in s})) - sum(a[j] for j in s)
        for s in proper_coalitions(n))
    grand = 1 - segment_cost(segments, _vec(n, {j: 1 for j in range(n)}))
    witness = (sum(x * y for x, y in zip(a, membership))
               - segment_cost(segments, membership) - value)
    ratio = min(kappa * min(al, be) - max(al, be) for _, al, be in segments)
    nonnegative = min(min(al, be) for _, al, be in segments)
    return {"cap": cap, "stability": stability, "grand": grand,
            "witness": witness, "ratio": ratio, "nonnegative": nonnegative}


# ---------------------------------------------------------------------------
# Explicit laws
# ---------------------------------------------------------------------------

def three_point_law(segments, tau):
    """A finite law on [0,1]^n whose pinball cost is scale * segment_cost.

    Component k is chosen with probability 1/K and moves the centre along
    d_k by K V_k, where V_k takes the values A/p, -B/p (probability p each,
    p = min(tau, 1-tau)) and 0. Zero is then a tau- and a (1-tau)-quantile of
    every component, so the components share the optimal offer and their
    costs add. Solving alpha = tau A + (1-tau) B, beta = (1-tau) A + tau B
    needs alpha/beta in [1/kappa, kappa]. Returns (states, probabilities,
    scale), where scale = 1/(2R) comes from the affine map onto the box.
    """
    tau = F(tau)
    p = min(tau, 1 - tau)
    count = len(segments)
    n = len(segments[0][0])
    atoms, probabilities = [], []
    for d, alpha, beta in segments:
        alpha, beta = F(alpha), F(beta)
        if tau == F(1, 2):
            if alpha != beta:
                raise ValueError("symmetric loss needs symmetric segments")
            up = down = alpha
        else:
            up = (tau * alpha - (1 - tau) * beta) / (2 * tau - 1)
            down = (tau * beta - (1 - tau) * alpha) / (2 * tau - 1)
            if up < 0 or down < 0:
                raise ValueError("segment ratio outside [1/kappa, kappa]")
        for value, mass in ((up / p, p), (-down / p, p), (F(0), 1 - 2 * p)):
            if mass > 0:
                atoms.append(tuple(count * value * F(d_i) for d_i in d))
                probabilities.append(mass / count)
    radius = max(max(abs(x) for x in atom) for atom in atoms) or F(1)
    states = [tuple(F(1, 2) + x / (2 * radius) for x in atom) for atom in atoms]
    return states, probabilities, 1 / (2 * radius)


# ---------------------------------------------------------------------------
# Numerical search over asymmetric zonotopes (any depth)
# ---------------------------------------------------------------------------

def _test_vectors(n, z):
    rows = [np.eye(n)[j] for j in range(n)]
    for coalition in proper_coalitions(n):
        if len(coalition) >= 2:
            row = np.zeros(n)
            row[list(coalition)] = 1.0
            rows.append(row)
    rows.append(np.ones(n))
    rows.append(np.asarray(z, dtype=float))
    return np.array(rows)


def ray_directions(vectors, tol=1e-9):
    """Directions orthogonal to n-1 independent test vectors, up to sign.

    On a finite test set every segment cost alpha (d'x)^+ + beta (d'x)^- is a
    nonnegative combination of segment costs along these rays with the same
    alpha/beta (a closed chamber is generated by its rays and the signs of
    d'x are constant on it), so restricting to the rays loses nothing.
    """
    vectors = np.asarray(vectors, dtype=float)
    n = vectors.shape[1]
    combos = np.array(list(itertools.combinations(range(len(vectors)), n - 1)))
    stack = vectors[combos]
    _, singular, vt = np.linalg.svd(stack)
    keep = singular[:, -1] > tol * np.maximum(singular[:, 0], 1.0)
    directions = vt[keep, -1, :]
    directions /= np.abs(directions).max(axis=1, keepdims=True)
    lead = np.argmax(np.abs(directions) > tol, axis=1)
    directions *= np.sign(directions[np.arange(len(directions)), lead])[:, None]
    _, unique = np.unique(np.round(directions, 9), axis=0, return_index=True)
    return directions[np.sort(unique)]


def asymmetric_zonotope_minimal_cost(z, shares, r, kappa, *, integer_excess=0.0,
                                     grand_cost=1.0):
    """Smallest c(z) over kappa-bounded asymmetric zonotopes (one LP).

    Every such cost is realized by ``three_point_law``, so a'z - B minus this
    value is attained by an explicit law with penalty ratio kappa.
    """
    a = np.asarray(shares, dtype=float)
    n = len(a)
    vectors = _test_vectors(n, z)
    rays = ray_directions(vectors)
    products = vectors @ rays.T                      # |T| x R
    rows_cost = np.hstack([np.maximum(products, 0), np.maximum(-products, 0)])
    count = len(rays)
    rows, rhs = [], []
    for j in range(n):
        rows.append(rows_cost[j])
        rhs.append(a[j] / r)
    rows.append(rows_cost[len(vectors) - 2])
    rhs.append(grand_cost)
    larger = [c for c in proper_coalitions(n) if len(c) >= 2]
    for coalition in proper_coalitions(n):
        t = coalition[0] if len(coalition) == 1 else n + larger.index(coalition)
        rows.append(-rows_cost[t])
        rhs.append(-(a[list(coalition)].sum() - integer_excess))
    eye = np.eye(count)
    rows_ratio = np.vstack([np.hstack([-kappa * eye, eye]),
                            np.hstack([eye, -kappa * eye])])
    result = linprog(rows_cost[-1],
                     A_ub=np.vstack([np.array(rows), rows_ratio]),
                     b_ub=np.r_[np.array(rhs), np.zeros(2 * count)],
                     bounds=[(0, None)] * (2 * count), method="highs")
    if result.status != 0:
        return {"value": None, "segments": None, "rays": count}
    alpha, beta = result.x[:count], result.x[count:]
    used = (alpha + beta) > 1e-10
    segments = [(rays[k], alpha[k], beta[k]) for k in np.flatnonzero(used)]
    return {"value": float(result.fun), "segments": segments, "rays": count}


def asymmetric_envelope_check(shares, r, kappa, depth):
    """Certificate upper bound and the best explicit law at its maximizer."""
    from .certificates import certificate_bound

    bound, z = certificate_bound(shares, r, depth, kappa=kappa)
    if bound <= 1e-12:
        return {"bound": bound, "attained": 0.0, "membership": None}
    found = asymmetric_zonotope_minimal_cost(z, shares, r, kappa)
    attained = float(np.dot(shares, z)) - found["value"]
    return {"bound": float(bound), "attained": attained,
            "membership": [float(x) for x in z], "segments": len(found["segments"]),
            "rays": found["rays"]}


# ---------------------------------------------------------------------------
# Equal shares at every depth
# ---------------------------------------------------------------------------

def asymmetric_configuration_intervals(n, depth, kappa):
    """Intervals on which the ceiling (1-r)m/n is attained, kappa >= 1.

    With p unit producers and q = m - p fractional ones the ceiling law
    exists exactly for max(0, (m-(1+kappa)p)/m) <= r <= kappa(m-p)/(kappa m+p).
    With kappa = 1 these are the intervals I_p of Theorem 1.
    """
    kappa = F(kappa)
    m = n - depth
    return [(p, max(F(0), (m - (1 + kappa) * p) / m), kappa * (m - p) / (kappa * m + p))
            for p in range(1, m)]


def asymmetric_high_threshold(n, depth, kappa):
    """kappa(m-1)/(kappa m + 1): above it the family H_1 is exact."""
    kappa = F(kappa)
    m = n - depth
    return kappa * (m - 1) / (kappa * m + 1)


def asymmetric_windows(n, depth, kappa):
    """Open subintervals of [0, high threshold] covered by no interval.

    The window between the configurations p+1 and p is
    (kappa(m-p-1)/(kappa m+p+1), (m-(1+kappa)p)/m); it is nonempty iff
    kappa < (p+1)(m-p)/(p m). All windows are closed once kappa >= 2(m-1)/m.
    """
    covered = sorted((lo, hi) for _, lo, hi in
                     asymmetric_configuration_intervals(n, depth, kappa))
    gaps, reach = [], F(0)
    for lo, hi in covered:
        if lo > reach:
            gaps.append((reach, lo))
        reach = max(reach, hi)
    top = asymmetric_high_threshold(n, depth, kappa)
    if reach < top:
        gaps.append((reach, top))
    return gaps


def asymmetric_high_value(n, r, depth, kappa, p=1):
    """Family H_p: (m-p) a (1-r)(r+kappa) / (r(1+kappa)) with a = 1/n."""
    r, kappa = F(r), F(kappa)
    m = n - depth
    return (m - p) * (1 - r) * (r + kappa) / (n * r * (1 + kappa))


def asymmetric_equal_share_value(n, r, depth, kappa):
    """Exact worst gap for equal shares, or None inside a window.

    Outside the windows the value is min{(1-r)m/n, H_1}; the upper bound
    holds for every r (two certificates and the ceiling).
    """
    r, kappa = F(r), F(kappa)
    m = n - depth
    if r >= asymmetric_high_threshold(n, depth, kappa):
        return asymmetric_high_value(n, r, depth, kappa)
    for _, lo, hi in asymmetric_configuration_intervals(n, depth, kappa):
        if lo <= r <= hi:
            return (1 - r) * m / n
    return None


def asymmetric_equal_share_construction(n, r, depth, kappa, *, family=None, p=None):
    """Segments, membership and value attaining the equal-share worst gap.

    Labels: units 0..p-1, fractional producers p..m-1, excluded m..n-1.
    Ceiling family on the p-th interval: one segment per fractional j along
    d_j = (t/p on the units, -1 on j), beta = a/r, alpha within
    [max(ap/(qt), cap/kappa), min(cap p/(qt), kappa cap)], c(z) = 0.
    Family H_p: the same directions with alpha = kappa a/r, beta = a/r,
    t = (1-r)/(1+kappa), plus a symmetric segment of weight w on each unit.
    Returns None when no family applies (inside a window).
    """
    r, kappa = F(r), F(kappa)
    a = F(1, n)
    cap = a / r
    m = n - depth
    excluded = [(_vec(n, {k: 1}), a, a) for k in range(m, n)]
    if family is None:
        if r >= asymmetric_high_threshold(n, depth, kappa):
            family, p = "high", 1
        else:
            for p_, lo, hi in asymmetric_configuration_intervals(n, depth, kappa):
                if lo <= r <= hi:
                    family, p = "ceiling", p_
                    break
            else:
                return None
    q = m - p
    if family == "high":
        if r < kappa * q / (kappa * m + p):
            return None
        t = (1 - r) / (1 + kappa)
        weight = (m * a - q * cap * (1 - t)) / p
        segments = [(_vec(n, {**{i: t / p for i in range(p)}, j: -1}), kappa * cap, cap)
                    for j in range(p, m)]
        segments += [(_vec(n, {i: 1}), weight, weight) for i in range(p)]
        value = asymmetric_high_value(n, r, depth, kappa, p)
    else:
        lo_r = max(F(0), (m - (1 + kappa) * p) / m)
        if not lo_r <= r <= kappa * q / (kappa * m + p):
            return None
        t = 1 - m * r / q
        low = max(a * p / (q * t), cap / kappa)
        high = min(cap * p / (q * t), kappa * cap)
        alpha = min(max(cap, low), high)
        segments = [(_vec(n, {**{i: t / p for i in range(p)}, j: -1}), alpha, cap)
                    for j in range(p, m)]
        value = (1 - r) * m / n
    z = _vec(n, {**{i: 1 for i in range(p)}, **{j: t for j in range(p, m)}})
    return {"family": family, "p": p, "segments": segments + excluded,
            "membership": z, "value": value}


# ---------------------------------------------------------------------------
# Arbitrary shares at every depth: two-block families
# ---------------------------------------------------------------------------

def asymmetric_block_construction(shares, r, kappa, excluded, units):
    """The two-block law for an excluded set K and units I (fractional J = F - I).

    Its value is the last-depth formula applied to the blocks,
    Psi_kappa(a(I), A_J), in the regime fixed by x = a(I)/A_J. One segment per
    fractional j along d_j = (t a_i/a(I) on the units, -1 on j), so d_j'z = 0:
      shortfall: alpha = kappa a_j/r, beta = a_j/r, t = (1-r)/(1+kappa), plus a
                 symmetric segment of weight w a_i on each unit;
      ceiling:   beta = a_j/r, alpha = lam a_j/r with lam in [1/kappa, kappa]
                 and r a(I) <= lam t A_J <= a(I), t = 1 - r - r x;
      unit-cap:  alpha = s a_j, beta = kappa s a_j with s = a(I)/(r t A_J),
                 t = kappa a(I)/(a(I)(r+kappa) + r A_J).
    Excluded producers get symmetric segments of weight a_k.
    """
    a = [F(x) for x in shares]
    r, kappa = F(r), F(kappa)
    n = len(a)
    face = [j for j in range(n) if j not in excluded]
    fractional = [j for j in face if j not in units]
    a_units, a_frac = sum(a[i] for i in units), sum(a[j] for j in fractional)
    regime, t, value = asymmetric_pair_regime(a_units, a_frac, r, kappa)
    segments = [(_vec(n, {k: 1}), a[k], a[k]) for k in excluded]

    def direction(j):
        return _vec(n, {**{i: t * a[i] / a_units for i in units}, j: -1})

    if regime == "shortfall":
        weight = 1 - a_frac * kappa * (1 - r) / (r * (1 + kappa) * a_units)
        segments += [(direction(j), kappa * a[j] / r, a[j] / r) for j in fractional]
        segments += [(_vec(n, {i: 1}), weight * a[i], weight * a[i]) for i in units]
    elif regime == "ceiling":
        low = max(1 / kappa, r * a_units / (t * a_frac))
        high = min(kappa, a_units / (t * a_frac))
        lam = min(max(F(1), low), high)
        segments += [(direction(j), lam * a[j] / r, a[j] / r) for j in fractional]
    else:
        s = a_units / (r * t * a_frac)
        segments += [(direction(j), s * a[j], kappa * s * a[j]) for j in fractional]
    z = _vec(n, {**{i: 1 for i in units}, **{j: t for j in fractional}})
    return {"regime": regime, "excluded": tuple(excluded), "units": tuple(units),
            "segments": segments, "membership": z, "value": value}


def asymmetric_best_block(shares, r, depth, kappa):
    """Largest two-block value max over K and I of Psi_kappa(a(I), A_J), with its law."""
    a = [F(x) for x in shares]
    n = len(a)
    best = None
    for excluded in itertools.combinations(range(n), depth):
        face = [j for j in range(n) if j not in excluded]
        for size in range(1, len(face)):
            for units in itertools.combinations(face, size):
                a_units = sum(a[i] for i in units)
                a_frac = sum(a[j] for j in face) - a_units
                value = asymmetric_pair_regime(a_units, a_frac, r, kappa)[2]
                if best is None or value > best[0]:
                    best = (value, excluded, units)
    return asymmetric_block_construction(a, r, kappa, best[1], best[2])
