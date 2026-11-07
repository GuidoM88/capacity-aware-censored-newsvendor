"""Symbolic verification of the algebra behind docs/exact_envelopes.md.

Every equality used in the proofs is checked as a symbolic identity (sympy).
Every inequality is reduced to an explicit factorization whose sign is clear
on the stated domain; the factorization itself is checked as an identity and
the sign argument is recorded next to it. Polynomial positivity is checked by
substituting the domain bounds and verifying that all coefficients of the
resulting polynomial are nonnegative.

This complements the exact rational checks at sample points: those test the
constructions numerically, this checks the general formulas for all sizes.
It does not check the convex-analysis lemmas (gauge duality, certificates),
which are short arguments in the notes.
"""

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
CHECKS = []

a, r, m, p, q, k, n = sp.symbols("a r m p q k n", positive=True)
s, tau, kap, sig, T, A, AJ, x, t, u, v = sp.symbols("s tau kappa sigma T A A_J x t u v", positive=True)
Z, U, Y, lB = sp.symbols("Z_I u_tr Y lambda_B", real=True)
M = a / r


def record(group, name, kind, ok, detail=""):
    CHECKS.append({"group": group, "check": name, "kind": kind, "passed": bool(ok), "detail": detail})


def identity(group, name, lhs, rhs):
    if isinstance(lhs, sp.MatrixBase):
        ok = (lhs - rhs).applyfunc(sp.simplify).is_zero_matrix
        record(group, name, "identity", ok, "matrix identity")
        return
    diff = sp.simplify(sp.together(sp.expand(lhs - rhs)))
    record(group, name, "identity", diff == 0, f"{sp.sstr(lhs)} = {sp.sstr(rhs)}" if diff == 0 else f"residual {diff}")


def factorization(group, name, expr, factored, reason):
    ok = sp.simplify(sp.together(expr - factored)) == 0
    record(group, name, "sign by factorization", ok, f"{sp.sstr(factored)}; {reason}")


def nonnegative_coefficients(group, name, poly_expr, gens, reason):
    poly = sp.Poly(sp.expand(poly_expr), *gens)
    ok = all(c >= 0 for c in poly.coeffs())
    record(group, name, "polynomial coefficients", ok, f"{len(poly.coeffs())} coefficients, all >= 0; {reason}")


def bilinear(group, name, expr, x1, x2):
    ok = sp.simplify(sp.diff(expr, x1, 2)) == 0 and sp.simplify(sp.diff(expr, x2, 2)) == 0
    record(group, name, "bilinearity", ok, "second derivatives in each variable vanish, so the minimum over a box is at a corner")


# ---------------------------------------------------------------------------
# A. Elementary ceiling C31
# ---------------------------------------------------------------------------
aF, B, xx = sp.symbols("a_F B x", positive=True)
identity("A. C31", "weighted average of the two bounds", (1 - r) * (aF - B - xx) + r * (1 / r - 1) * xx,
         (1 - r) * (aF - B))

# ---------------------------------------------------------------------------
# B. Separable bound (upper bound of Theorem 1 above (m-1)/(m+1))
# ---------------------------------------------------------------------------
tstar = (M - a) / (2 * M)
identity("B. separable bound", "peak of h at t* = (1-r)/2", tstar, (1 - r) / 2)
identity("B. separable bound", "both branches of h meet at t*", (1 - tstar) * (M - a), tstar * (M + a))
identity("B. separable bound", "peak value a(1-r^2)/(2r)", tstar * (M + a), a * (1 - r**2) / (2 * r))
factorization("B. separable bound", "regime threshold r >= q/(q+2)",
              a * (1 + q * tstar) - q * a * (1 - r**2) / (2 * r), a * (r * (q + 2) - q) / (2 * r),
              "nonnegative exactly when r >= q/(q+2)")
