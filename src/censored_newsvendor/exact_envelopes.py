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


# ---------------------------------------------------------------------------
# Inside the windows: two further families of explicit laws
# ---------------------------------------------------------------------------

def positive_cost_construction(n, r, depth, p):
    """Family H_p: p unit producers, the other m-p at t = (1-r)/2, c(z) > 0.

    Valid for (m-p)/(m+p) <= r <= 1; value (m-p)(1-r^2)/(2nr). For p = 1 this
    is the high-regime law of Theorem 1.
    """
    r = F(r)
    a, cap = F(1, n), F(1, n) / r
    free = n - depth
    q = free - p
    if not (q >= 1 and F(q, q + 2 * p) <= r <= 1):
        return None
    delta = cap * (1 - r) / 2
    beta = ((p + q) * a - q * cap * (1 + r) / 2) / p
    generators = [_vec(n, {i: beta}) for i in range(p)]
    generators += [_vec(n, {k: a}) for k in range(free, n)]
    generators += [_vec(n, {**{i: delta / p for i in range(p)}, j: -cap})
                   for j in range(p, free)]
    z = _vec(n, {**{i: 1 for i in range(p)}, **{j: (1 - r) / 2 for j in range(p, free)}})
    return {"regime": f"H{p}", "p": p, "generators": generators, "membership": z,
            "value": q * (1 - r * r) / (2 * n * r)}


def transitional_construction(n, r, depth, p):
    """Family V_p: p unit producers, one producer at t1, the others at t2, c(z) = 0.

    Defined on the window between I_{p+1} and I_p, i.e. for
    (m-p-1)/(m+p+1) <= r <= (m-2p)/m, which is nonempty when p^2+p < m.
    """
    r = F(r)
    free = n - depth
    q2 = free - p - 1
    if q2 < 1 or not F(q2, free + p + 1) <= r <= F(free - 2 * p, free):
        return None
    a, cap = F(1, n), F(1, n) / r
    t1 = (p + 1) * (1 - r) / (2 * (p + 1) - free * (1 - r))
    t2 = ((p + 1) * r - 1 + t1) / q2
    gamma = cap * (p + t1 - q2 * t2) / (2 * p)
    alpha = p * (cap - gamma) / q2
    beta = (cap - gamma * p / t1) / q2
    delta = -gamma * p / t1
    units, star, fractional = range(p), p, range(p + 1, free)
    generators = [_vec(n, {**{i: alpha / p for i in units}, star: beta, j: -cap})
                  for j in fractional]
    generators.append(_vec(n, {**{i: gamma for i in units}, star: delta}))
    generators += [_vec(n, {k: a}) for k in range(free, n)]
    z = _vec(n, {**{i: 1 for i in units}, star: t1, **{j: t2 for j in fractional}})
    return {"regime": f"V{p}", "p": p, "generators": generators, "membership": z,
            "value": a * (p - 1 + (p + 1) * r + 2 * t1)}


def best_equal_share_construction(n, r, depth=1):
    """Best explicit law among all families (C31, H_p, V_p) at this ratio."""
    free = n - depth
    found = [equal_share_construction(n, r, depth)]
    found += [positive_cost_construction(n, r, depth, p) for p in range(1, free)]
    found += [transitional_construction(n, r, depth, p) for p in range(1, free)]
    found = [c for c in found if c is not None]
    return max(found, key=lambda c: c["value"])


def window_switch_polynomial(n, r, depth, p):
    """Q(r) = m r^2 + 2(p-1) r + 2 + 2p - m; V_p wins where Q >= 0, H_{p+1} where Q <= 0."""
    free = n - depth
    r = F(r)
    return free * r * r + 2 * (p - 1) * r + 2 + 2 * p - free


def equal_share_exact_value(n, r, depth=1):
    """Closed-form worst gap (D_depth - B)/L for equal shares, every 0 < r <= 1.

    Theorem 1 outside the windows; inside the window between I_{p+1} and I_p
    (Theorem 4) the value is V_p(r) when Q(r) >= 0 and H_{p+1}(r) otherwise.
    """
    r = F(r)
    value = equal_share_value(n, r, depth)
    if value is not None:
        return value
    free = n - depth
    for p in range(1, free - 1):
        lo, hi = F(free - p - 1, free + p + 1), F(free - 2 * p, free)
        if lo <= r <= hi:
            if window_switch_polynomial(n, r, depth, p) >= 0:
                return transitional_construction(n, r, depth, p)["value"]
            return positive_cost_construction(n, r, depth, p + 1)["value"]
    raise AssertionError("ratio not covered")


# ---------------------------------------------------------------------------
# Arbitrary shares, any depth: the two main families
# ---------------------------------------------------------------------------

def general_share_construction(shares, r, depth=1):
    """Best explicit law among the C31 and positive-cost families, any shares.

    For an excluded set K, unit producers I and fractional producers J
    (F = I + J), with a(I) and A_J their share totals:
    * C31 family, when A_J(1-r)/(1+r) <= a(I) <= A_J(1-r)/(2r): value
      (1-r)a(F), witness 1_I + t 1_J with t = (1-r) - r a(I)/A_J and c(z) = 0;
    * positive-cost family, when a(I) >= A_J(1-r)/(2r): value
      A_J(1-r^2)/(2r), witness 1_I + ((1-r)/2) 1_J.
    Unit coefficients are proportional to the shares. Returns None if no
    partition qualifies.
    """
    a = [F(x) for x in shares]
    r = F(r)
    n = len(a)
    best = None
    for excluded in itertools.combinations(range(n), depth):
        face = [j for j in range(n) if j not in excluded]
        base = [_vec(n, {k: a[k]}) for k in excluded]
        for size in range(1, len(face)):
            for units in itertools.combinations(face, size):
                fractional = [j for j in face if j not in units]
                a_units = sum(a[i] for i in units)
                a_frac = sum(a[j] for j in fractional)
                candidates = []
                if a_frac * (1 - r) / (1 + r) <= a_units <= a_frac * (1 - r) / (2 * r):
                    t = (1 - r) - r * a_units / a_frac
                    gens = base + [_vec(n, {**{i: (a[j] / r) * t * a[i] / a_units for i in units},
                                            j: -a[j] / r}) for j in fractional]
                    z = _vec(n, {**{i: 1 for i in units}, **{j: t for j in fractional}})
                    candidates.append(("C31", gens, z, (1 - r) * (a_units + a_frac)))
                if a_units >= a_frac * (1 - r) / (2 * r):
                    spread = a_frac * (1 - r) / (2 * r)
                    kappa = 1 - spread / a_units
                    gens = base + [_vec(n, {i: kappa * a[i]}) for i in units]
                    gens += [_vec(n, {**{i: (a[j] / r) * (1 - r) / 2 * a[i] / a_units for i in units},
                                      j: -a[j] / r}) for j in fractional]
                    z = _vec(n, {**{i: 1 for i in units}, **{j: (1 - r) / 2 for j in fractional}})
                    candidates.append(("H", gens, z, a_frac * (1 - r * r) / (2 * r)))
                for regime, gens, z, value in candidates:
                    if best is None or value > best["value"]:
                        best = {"regime": regime, "excluded": excluded, "units": units,
                                "generators": gens, "membership": z, "value": value}
    return best