tlow = (1 - r) - r / q
identity("B. separable bound", "low-regime intersection", a * (1 + q * tlow), q * (1 - tlow) * (M - a))
identity("B. separable bound", "low-regime value (1-r)(q+1)a", a * (1 + q * tlow), a * (1 - r) * (q + 1))
factorization("B. separable bound", "low-regime point lies right of the peak",
              tlow - tstar, ((1 - r) * q - 2 * r) / (2 * q), "nonnegative exactly when r <= q/(q+2)")

# ---------------------------------------------------------------------------
# C. Theorem 1, configuration p (C31 attained on I_p)
# ---------------------------------------------------------------------------
tc = (1 - r) - p * r / q
identity("C. Theorem 1, I_p", "fractional generators vanish at the witness", (M * tc / p) * p - M * tc, 0)
identity("C. Theorem 1, I_p", "witness value (1-r)(p+q)a", a * (p + q * tc), (1 - r) * (p + q) * a)
factorization("C. Theorem 1, I_p", "unit cap q t <= p", p - q * tc, (p + q) * r - (q - p),
              "nonnegative exactly when r >= (q-p)/(q+p)")
identity("C. Theorem 1, I_p", "grand cost k a + q M (1-t) = (p+q+k) a", k * a + q * M * (1 - tc), (p + q + k) * a)
cost_S = kap * a + tau * (M - M * tc * s / p) + (q - tau) * (M * tc * s / p)
identity("C. Theorem 1, I_p", "coalition cost formula", cost_S, kap * a + tau * M + (q - 2 * tau) * M * tc * s / p)
Phi = tau * (M - a) + (q - 2 * tau) * M * tc * s / p - a * s
identity("C. Theorem 1, I_p", "slack = cost - a|S|", cost_S - a * (s + tau + kap), Phi)
bilinear("C. Theorem 1, I_p", "slack bilinear in (s, tau)", Phi, s, tau)
identity("C. Theorem 1, I_p", "corner (0,0)", Phi.subs({s: 0, tau: 0}), 0)
identity("C. Theorem 1, I_p", "corner (0,q)", Phi.subs({s: 0, tau: q}), q * (M - a))
factorization("C. Theorem 1, I_p", "corner (p,0) >= 0", Phi.subs({s: p, tau: 0}), a * (q - r * (q + 2 * p)) / r,
              "nonnegative exactly when r <= q/(q+2p)")
identity("C. Theorem 1, I_p", "corner (p,q)", Phi.subs({s: p, tau: q}), 0)
factorization("C. Theorem 1, I_p", "witness level t >= 0", tc, (q * (1 - r) - p * r) / q,
              "nonnegative when r <= q/(q+p), implied by r <= q/(q+2p)")

# ---------------------------------------------------------------------------
# D. Family H_p (high regime of Theorem 1 for p = 1)
# ---------------------------------------------------------------------------
delta = M * (1 - r) / 2
beta = ((p + q) * a - q * M * (1 + r) / 2) / p
th = (1 - r) / 2
identity("D. family H_p", "fractional generators vanish at the witness", (delta / p) * p - M * th, 0)
identity("D. family H_p", "witness value (m-p)(1-r^2)a/(2r)", a * (p + q * th) - p * beta, q * a * (1 - r**2) / (2 * r))
identity("D. family H_p", "unit singleton cost equals a", beta + q * delta / p, a)
identity("D. family H_p", "grand cost", p * beta + k * a + q * (M - delta), (p + q + k) * a)
Psi = s * beta + tau * (M - a) + (q - 2 * tau) * delta * s / p - a * s
bilinear("D. family H_p", "slack bilinear in (s, tau)", Psi, s, tau)
identity("D. family H_p", "corner (0,q)", Psi.subs({s: 0, tau: q}), q * (M - a))
identity("D. family H_p", "corner (p,0)", Psi.subs({s: p, tau: 0}), 0)
identity("D. family H_p", "corner (p,q)", Psi.subs({s: p, tau: q}), 0)
factorization("D. family H_p", "beta >= 0", p * beta, a * (r * (2 * p + q) - q) / (2 * r),
              "nonnegative exactly when r >= q/(q+2p) = (m-p)/(m+p)")
identity("D. family H_p", "meets C31 at r = q/(q+2p)",
         (q * a * (1 - r**2) / (2 * r) - (1 - r) * (p + q) * a).subs(r, q / (q + 2 * p)), 0)

# ---------------------------------------------------------------------------
# E. Theorem 4, family V_p and the dual certificates
# ---------------------------------------------------------------------------
qq = m - p - 1
D = 2 * (p + 1) - m * (1 - r)
t1 = (p + 1) * (1 - r) / D
t2 = ((p + 1) * r - 1 + t1) / qq
gamma_def = M * (p + t1 - qq * t2) / (2 * p)
alpha_def = p * (M - gamma_def) / qq
beta_def = (M - gamma_def * p / t1) / qq
delta_def = -gamma_def * p / t1
identity("E. Theorem 4, V_p", "gamma closed form", gamma_def, M * (p + 1) * (1 - r) / (2 * p))
identity("E. Theorem 4, V_p", "alpha closed form", alpha_def, M * ((p - 1) + (p + 1) * r) / (2 * qq))
identity("E. Theorem 4, V_p", "beta closed form", beta_def, M * (m * (1 - r) - 2 * p) / (2 * qq))
identity("E. Theorem 4, V_p", "delta closed form", delta_def, -M * (2 * (p + 1) - m * (1 - r)) / 2)
identity("E. Theorem 4, V_p", "fractional generators vanish at the witness", alpha_def + beta_def * t1 - M * t2, 0)
identity("E. Theorem 4, V_p", "transition generator vanishes at the witness", gamma_def * p + delta_def * t1, 0)
identity("E. Theorem 4, V_p", "unit caps tight", qq * alpha_def / p + gamma_def, M)
identity("E. Theorem 4, V_p", "transition cap tight", qq * beta_def - delta_def, M)
identity("E. Theorem 4, V_p", "alpha + beta = M(1-r)/2", alpha_def + beta_def, M * (1 - r) / 2)
identity("E. Theorem 4, V_p", "free grand cost m a",
         qq * (M - alpha_def - beta_def) + gamma_def * p * (1 - t1) / t1, m * a)
identity("E. Theorem 4, V_p", "witness value", a * (p + t1 + qq * t2), a * (p - 1 + (p + 1) * r + 2 * t1))
w0 = alpha_def * s / p
w1 = alpha_def * s / p + beta_def
slack0 = tau * (M - a) + (qq - 2 * tau) * w0 + gamma_def * s - a * s
slack1 = tau * (M - a) + (qq - 2 * tau) * w1 + gamma_def * (p / t1 - s) - a * (s + 1)
bilinear("E. Theorem 4, V_p", "slack without * bilinear", slack0, s, tau)
bilinear("E. Theorem 4, V_p", "slack with * bilinear", slack1, s, tau)
identity("E. Theorem 4, V_p", "corner (0,q'), * out", slack0.subs({s: 0, tau: qq}), qq * (M - a))
identity("E. Theorem 4, V_p", "corner (p,0), * out", slack0.subs({s: p, tau: 0}), p * (M - a))
factorization("E. Theorem 4, V_p", "corner (p,q'), * out", slack0.subs({s: p, tau: qq}), a * ((m - p) / r - (m + p)),
              "nonnegative when r <= (m-p)/(m+p), implied by r <= r_R")
identity("E. Theorem 4, V_p", "corner (0,0), * in", slack1.subs({s: 0, tau: 0}), M - a)
identity("E. Theorem 4, V_p", "corner (0,q'), * in", slack1.subs({s: 0, tau: qq}), a * (p / r + p))
identity("E. Theorem 4, V_p", "corner (p,0), * in", slack1.subs({s: p, tau: 0}), 0)
identity("E. Theorem 4, V_p", "corner (p,q'), * in", slack1.subs({s: p, tau: qq}), 0)
factorization("E. Theorem 4, V_p", "r_R <= (m-p)/(m+p)", (m - p) / (m + p) - (m - 2 * p) / m,
              2 * p**2 / (m * (m + p)), "positive")