def general_transitional_candidates(shares, r, depth=1):
    """Transitional family for arbitrary shares (faces with at least 3 free producers).

    Units I, one producer * in transition, fractional producers J' at a common
    level. With a(I), a_*, A_J' the share totals and a(F) their sum,
    t1 = (1-r)(a(I)+a_*)/(r a(F) + a(I) + a_* - A_J'),
    t2 = (r(a(I)+a_*) - (1-t1)a_*)/A_J', value a(I)(1+r) - a_*(1-r) + 2 t1 a_*;
    unit coefficients proportional to the shares. A candidate is kept only if
    every constraint holds in exact arithmetic.
    """
    a = [F(x) for x in shares]
    r = F(r)
    n = len(a)
    out = []
    for excluded in itertools.combinations(range(n), depth):
        face = [j for j in range(n) if j not in excluded]
        base = [_vec(n, {k: a[k]}) for k in excluded]
        for size in range(1, len(face) - 1):
            for units in itertools.combinations(face, size):
                for star in face:
                    if star in units:
                        continue
                    rest = [j for j in face if j not in units and j != star]
                    a_u, a_s, a_r = sum(a[i] for i in units), a[star], sum(a[j] for j in rest)
                    denominator = r * (a_u + a_s + a_r) + a_u + a_s - a_r
                    if denominator <= 0:
                        continue
                    t1 = (1 - r) * (a_u + a_s) / denominator
                    t2 = (r * (a_u + a_s) - (1 - t1) * a_s) / a_r
                    if not (0 < t1 <= 1 and 0 <= t2 <= 1):
                        continue
                    gamma = (a_u + t1 * a_s - t2 * a_r) / (2 * r)
                    alpha = (a_u / r - gamma) / (a_r / r)
                    beta = (a_s / r - gamma / t1) / (a_r / r)
                    if gamma < 0 or alpha < 0 or beta < 0:
                        continue
                    gens = list(base)
                    for j in rest:
                        cap = a[j] / r
                        gens.append(_vec(n, {**{i: cap * alpha * a[i] / a_u for i in units},
                                             star: cap * beta, j: -cap}))
                    gens.append(_vec(n, {**{i: gamma * a[i] / a_u for i in units}, star: -gamma / t1}))
                    z = _vec(n, {**{i: 1 for i in units}, star: t1, **{j: t2 for j in rest}})
                    value = a_u * (1 + r) - a_s * (1 - r) + 2 * t1 * a_s
                    check = verify_generators(gens, a, r, z, value)
                    if (check["cap"] >= 0 and check["stability"] >= 0 and check["grand"] >= 0
                            and check["witness"] == 0 and check["rho"] >= r):
                        out.append({"regime": "V", "excluded": excluded, "units": units,
                                    "transitional": star, "generators": gens, "membership": z,
                                    "value": value})
    return out


def general_cap_binding_candidates(shares, r, depth=1):
    """Cap-binding family for arbitrary shares, generalizing the third regime of Theorem 2.

    Units I at their standalone caps, fractional producers J at a common level
    t = a(I)/(r A_J + (1+r) a(I)), c(z) = 0, value a(I) + t A_J; valid when
    a(I) <= A_J (1-r)/(1+r). One generator per fractional producer j, with
    entries c_j t a_i/a(I) on the units and -c_j at j, where c_j = a_j a(I)/(r t A_J).
    """
    a = [F(x) for x in shares]
    r = F(r)
    n = len(a)
    out = []
    for excluded in itertools.combinations(range(n), depth):
        face = [j for j in range(n) if j not in excluded]
        base = [_vec(n, {k: a[k]}) for k in excluded]
        for size in range(1, len(face)):
            for units in itertools.combinations(face, size):
                fractional = [j for j in face if j not in units]
                a_u, a_f = sum(a[i] for i in units), sum(a[j] for j in fractional)
                if a_u > a_f * (1 - r) / (1 + r):
                    continue
                t = a_u / (r * a_f + (1 + r) * a_u)
                scale = a_u / (r * t * a_f)
                gens = list(base)
                for j in fractional:
                    c_j = scale * a[j]
                    gens.append(_vec(n, {**{i: c_j * t * a[i] / a_u for i in units}, j: -c_j}))
                z = _vec(n, {**{i: 1 for i in units}, **{j: t for j in fractional}})
                out.append({"regime": "G", "excluded": excluded, "units": units,
                            "generators": gens, "membership": z, "value": a_u + t * a_f})
    return out


def best_general_construction(shares, r, depth=1):
    """Best explicit law over the four known families, for any shares and depth."""
    found = []
    two = general_share_construction(shares, r, depth)
    if two is not None:
        found.append(two)
    found += general_transitional_candidates(shares, r, depth)
    found += general_cap_binding_candidates(shares, r, depth)
    return max(found, key=lambda c: c["value"])