factorization("E. Theorem 4, V_p", "beta >= 0 iff r <= r_R", beta_def, a * m * ((m - 2 * p) / m - r) / (2 * qq * r),
              "nonnegative exactly when r <= r_R = (m-2p)/m")
factorization("E. Theorem 4, V_p", "t1 <= 1 iff r >= r_L", 1 - t1,
              (m + p + 1) * (r - (m - p - 1) / (m + p + 1)) / D, "nonnegative exactly when r >= r_L, with D > 0")
factorization("E. Theorem 4, V_p", "D > 0 on the window",
              (m - p - 1) / (m + p + 1) - (m - 2 * p - 2) / m, 2 * (p + 1)**2 / (m * (m + p + 1)),
              "r_L exceeds (m-2p-2)/m, the zero of D")
sv = sp.symbols("s_v", positive=True)                       # s_v = 1 - r
phi = (p + 1) * m * sv**2 - (p * m + (p + 1) * (2 * p + 1)) * sv + 2 * p * (p + 1)
identity("E. Theorem 4, V_p", "q' t2 D equals the quadratic phi(1-r)", sp.expand(qq * t2 * D), phi.subs(sv, 1 - r))
identity("E. Theorem 4, V_p", "phi at the right end of the window", phi.subs(sv, 2 * p / m), 2 * p * (m - p - 1) / m)
nonnegative_coefficients("E. Theorem 4, V_p", "vertex of phi right of the window, p >= 3",
                         ((p * m + (p + 1) * (2 * p + 1)) * (m + p + 1) - 4 * m * (p + 1)**2)
                         .subs(m, p**2 + p + 1 + u).subs(p, 3 + v), (u, v),
                         "windows need m >= p^2+p+1; substituted m = p^2+p+1+u, p = 3+v")
N1 = (p * m + (p + 1) * (2 * p + 1)) * (m + p + 1) - 4 * m * (p + 1)**2
identity("E. Theorem 4, V_p", "vertex condition for p = 2", N1.subs(p, 2), 2 * m**2 - 15 * m + 45)
record("E. Theorem 4, V_p", "2m^2 - 15m + 45 > 0", "discriminant", sp.discriminant(2 * m**2 - 15 * m + 45, m) < 0,
       "discriminant -135 < 0")
factorization("E. Theorem 4, V_p", "vertex condition for p = 1", N1.subs(p, 1), (m - 2) * (m - 6),
              "nonnegative for m >= 6")
factorization("E. Theorem 4, V_p", "discriminant of phi for p = 1",
              sp.discriminant(phi.subs(p, 1), sv), (m - 2) * (m - 18), "negative for m = 3, 4, 5")
# Dual certificates, in the variables Z_I (top p), u_tr (coordinate p+1), Y (the rest)
F0 = a * (Z + U + Y)
FA = a * (Z + U + Y) - (p + 1) * a + M * ((p - Z) + (1 - U) + Y)
FB = a * (Z + U + Y) - m * a * U + M * (Z - p * U + qq * U - Y)
FBp = a * (Z + U + Y) - m * a + M * ((p - Z) + (1 - U) + qq - Y)
Q = m * r**2 + 2 * (p - 1) * r + 2 + 2 * p - m
l0 = (M**2 * (2 + 2 * p - m) + 2 * a * M * (p - 1) + m * a**2) / (2 * a * M)
lA = (M * (m - 2 * p) - m * a) / (2 * M)
mu1 = M * (2 + 2 * p - m) + a * m
combo = sp.expand(l0 * F0 + lA * FA + FB + mu1 * (p - Z))
for var in (Z, U, Y):
    identity("E. Theorem 4, duals", f"V regime: coefficient of {var} cancels", sp.diff(combo, var), 0)
identity("E. Theorem 4, duals", "V regime: constant equals V_p",
         combo.subs({Z: 0, U: 0, Y: 0}) / (l0 + lA + 1), a * (p - 1 + (p + 1) * r + 2 * t1))
identity("E. Theorem 4, duals", "V regime: lambda_0 proportional to Q", l0 * 2 * a * M, a**2 * Q / r**2)
factorization("E. Theorem 4, duals", "V regime: lambda_A >= 0", lA, m * ((m - 2 * p) / m - r) / (2),
              "nonnegative exactly when r <= r_R")
factorization("E. Theorem 4, duals", "V regime: multiplier on p - Z_I >= 0", mu1, a * m * (r - (m - 2 * p - 2) / m) / r,
              "nonnegative since r >= r_L > (m-2p-2)/m")
lAh = (M - a) / (2 * M)
lBp = (M + a) / (2 * M) - lB
mu1h = (a - M) + 2 * M * lB
mu3h = (a - M) + lB * (M * (m - 2 * p) - m * a)
comboH = sp.expand(lAh * FA + lB * FB + lBp * FBp + mu1h * (p - Z) + mu3h * (1 - U))
for var in (Z, U, Y):
    identity("E. Theorem 4, duals", f"H regime: coefficient of {var} cancels for every lambda_B", sp.diff(comboH, var), 0)
identity("E. Theorem 4, duals", "H regime: weights sum to one", lAh + lB + lBp, 1)
identity("E. Theorem 4, duals", "H regime: constant equals H_{p+1}",
         comboH.subs({Z: 0, U: 0, Y: 0}), qq * a * (1 - r**2) / (2 * r))
identity("E. Theorem 4, duals", "H regime: feasibility rearranges to Q <= 0",
         (M + a) * (M * (m - 2 * p) - m * a) - 2 * M * (M - a), -a**2 * Q / r**2)
Hn = qq * a * (1 - r**2) / (2 * r)
Vn = a * (p - 1 + (p + 1) * r + 2 * t1)
factorization("E. Theorem 4, duals", "V_p - H_{p+1} has the sign of Q on the window", Vn - Hn,
              a * (m + p + 1) * (r - (m - p - 1) / (m + p + 1)) * Q / (2 * r * D),
              "the other factors are nonnegative on the window, so V_p >= H_{p+1} exactly when Q >= 0")

# ---------------------------------------------------------------------------
# F. Theorem 3 (three free producers) as a special case
# ---------------------------------------------------------------------------
identity("F. Theorem 3", "Q for m = 3, p = 1 is 3r^2 + 1", Q.subs({m: 3, p: 1}), 3 * r**2 + 1)
identity("F. Theorem 3", "window value for m = 3", Vn.subs({m: 3, p: 1}), 2 * a * (2 - r + 3 * r**2) / (1 + 3 * r))
identity("F. Theorem 3", "lambda_A for m = 3", lA.subs({m: 3, p: 1}), (M - 3 * a) / (2 * M))
identity("F. Theorem 3", "lambda_0 for m = 3", l0.subs({m: 3, p: 1}), (M**2 + 3 * a**2) / (2 * a * M))
t1_3, t2_3 = t1.subs({m: 3, p: 1}), (t1 - (1 - 2 * r)).subs({m: 3, p: 1})
identity("F. Theorem 3", "t2 = t1 - (1-2r) for m = 3", t2.subs({m: 3, p: 1}), t2_3)
uu = M * (1 + t1_3 - t2_3) / (2 * t1_3)
g1 = ((M - uu) * t1_3 - M * t2_3, -(M - uu), M)
g2 = (uu * t1_3, -uu, 0)
zz = (1, t1_3, t2_3)
identity("F. Theorem 3", "plane law: g1 vanishes at z", sum(g * w for g, w in zip(g1, zz)), 0)
identity("F. Theorem 3", "plane law: g2 vanishes at z", sum(g * w for g, w in zip(g2, zz)), 0)
# Signs used to remove the absolute values (r <= 1/3, t1 <= 1)
identity("F. Theorem 3", "plane law: first unit entry equals -a", g1[0], -a)
factorization("F. Theorem 3", "plane law: u <= M", M - uu, M * (t1_3 + t2_3 - 1) / (2 * t1_3),
              "nonnegative since t1 + t2 - 1 = 2(t1 - (1-r)) >= 0 below")
factorization("F. Theorem 3", "plane law: t1 >= 1 - r", t1_3 - (1 - r), (1 - r) * (1 - 3 * r) / (1 + 3 * r),
              "nonnegative for r <= 1/3")
factorization("F. Theorem 3", "plane law: g2 at the top-two coalition is nonpositive", g2[0] + g2[1], -uu * (1 - t1_3),
              "nonpositive since t1 <= 1")
factorization("F. Theorem 3", "plane law: g1 at the top-two coalition is nonpositive", g1[0] + g1[1],
              -(M - uu) * (1 - t1_3) - M * t2_3, "nonpositive since u <= M, t1 <= 1, t2 >= 0")
identity("F. Theorem 3", "plane law: unit cap", -g1[0] + g2[0], M)
identity("F. Theorem 3", "plane law: transitional cap", -g1[1] - g2[1], M)
identity("F. Theorem 3", "plane law: top-two coalition", -(g1[0] + g1[1]) - (g2[0] + g2[1]), 2 * a)
identity("F. Theorem 3", "plane law: face coalition", sum(g1) - (g2[0] + g2[1]), 3 * a)
factorization("F. Theorem 3", "plane law: g1 at the face coalition is nonnegative", sum(g1),
              M * (1 - t2_3) - (M - uu) * (1 - t1_3), "nonnegative since 1 - t2 >= 1 - t1 and M >= M - u")

# ---------------------------------------------------------------------------
# G. Theorem 2 (last depth): the four-line envelope
# ---------------------------------------------------------------------------
ai, aj = sp.symbols("a_i a_j", positive=True)
g1l, g2l = ai + t * aj, t * aj * (1 + 1 / r)
g3l, g4l = (1 - t) * aj * (1 / r - 1), (1 - t) * ai * (1 + 1 / r)
factorization("G. Theorem 2", "g4 <= g3 exactly when x <= (1-r)/(1+r)", g3l - g4l,
              (1 - t) * (aj * (1 - r) - ai * (1 + r)) / r, "sign of a_j(1-r) - a_i(1+r) for t < 1")
t14 = ai / (r * aj + (1 + r) * ai)
identity("G. Theorem 2", "g1 meets g4", g1l.subs(t, t14), g4l.subs(t, t14))
identity("G. Theorem 2", "third-regime value", g1l.subs(t, t14), ai * (1 + r) * (ai + aj) / (r * aj + (1 + r) * ai))
t13 = (1 - r) - r * ai / aj
identity("G. Theorem 2", "g1 meets g3", g1l.subs(t, t13), g3l.subs(t, t13))
identity("G. Theorem 2", "middle-regime value", g1l.subs(t, t13), (1 - r) * (ai + aj))
factorization("G. Theorem 2", "g1 <= g2 at the middle point", g2l.subs(t, t13) - g1l.subs(t, t13),
              (aj * (1 - r) - 2 * r * ai) / r, "nonnegative exactly when x <= (1-r)/(2r)")
identity("G. Theorem 2", "g2 meets g3 at t = (1-r)/2", g2l.subs(t, (1 - r) / 2), g3l.subs(t, (1 - r) / 2))
identity("G. Theorem 2", "first-regime value", g2l.subs(t, (1 - r) / 2), aj * (1 - r**2) / (2 * r))
factorization("G. Theorem 2", "g1 <= g2 at the third-regime point", g2l.subs(t, t14) - g1l.subs(t, t14),
              ai * (1 + r) * (aj * (1 - r) - r * ai) / (r * (r * aj + (1 + r) * ai)),
              "nonnegative when x <= (1-r)/r, implied by x <= (1-r)/(1+r)")
identity("G. Theorem 2", "continuity at x = (1-r)/(1+r)",
         (ai * (1 + r) * (ai + aj) / (r * aj + (1 + r) * ai) - (1 - r) * (ai + aj)).subs(ai, aj * (1 - r) / (1 + r)), 0)
identity("G. Theorem 2", "continuity at x = (1-r)/(2r)",
         ((1 - r) * (ai + aj) - aj * (1 - r**2) / (2 * r)).subs(ai, aj * (1 - r) / (2 * r)), 0)
factorization("G. Theorem 2", "no regime where g2 meets g4", (1 - r) / r - (1 - r) / (1 + r), (1 - r) / (r * (1 + r)),
              "positive for 0 < r < 1, so x >= (1-r)/r and x <= (1-r)/(1+r) cannot both hold")

# ---------------------------------------------------------------------------
# H. Theorem 5 and the cap-binding family, arbitrary shares
# ---------------------------------------------------------------------------
tC = (1 - r) - r * A / AJ
factorization("H. Theorem 5, C31", "unit caps", A - tC * AJ, A * (1 + r) - AJ * (1 - r),
              "nonnegative exactly when a(I) >= A_J(1-r)/(1+r)")
aK = sp.symbols("a_K", positive=True)
identity("H. Theorem 5, C31", "grand cost", aK + (1 - tC) * AJ / r, aK + A + AJ)
PhiC = T * (1 - tC * sig) / r + (AJ - T) * tC * sig / r - sig * A - T
bilinear("H. Theorem 5, C31", "slack bilinear in (sigma, a(T))", PhiC, sig, T)
identity("H. Theorem 5, C31", "corner (0,0)", PhiC.subs({sig: 0, T: 0}), 0)
identity("H. Theorem 5, C31", "corner (0,A_J)", PhiC.subs({sig: 0, T: AJ}), AJ * (1 / r - 1))
factorization("H. Theorem 5, C31", "corner (1,0)", PhiC.subs({sig: 1, T: 0}), (AJ * (1 - r) - 2 * r * A) / r,
              "nonnegative exactly when a(I) <= A_J(1-r)/(2r)")
identity("H. Theorem 5, C31", "corner (1,A_J)", PhiC.subs({sig: 1, T: AJ}), 0)
identity("H. Theorem 5, C31", "value (1-r)a(F)", A + tC * AJ, (1 - r) * (A + AJ))
Delta = AJ * (1 - r) / (2 * r)
kappaH = 1 - Delta / A
identity("H. Theorem 5, H", "unit singleton cost a_i", kappaH + Delta / A, 1)
identity("H. Theorem 5, H", "grand cost", kappaH * A + aK + AJ / r - Delta, aK + A + AJ)
PhiH = sig * kappaH * A + T / r - sig * T * (1 - r) / (2 * r) + sig * (Delta - T * (1 - r) / (2 * r)) - sig * A - T
identity("H. Theorem 5, H", "slack a(T)(1/r-1)(1-sigma)", PhiH, T * (1 / r - 1) * (1 - sig))
identity("H. Theorem 5, H", "value A_J(1-r^2)/(2r)", A + (1 - r) / 2 * AJ - kappaH * A, AJ * (1 - r**2) / (2 * r))
factorization("H. Theorem 5, H", "unit coefficients nonnegative", kappaH * A, A - AJ * (1 - r) / (2 * r),
              "nonnegative exactly when a(I) >= A_J(1-r)/(2r)")
tG = A / (r * AJ + (1 + r) * A)
lam = A / (r * tG * AJ)
identity("H. Theorem 5, G", "unit caps tight", lam * tG * AJ / A, 1 / r)
factorization("H. Theorem 5, G", "fractional caps", tG - A / AJ, A * (AJ * (1 - r) - (1 + r) * A) / (AJ * (r * AJ + (1 + r) * A)),
              "nonnegative exactly when a(I) <= A_J(1-r)/(1+r)")
identity("H. Theorem 5, G", "grand cost", aK + lam * AJ * (1 - tG), aK + A + AJ)
PhiG = lam * (T * (1 - tG * sig) + (AJ - T) * tG * sig) - sig * A - T
bilinear("H. Theorem 5, G", "slack bilinear in (sigma, a(T))", PhiG, sig, T)
identity("H. Theorem 5, G", "corner (0,0)", PhiG.subs({sig: 0, T: 0}), 0)
factorization("H. Theorem 5, G", "corner (0,A_J) via lambda >= 1", lam - 1, (1 + r) * A / (r * AJ),
              "positive, so lambda >= 1")
identity("H. Theorem 5, G", "corner (1,0)", PhiG.subs({sig: 1, T: 0}), A * (1 / r - 1))
identity("H. Theorem 5, G", "corner (1,A_J)", PhiG.subs({sig: 1, T: AJ}), 0)
identity("H. Theorem 5, G", "value reduces to the third regime of Theorem 2",
         (A + tG * AJ).subs({A: ai, AJ: aj}), ai * (1 + r) * (ai + aj) / (r * aj + (1 + r) * ai))

# ---------------------------------------------------------------------------
# I. Proposition 5 (mixtures) and window lengths
# ---------------------------------------------------------------------------
Pn = n * (n - 1) / 2
ssz, zeta, S_ = sp.symbols("s_scale zeta S_size", positive=True)
identity("I. Proposition 5", "pair mass at the minimal cut", (sp.Rational(9, 10) * ssz / Pn) * (n - 1), sp.Rational(9, 5) * ssz / n)
factorization("I. Proposition 5", "cut size |S|(n-|S|) >= n-1", S_ * (n - S_) - (n - 1), (S_ - 1) * (n - 1 - S_),
              "nonnegative for 1 <= |S| <= n-1")
for size in (3, 4, 5, 6):
    e = sp.eye(size)
    total = sp.zeros(size, size)
    for i in range(size):
        for j in range(i + 1, size):
            d = e[:, i] - e[:, j]
            total += d * d.T
    identity("I. Proposition 5", f"sum of pair outer products, n = {size}", total, size * sp.eye(size) - sp.ones(size, size))
kj, aj_ = sp.symbols("kappa_j a_jj", positive=True)
eps, mn = sp.symbols("epsilon mmin", positive=True)
identity("I. Proposition 5", "caps hold with equality at the binding producer",
         (1 - eps) * aj_ / ((1 - eps) / (1 / r - eps * kj)) + eps * kj * aj_, aj_ / r)
identity("J. windows", "window length between I_{p+1} and I_p",
         (m - 2 * p) / m - (m - p - 1) / (m + p + 1), 2 * (m - p - p**2) / (m * (m + p + 1)))


def main():
    failed = [c for c in CHECKS if not c["passed"]]
    output = ROOT / "results/verification/symbolic_checks.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"date": "2026-11-07", "sympy": sp.__version__,
                                  "checks": CHECKS}, indent=2) + "\n")
    groups = {}
    for c in CHECKS:
        groups.setdefault(c["group"], [0, 0])
        groups[c["group"]][0] += c["passed"]
        groups[c["group"]][1] += 1
    lines = ["# Symbolic verification of the proofs", "",
             f"2026-11-07, sympy {sp.__version__}. Generated by `scripts/verify_symbolic.py` from "
             "[symbolic_checks.json](symbolic_checks.json). Equalities are checked as identities; "
             "inequalities are reduced to factorizations whose sign is stated; polynomial positivity is "
             "checked through nonnegative coefficients after substituting the domain bounds.", "",
             f"**{len(CHECKS) - len(failed)} of {len(CHECKS)} checks pass.**", "",
             "| group | passed |", "| --- | ---: |"]
    for g, (ok, total) in groups.items():
        lines.append(f"| {g} | {ok} / {total} |")
    lines += ["", "## All checks", "", "| group | check | kind | result |", "| --- | --- | --- | :---: |"]
    for c in CHECKS:
        lines.append(f"| {c['group']} | {c['check']} | {c['kind']} | {'pass' if c['passed'] else 'FAIL'} |")
    lines += ["", "Not covered here: the convex-analysis lemmas (gauge duality, triangle certificates) and the "
              "general validity conditions of the transitional family for arbitrary shares, which is checked "
              "instance by instance in exact arithmetic.", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"{len(CHECKS) - len(failed)} of {len(CHECKS)} symbolic checks pass")
    for c in failed:
        print("FAILED:", c["group"], "|", c["check"], "|", c["detail"])
    return failed


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
