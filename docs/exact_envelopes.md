# Exact worst-case gaps under a standalone floor

November 6, 2026, branch `pulp-fiction`. Companion to
[seminorm_envelope.md](seminorm_envelope.md), whose notation and upper
bounds are used throughout. Code: `censored_newsvendor/exact_envelopes.py`;
checks: [results/exclusion/exact_envelopes.md](../results/exclusion/exact_envelopes.md).

The question is the one raised by C39: given positive shares w, an
exclusion depth k and a floor r on the standalone ratio rho, how large can
(D_k - B)/L be? Upper bounds were already available (C31, and Propositions 2
and 3 of the seminorm note). What was missing were demand laws that attain
them. This note gives explicit laws, and with them the following exact results:

* **Theorem 1.** Equal shares, any n and any depth: the worst gap is known in
  closed form for every r outside a finite union of explicit "windows".
* **Theorem 2.** Arbitrary positive shares at the last nonterminal depth
  k = n-2 (for three producers, depth one): the worst gap is known in closed
  form for every r, with three regimes per ordered pair of producers.
* **Theorem 4.** Inside the windows the worst gap is the larger of two
  further explicit families, with a quadratic in r deciding which one wins
  (Section 5). Together with Theorem 1 this solves the equal-share case in
  closed form for every n, every depth and every r.
* **Section 6.** For arbitrary shares at any depth, a certificate LP and an
  explicit-law LP meet in every instance tried.
* **Asymmetric penalties.** [asymmetric_penalties.md](asymmetric_penalties.md)
  extends Theorem 2 to every ratio between the shortfall and surplus
  penalties (Theorem A) and Theorems 1 and 4 outside a set of windows that
  closes once the ratio reaches 2(m-1)/m (Theorem B).

Loss is symmetric absolute loss, L is normalized to 1, so a = w, and
rho >= r means c_j <= a_j/r for every producer.

## 1. Laws from generators

Take vectors g_1, ..., g_m in R^n. Let Y pick an index k uniformly and a
sign s uniformly and set Y = mu + s m g_k. Then x'Y is symmetric about x'mu,
so (Lemma 5 of the seminorm note)

$$
c(x)=\sum_{k=1}^m|g_k^\top x| .
$$

An affine change of units puts the law in the unit box without changing any
ratio, and the grand offer at the centre is optimal with L = c(1). So a value
V is attained at depth k as soon as the generators satisfy

* caps: c(e_j) <= a_j/r for every j (so rho >= r);
* stability: c(1_S) >= a(S) for every proper S (so B = 0);
* grand cost: c(1) = 1;
* witness: some z on a depth-k face has a'z - c(z) = V.

Every construction below is checked in exact rational arithmetic on all of
these conditions, for every coalition (`verify_generators`), and a sample of
the resulting laws is re-evaluated with the original `ExclusionEnvelope` and
`coalition_table` code.

## 2. Equal shares, any depth

Fix n >= 3, a depth 1 <= k <= n-2 and write m = n-k for the number of free
producers on a face. For p = 1, ..., m-1 put q = m-p and

$$
I_p=\Bigl[\max\Bigl(0,\frac{q-p}{q+p}\Bigr),\ \frac{q}{q+2p}\Bigr].
$$

**Theorem 1.** For equal shares and 0 < r <= 1,

$$
\sup_{\rho\ge r}\frac{D_k-B}{L}=
\begin{cases}
\dfrac{(1-r)\,m}{n}, & r\in I_1\cup\dots\cup I_{m-1},\\[6pt]
\dfrac{(m-1)(1-r^2)}{2nr}, & r\ge\dfrac{m-1}{m+1}.
\end{cases}
$$

Both values are attained by finite symmetric laws with at most n
generators. The two cases agree at r = (m-1)/(m+1), the right end of I_1.

The value depends on n and k only through m and the normalization 1/n.
For k = 1 and n = 3 this is C39. For k = n-2 (m = 2) the intervals cover
[0,1] and Theorem 1 is the equal-share case of Theorem 2.

*Upper bounds.* The first line is C31 at depth k, since the sum of the m
largest shares is m/n. The second is the separable bound: the proof of
Proposition 2 in the seminorm note uses only a face F, the coalitions
S subset of F and the caps, so it holds verbatim with |F| = m, giving
(m-1)(1-r^2)/(2nr) for r >= (m-1)/(m+1).

*Construction on I_p.* Put M = a/r with a = 1/n, take unit producers I
(|I| = p), fractional producers J (|J| = q) and excluded producers K
(|K| = k), and let

$$
t=(1-r)-\frac{pr}{q},\qquad
g_\ell=a\,e_\ell\ (\ell\in K),\qquad
g_j=\frac{Mt}{p}\mathbf 1_I-M e_j\ (j\in J),\qquad
z=\mathbf 1_I+t\mathbf 1_J .
$$

On I_p we have 0 <= t < 1. Every generator vanishes at z, so c(z) = 0 and
the witness value is a(p+qt) = a(p+q)(1-r) = (1-r)m/n. The caps hold:
c(e_j) = M on J, c(e_l) = a on K, and c(e_i) = qMt/p on I, which is at
most M exactly when r >= (q-p)/(q+p). Since 1-t = r(p+q)/q, the grand cost
is c(1) = ka + qM(1-t) = ka + (p+q)a = 1.

For stability, let S contain s unit, tau fractional and kappa excluded
producers. Because ts/p <= t < 1,

$$
c(\mathbf 1_S)=\kappa a+\tau M+(q-2\tau)\frac{Mts}{p},\qquad
c(\mathbf 1_S)-a|S|=\tau(M-a)+(q-2\tau)\frac{Mts}{p}-as=:\Phi(s,\tau).
$$

Phi is bilinear on [0,p] x [0,q], so its minimum is at a corner:
Phi(0,0) = 0, Phi(0,q) = q(M-a) >= 0, Phi(p,q) = qM(1-t) - a(p+q) = 0, and
Phi(p,0) = qMt - ap, which is nonnegative exactly when r <= q/(q+2p).
Hence every proper coalition is stable and B = 0. The two conditions on r
are the two ends of I_p.

*Construction for r >= (m-1)/(m+1).* Take one unit producer u, the other
q = m-1 free producers J, and

$$
\delta=\frac{M-a}2,\quad \beta=a-q\delta,\quad
g_0=\beta e_u,\quad g_\ell=a e_\ell\ (\ell\in K),\quad
g_j=\delta e_u-Me_j\ (j\in J),\quad z=e_u+\frac{1-r}2\mathbf 1_J .
$$

Here beta >= 0 exactly when r >= q/(q+2). Since M(1-r)/2 = delta, the
generators g_j vanish at z and c(z) = beta. The witness value is

$$
a\Bigl(1+q\frac{1-r}2\Bigr)-\beta=\frac q2\bigl(M-ar\bigr)=\frac{(m-1)(1-r^2)}{2nr}.
$$

Caps: c(e_j) = M, c(e_u) = beta + q delta = a, c(e_l) = a. Grand cost:
c(1) = beta + ka + q(M - delta) = a(1+k+q) = 1. If u is in S, then
c(1_S) = beta + kappa a + tau(M-delta) + (q-tau)delta = a(1+kappa+tau) = a|S|;
otherwise c(1_S) = kappa a + tau M >= a|S|. So B = 0. QED.

**The windows.** Ratios r < (m-1)/(m+1) outside every I_p are not covered.
The left end of I_p is (m-2p)/m and the right end of I_{p+1} is
(m-p-1)/(m+p+1), so a window separates them exactly when p^2+p < m, and its
length is 2(m-p-p^2)/(m(m+p+1)). At depth one (m = n-1):

| n | windows |
| ---: | --- |
| 3 | none |
| 4 | (1/5, 1/3) |
| 5 | (1/3, 1/2) |
| 6 | (3/7, 3/5) |
| 8 | (2/5, 3/7), (5/9, 5/7) |

Their total length is not small for moderate n: about 0.13 to 0.20 for
4 <= n <= 30 (0.16 at n = 30), and it decays only like n^(-1/2) (computed
values: 0.11 at n = 100, 0.04 at n = 1000; the product with sqrt(n) tends
to about 1.3). Inside a window the worst gap is strictly below C31, e.g.
31/56 against 9/16 for n = 4, r = 1/4; Theorem 4 in Section 5 gives the
exact window values.

## 3. Arbitrary shares at the last nonterminal depth

At depth k = n-2 every face has exactly two free producers. For an ordered
pair (i, j), i the unit producer and j the fractional one, write
x = a_i/a_j and

$$
\Phi_{ij}(r)=
\begin{cases}
\dfrac{a_j(1-r^2)}{2r}, & x\ge\dfrac{1-r}{2r},\\[6pt]
(1-r)(a_i+a_j), & \dfrac{1-r}{1+r}\le x\le\dfrac{1-r}{2r},\\[6pt]
\dfrac{a_i(1+r)(a_i+a_j)}{ra_j+(1+r)a_i}, & x\le\dfrac{1-r}{1+r}.
\end{cases}
$$

The three expressions agree on the boundaries.

**Theorem 2.** For n >= 3, positive shares and 0 < r <= 1,

$$
\sup_{\rho\ge r}\frac{D_{n-2}-B}{L}=\max_{i\ne j}\Phi_{ij}(r),
$$

attained by a finite symmetric law with n-1 or n generators.

*Upper bound.* Proposition 3 of the seminorm note uses only nonnegative
cost, the singleton {i}, the pair {i,j} and the caps of i and j, so it holds
at depth n-2 for every n (directly checked coalitions there have size at
least three and excess at most B). It bounds the gap by the best point of the
lower envelope of the increasing lines g1 = a_i + t a_j and
g2 = t a_j(1+1/r) and the decreasing lines g3 = (1-t)a_j(1/r-1) and
g4 = (1-t)a_i(1+1/r). Now g4 <= g3 for all t exactly when x <= (1-r)/(1+r).
In that case g4 meets g1 at t = a_i/(r a_j + (1+r)a_i), where g1 <= g2, and
the value is the third line of Phi. Otherwise g3 is the decreasing envelope:
it meets g1 at t = (1-r) - rx, where g1 <= g2 exactly when x <= (1-r)/(2r),
giving (1-r)(a_i+a_j), and otherwise it meets g2 at t = (1-r)/2, giving
a_j(1-r^2)/(2r).

*Constructions.* Each excluded producer l gets the generator a_l e_l, so
c(1_S) = a(S minus {i,j}) + P(S cap {i,j}) for the cost P of the
remaining "pair" generators. Stability, caps and the grand cost therefore
reduce to P(e_i) in [a_i, a_i/r], P(e_j) in [a_j, a_j/r] and
P(e_i+e_j) = a_i+a_j. Write M_i = a_i/r and M_j = a_j/r.

* Regime x >= (1-r)/(2r): with delta = (M_j - a_j)/2 <= a_i, the pair
  generators are (a_i - delta)e_i and delta e_i - M_j e_j, and
  z = e_i + ((1-r)/2)e_j. Then P(e_i) = a_i, P(e_j) = M_j,
  P(e_i+e_j) = a_i + M_j - 2 delta = a_i + a_j, c(z) = a_i - delta, and
  a'z - c(z) = (M_j - r a_j)/2 = a_j(1-r^2)/(2r).
* Middle regime: t = (1-r) - rx and the single pair generator
  M_j t e_i - M_j e_j, with z = e_i + t e_j. Then P(e_i) = M_j t lies in
  [a_i, M_i] exactly on this regime, P(e_j) = M_j,
  P(e_i+e_j) = M_j(1-t) = a_j(1+x) = a_i + a_j, c(z) = 0 and the value is
  a_i + t a_j = (1-r)(a_i+a_j).
* Regime x <= (1-r)/(1+r): t = a_i/(r a_j + (1+r)a_i), c_j = M_i/t and the
  pair generator M_i e_i - c_j e_j, with z = e_i + t e_j. Here
  c_j <= M_j because t >= x on this regime, (1-t)/t = r(a_i+a_j)/a_i gives
  P(e_i+e_j) = c_j(1-t) = a_i + a_j, and c(z) = 0. The cap of i is tight.

QED.

With equal shares x = 1, only the first two regimes occur, and Theorem 2
gives (1-r)2/n for r <= 1/3 and (1-r^2)/(2nr) above, in agreement with
Theorem 1 at m = 2. For three producers it extends C39 to arbitrary shares.
For example, w = (3/5, 1/4, 3/20) and r = 1/5 give 17/28 = 0.607143, in the
third regime with i the producer of share 1/4 and j the producer of share
3/5. The C39 inequalities alone would give 0.68.

## 4. Checks

**Symbolic verification.** `scripts/verify_symbolic.py` checks the algebra
of every proof in this note with sympy, for general sizes rather than at
sample points: 134 checks, all passing
([report](../results/verification/symbolic_checks.md)). Equalities are
checked as identities; each inequality is reduced to a factorization whose
sign is stated; the positivity needed for t_2 >= 0 is checked through
nonnegative polynomial coefficients after substituting the window bounds. Not
covered: the short convex-analysis lemmas and the general conditions of the
transitional family for arbitrary shares.

**Exact checks at sample points.**

`python scripts/check_exact_envelopes.py` verifies, in exact arithmetic,
1910 equal-share constructions (n = 3..10, every depth, r = k/60 outside the
windows) and 600 random rational instances of Theorem 2 (n = 3..6), compares
the closed forms with the upper bounds, and re-evaluates 111 of the laws with
the original audit code. `tests/test_exact_envelopes.py` contains fast
versions of the same checks.

## 5. Inside the windows

Two further families of explicit laws close the windows. Throughout, equal
shares a = 1/n, m free producers, unit producers I (|I| = p), excluded
producers K and M = a/r.

**Family H_p (positive cost at the witness).** For q = m-p >= 1 and
(m-p)/(m+p) <= r <= 1 put delta = M(1-r)/2 and
beta = ((p+q)a - qM(1+r)/2)/p, and take the generators beta e_i (i in I),
a e_l (l in K) and (delta/p)1_I - M e_j for the q fractional producers j, with
witness z = 1_I + ((1-r)/2) 1_J. The fractional generators vanish at z, so
c(z) = p beta and the witness value is

$$
H_p(r)=a\Bigl(p+q\frac{1-r}2\Bigr)-p\beta=\frac{(m-p)(1-r^2)}{2nr}.
$$

The unit singletons cost exactly a, the fractional ones M, and the grand cost
is 1. For a coalition with s unit, tau fractional and kappa excluded
producers, c(1_S) - a|S| = s beta + tau(M-a) + (q-2tau) delta s/p - as, which
is bilinear and nonnegative at the four corners (the corners (p,0) and (p,q)
give exactly zero). beta >= 0 is the condition on r. At r = (m-p)/(m+p),
the right end of I_p, beta = 0 and H_p equals C31: H_p continues the C31
plateau of configuration p beyond I_p. For p = 1 it is the high-regime law of
Theorem 1.

**Family V_p (a producer in transition).** Suppose p^2+p < m, so that a
window separates I_{p+1} from I_p, and write q' = m-p-1 and
r_L = (m-p-1)/(m+p+1), r_R = (m-2p)/m for its ends. For r_L <= r <= r_R put

$$
t_1=\frac{(p+1)(1-r)}{2(p+1)-m(1-r)},\qquad t_2=\frac{(p+1)r-1+t_1}{q'} ,
$$

$$
\gamma=\frac{M(p+1)(1-r)}{2p},\qquad
\alpha=\frac{M\bigl((p-1)+(p+1)r\bigr)}{2q'},\qquad
\beta=\frac{M\bigl(m(1-r)-2p\bigr)}{2q'},\qquad
\delta=-\frac{M\bigl(2(p+1)-m(1-r)\bigr)}2 .
$$

One free producer, marked *, is in transition. The generators are
(alpha/p)1_I + beta e_* - M e_j for each of the q' other fractional producers
j, gamma 1_I + delta e_*, and a e_l for the excluded producers; the witness is
z = 1_I + t_1 e_* + t_2 1_{J'}. Then

$$
V_p(r)=\frac1n\bigl(p-1+(p+1)r+2t_1\bigr).
$$

*Verification.* On the window alpha, beta, gamma >= 0 and delta <= 0
(beta >= 0 is r <= r_R; delta <= 0 is r >= (m-2p-2)/m, which follows from
r >= r_L). Every generator vanishes at z: gamma p + delta t_1 = 0 by the
choice of t_1, and alpha + beta t_1 - M t_2 = 0 reduces to the same identity.
So c(z) = 0 and the witness value is a'z = V_p. All free singletons cost
exactly M: q'alpha/p + gamma = M on I, q'beta + |delta| = M at *. Since
alpha + beta = M(1-r)/2, the grand cost is
q'M(1+r)/2 + gamma p(1-t_1)/t_1 + ka = mMr + ka = 1. For stability write
w = alpha s/p + beta iota, where s counts unit producers and iota is 1 if
* belongs to S; then w <= M(1-r)/2 < M and

$$
c(\mathbf 1_S)-a|S|=\tau(M-a)+(q'-2\tau)w+|\gamma s+\delta\iota|-a(s+\iota),
$$

bilinear in (s, tau) for each iota. Its eight corners are 0, q'(M-a),
p(M-a) and a((m-p)/r-(m+p)) for iota = 0, and M-a, a(p/r+p), 0 and 0 for
iota = 1; all are nonnegative because r_R <= (m-p)/(m+p). Finally the witness
is admissible: t_1 <= 1 is r >= r_L, and t_2 >= 0 amounts to the quadratic
(p+1)m s^2 - (pm+(p+1)(2p+1))s + 2p(p+1) >= 0 in s = 1-r. It is
nonnegative at both ends of the window, and its vertex lies to the right of
the window when p >= 2, or when p = 1 and m >= 6; for p = 1 and m <= 5 its
discriminant (m-2)(m-18) is negative.

**Certificates.** Sort the free coordinates of a witness,
1 = z_1 >= ... >= z_m. For every top-s coalition S and scale nu = z_t,

$$
\nu\,c(\mathbf 1_S)\le c(z)+M\sum_{i\le s}|z_i-\nu|+M\sum_{i>s}z_i ,
\qquad c(\mathbf 1_S)\ge sa-B ,
$$

and since nu <= 1 the integer excess only weakens the bound. Four of these
suffice in the window between I_{p+1} and I_p. With Z_I the sum of the p
largest coordinates, u = z_{p+1} and Y the sum of the remaining q', they read

$$
\begin{aligned}
F_0&=a(Z_I+u+Y),\\
F_A&=a(Z_I+u+Y)-(p+1)a+M\bigl[(p-Z_I)+(1-u)+Y\bigr]\quad(\text{top }p+1,\ \nu=1),\\
F_B&=a(Z_I+u+Y)-mau+M\bigl[Z_I-pu+q'u-Y\bigr]\quad(\text{top }m,\ \nu=u),\\
F_{B'}&=a(Z_I+u+Y)-ma+M\bigl[(p-Z_I)+(1-u)+q'-Y\bigr]\quad(\text{top }m,\ \nu=1),
\end{aligned}
$$

each an upper bound on (D_k - B)/L at that witness, valid on the sorted
region, where in particular Z_I <= p and u <= 1.

**Theorem 4 (windows).** Let p^2+p < m, r_L <= r <= r_R and

$$
Q(r)=mr^2+2(p-1)r+2+2p-m .
$$

Then the worst gap is V_p(r) if Q(r) >= 0 and H_{p+1}(r) if Q(r) <= 0;
equivalently, it is max(V_p(r), H_{p+1}(r)), because
V_p - H_{p+1} = a(m+p+1)(r - r_L) Q(r) / (2rD) with D = 2(p+1) - m(1-r) > 0
on the window.

*Proof.* The lower bounds are the two laws above (H_{p+1} is available since
r >= r_L = (m-p-1)/(m+p+1)). For the upper bounds we combine the certificates
with nonnegative weights so that every variable cancels.

If Q(r) >= 0, take weights proportional to

$$
\lambda_B=1,\qquad \lambda_A=\frac{M(m-2p)-ma}{2M},\qquad
\lambda_0=\frac{M^2(2+2p-m)+2aM(p-1)+ma^2}{2aM},
$$

together with the multiplier lambda_B (M(2+2p-m)+am) on the constraint
p - Z_I >= 0. The coefficients of Z_I, u and Y cancel; lambda_A >= 0 is
r <= r_R, lambda_0 >= 0 is Q(r) >= 0 (it equals a^2 Q(r)/r^2 up to the
factor 1/(2aM)), and the last multiplier is nonnegative because
r >= r_L >= (m-2p-2)/m. The resulting constant is the common value of the
three certificates at the witness of V_p, which is V_p(r).

If Q(r) <= 0, take lambda_A = (M-a)/(2M) and split the remaining weight
(M+a)/(2M) between F_B and F_{B'}, with F_B receiving lambda_B; add
multipliers (a-M) + 2M lambda_B on p - Z_I >= 0 and
(a-M) + lambda_B (M(m-2p)-ma) on 1 - u >= 0. The coefficient of Y cancels by
the choice of lambda_A, and those of Z_I and u by the choice of the
multipliers. Both multipliers are nonnegative and lambda_B stays below
(M+a)/(2M) for some lambda_B exactly when

$$
\frac{M-a}{M(m-2p)-ma}\le\frac{M+a}{2M},
$$

which rearranges to Q(r) <= 0. The constant is the common value of the three
certificates at the witness of H_{p+1} (Z_I = p, u = 1, Y = q'(1-r)/2),
which is H_{p+1}(r). QED.

For m = 3 one has Q(r) = 3r^2+1 > 0, so V_1 is the answer throughout the
window; that is Theorem 3 below, proved first and kept for its explicit
three-certificate argument. Numerically, the switching rule and the
admissibility of the witnesses hold at all 129,888 window ratios checked in
exact arithmetic for m = 3..300, and the closed form agrees with the
certificate LP at every ratio tested.

**Corollary (equal shares, complete).** For equal shares, every n >= 3, every
depth k <= n-2 and every 0 < r <= 1, the worst gap (D_k - B)/L is given in
closed form by Theorems 1 and 4: C31 on the intervals I_p, H_1 above
(m-1)/(m+1), and max(V_p, H_{p+1}) in each window. It is attained by an
explicit finite symmetric demand law with at most n generators
(`equal_share_exact_value` in the code).

**Theorem 3 (three free producers).** For equal shares with m = 3 free
producers, i.e. depth n-3, and 1/5 <= r <= 1/3,

$$
\sup_{\rho\ge r}\frac{D_{n-3}-B}{L}=\frac{2(2-r+3r^2)}{n(1+3r)} .
$$

*Proof.* The lower bound is V_1. For m = 3 its law has generators
g_2 = (u t_1, -u, 0) and g_1 = ((M-u)t_1 - Mt_2, -(M-u), M) on the free
coordinates, with u = M(1+t_1-t_2)/(2t_1), plus a e_l on the excluded
producers: since c(z) = 0, the cost is a norm on the plane orthogonal to z,
where every centrally symmetric polygon is a zonotope. For the upper bound
take a sorted witness (1, t_1, t_2) and three certificates: nonnegative cost;
the top-two coalition with nu = 1, giving gap <= a(t_1+t_2-1) + M(1-t_1+t_2);
and the face coalition scaled by nu = t_1, giving
gap <= a(1-2t_1+t_2) + M(1-t_2). Their gradients in (t_1, t_2) are (a,a),
(a-M, a+M) and (-2a, a-M), and

$$
\lambda_A=\frac{M-3a}{2M}\lambda_B,\qquad
\lambda_0=\frac{M^2+3a^2}{2aM}\lambda_B
$$

combine them to zero with nonnegative weights exactly when M >= 3a, i.e.
r <= 1/3. So the maximum of the three-way minimum is the point where all
three are equal, t_1 = 2(1-r)/(1+3r), t_2 = t_1-(1-2r), with value
a(1+t_1+t_2). It lies in the sorted region when r >= 1/5. QED.

In particular, for four producers at depth one the exact worst gap is

$$
\frac{3(1-r)}{4}\ \ (0<r\le 1/5),\qquad
\frac{2-r+3r^2}{2(1+3r)}\ \ (1/5\le r\le 1/3),
$$

$$
\frac{3(1-r)}{4}\ \ (1/3\le r\le 1/2),\qquad
\frac{1-r^2}{4r}\ \ (1/2\le r\le 1).
$$

The [window checks](../results/exclusion/window_envelopes.md) compare the
best explicit law with the certificate LP at 324 ratios (n = 4..12, depths 1
to 3): they agree to 1e-9 everywhere.

## 6. Arbitrary shares at any depth: two LPs

Without symmetry the certificate idea still works, at the price of
enumerating orderings. Fix a face F (the producers not excluded at depth k),
the producer u that carries the largest coordinate of the witness (scaled to
one) and a decreasing order of the others. For every coalition S inside F and
every scale nu = z_t with t in F,

$$
\nu\,c(\mathbf 1_S)\le c(z)+\sum_{i\in S}\frac{a_i}{r}\,|z_i-\nu|+\sum_{i\in F\setminus S}\frac{a_i}{r}\,z_i ,
\qquad c(\mathbf 1_S)\ge a(S)-B ,
$$

and nu <= 1, so B only weakens the bound. With the order fixed every
certificate is linear, and maximizing the minimum of all of them and of a'z
is one LP; the largest value over faces, units and orders bounds
(D_k - B)/L for every demand law (`censored_newsvendor.certificates`). For
equal shares it reduces to the bound of Section 5, and it reproduces
Theorems 1 to 3 wherever they apply (checked at 40 random last-depth
instances and on the four-producer curve).

The bound is useful because it can be matched from below. Evaluating the exact
seminorm relaxation (Lemma 1 of the seminorm note) at the LP's maximizer shows
whether the relaxed envelope reaches it; the zonotope LP then builds a finite
symmetric law at that membership, which the original audit code evaluates.

**Random instances** ([results](../results/exclusion/certificate_method.md)).
In 68 of 68 instances with random shares (n = 4, 5, 6; depths 1 to 3) the
certificate bound equals the relaxation at its maximizer, so the relaxed worst
gap is determined. In all 38 instances where an explicit law was built (every
four-producer instance and two five-producer ones) the law reaches the bound,
so there the worst gap over demand laws is determined.

**When the elementary ceiling is the answer**
([summary](../results/exclusion/c31_exactness.md)). Comparing the same 68
values with C31, the ceiling (1-r) times the sum of the n-k largest shares, is
exact in 45 of them. The pattern is sharp: all 39 instances with r <= 0.4 sit
exactly at C31, 6 of 14 with r in {0.5, 0.6}, and none of the 15 with
r >= 0.7, where the exact value is often far lower (0.187 against 0.26 for
four producers at depth two and r = 0.6). At the optimum only two
certificates are typically active in the C31 cases, nonnegative cost and the
whole face, which is exactly the argument behind C31. The equal-share windows
at moderate r thus look like a feature of symmetric shares; with generic
shares the elementary ceiling is the answer for small and moderate r, and the
exact theory matters for large r.

**Two explicit families for arbitrary shares.** The equal-share
constructions generalize once the unit producers' coefficients are taken
proportional to their shares. Fix an excluded set K, unit producers I and
fractional producers J (so F = I + J), and write a(I), A_J for their share
totals.

**Theorem 5.** For arbitrary positive shares and any depth k, the worst gap
is at least the largest of the following values over all K and partitions
F = I + J with I and J nonempty:

$$
(1-r)\,a(F)\quad\text{if}\quad \frac{1-r}{1+r}A_J\le a(I)\le\frac{1-r}{2r}A_J,
\qquad
\frac{A_J(1-r^2)}{2r}\quad\text{if}\quad a(I)\ge\frac{1-r}{2r}A_J .
$$

*Proof.* For the first value take t = (1-r) - r a(I)/A_J, generators a_l e_l
for l in K and, for each j in J, the vector with entries
(a_j/r) t a_i/a(I) on the unit producers and -a_j/r at j; the witness is
1_I + t 1_J and c(z) = 0. The unit caps reduce to t A_J <= a(I), the lower
condition; the grand cost is a(K) + (1-t)A_J/r = 1. With sigma the unit share
fraction of a coalition and a(T) its fractional share, c(1_S) - a(S) is
bilinear in (sigma, a(T)) on [0,1] x [0, A_J], with corner values 0,
A_J(1/r-1), A_J t/r - a(I) >= 0 (the upper condition) and 0. For the second
value take Delta = A_J(1-r)/(2r), generators (1 - Delta/a(I)) a_i e_i on the
units, a_l e_l on K and, for each j in J, entries (a_j/r)((1-r)/2) a_i/a(I)
on the units and -a_j/r at j; the witness is 1_I + ((1-r)/2)1_J. The
condition makes the unit coefficients nonnegative, every unit singleton costs
exactly a_i, the grand cost is 1, and c(1_S) - a(S) = a(T)(1/r-1)(1-sigma)
>= 0. QED.

For equal shares these are the intervals I_p and the family H_p; at depth n-2
they are the second and first regimes of Theorem 2. In the 68 random instances
the larger of the two values equals the exact worst gap 67 times; the
exception (five producers with shares 0.045, 0.409, 0.409, 0.091, 0.045 at
r = 0.6, value 0.306 against 0.291) needs a transitional family like V_p or the
third regime of Theorem 2. Every construction was checked in exact
arithmetic on those 68 instances, and again in the 1000-instance check below.

**Two more families, and a conjectured closed form.** Two further mechanisms
complete the picture; both reduce to known cases.

* *Cap-binding family G* (the third regime of Theorem 2 when F has two
  producers). If a(I) <= A_J(1-r)/(1+r), put t = a(I)/(rA_J + (1+r)a(I)) and,
  for each j in J, c_j = a_j a(I)/(r t A_J) and the generator with entries
  c_j t a_i/a(I) on the units and -c_j at j, plus a_l e_l on K. The witness
  1_I + t 1_J has zero cost, the unit caps are tight, the grand cost is 1, and
  with sigma and a(T) as above c(1_S) - a(S) is bilinear with corner values
  0, A_J(lambda-1), a(I)(1/r-1) and 0, where lambda = a(I)/(r t A_J) >= 1.
  The value is a(I) + t A_J.
* *Transitional family V* (the family V_p when shares are equal). Units I,
  one producer * in transition and fractional producers J' at a common level,
  with t_1 = (1-r)(a(I)+a_*)/(r a(F) + a(I) + a_* - A_J'),
  t_2 = (r(a(I)+a_*) - (1-t_1)a_*)/A_J' and value
  a(I)(1+r) - a_*(1-r) + 2 t_1 a_*. The generators follow V_p with unit
  coefficients proportional to shares (`general_transitional_candidates`).
  Here we have not written general conditions; each candidate is kept only
  after an exact check of every constraint.

**Conjecture 6 (closed form for arbitrary shares).** For symmetric absolute
loss, positive shares, any depth k and 0 < r <= 1, the worst gap
(D_k - B)/L equals the largest value of the families C31, H, G and V over
all excluded sets K and all splits of the remaining producers.

Evidence ([results](../results/exclusion/general_formula.md)): in 1000 random
instances (n = 3..6, random depth and r) the best explicit law is valid in
exact arithmetic and its value equals the certificate bound, which holds for
every demand law, in all 1000; the attaining families are C31 (482), H (467),
V (27) and G (24). The same holds for the 68 instances above. Since every
value is attained by an explicit law, the conjecture concerns only the upper
bound: that the certificate LP never exceeds the best family.

The number of LPs grows like C(n,k)(n-k)!, so the method is practical up to
six or seven producers. For larger n with structure, such as equal shares,
the sorted version of Section 5 needs a single LP.

### Toward a proof of Conjecture 6 for three free producers

For four producers at depth one (three free producers per face), the dual
solution of the certificate LP at the optimum was recorded on 500 random
instances ([active_certificates.md](../results/exclusion/active_certificates.md)).
At most three certificates are ever active, and they are always of the types
that prove the equal-share windows: zero cost, a top set at level one, and the
whole face at level one or at the level of a fractional producer. Each family
has its own pattern. The transitional family V uses zero cost, the top two at
level one and the whole face at the level of the second producer, in 27 of 27
instances. H mostly uses three top-type sets at level one, C31 uses zero cost
and the whole face, and G uses zero cost and the whole face at the level of
the third producer. This suggests that the proof of Theorem 4 (dual weights
on four certificates, regime by regime) can be carried over to three free
producers with arbitrary shares. The missing ingredient is the general
validity condition of the transitional family, which is still checked
instance by instance.

**Lemma (transitional regime, three free producers).** Let a face have three
free producers u, b, c and consider memberships with z_u = 1 >= z_b = y >=
z_c = w >= 0. With P_i = a_i(1+r)/r, Q_i = a_i(1-r)/r and
D = r(a_u + a_b + a_c) + a_u + a_b - a_c > 0, put

    lambda_B = 2 a_b r / D,
    lambda_C = r((1-r)(a_b + a_c) - (1+r)a_u) / D,
    lambda_L = ((1+r)^2 a_u + (1-r)^2 a_b - (1-r^2) a_c) / D.

They sum to one, and lambda_L L + lambda_C C + lambda_B B is the constant
V(u; b; c) = a_u(1+r) - a_b(1-r) + 2 t_1 a_b, where L = a'z is the zero-cost
bound, C = Q_b(1-y) + P_c w the certificate of {u, b} at level one, and
B = P_u(1-y) + Q_c(y-w) the certificate of the whole face at level y (group N
of the symbolic checks). Hence, whenever a_u(1+r) <= (1-r)(a_b + a_c) and
(1+r)^2 a_u + (1-r)^2 a_b >= (1-r^2) a_c, the excess of every such membership
is at most V(u; b; c), the value of the transitional family. Where the family
is also valid, it is the exact worst case on that ordering.

**Lemma (large top producer).** For the same face and any membership with
z_u = 1 (no ordering needed), zero cost and the whole face at level one with
weights (1-r, r) give the bound (1-r)T, and the sets {u, b}, F and {u, c} at
level one with weights ((1-r)/2, r, (1-r)/2) give H_u = (a_b + a_c)(1-r^2)/(2r)
(group N). If a_u(1+r) >= (1-r)(a_b + a_c), the two-block value with units
{u} is exactly min{(1-r)T, H_u}, attained by the C31 or H family. So every
ordering whose top producer is not small satisfies Conjecture 6.

**Where the proof stands** ([three_producers.md](../results/exclusion/three_producers.md),
400 random instances, 2400 orderings, none exceeding the best family on the
face). Orderings with a large top producer, 1490 of them, are covered by the
lemma. For a small top producer with D > 0 and lambda_L >= 0 (684), the
transitional certificate holds; it is tight in the 218 orderings where the
transitional law is valid, and elsewhere the true value is lower and comes
from other certificates. The other small-top orderings (146 with
lambda_L < 0, 80 with D <= 0) use, in all observed cases, zero cost and the
whole face at the level of the second or third producer, sometimes with
{u, b} at the level of the second. Their dual weights and a covering argument
are what remains for a proof with three producers.

**Two more combinations** (group N), valid on explicit regions: zero cost and
the whole face at the level of the third producer, together with the
constraint z_b <= 1, give the two-block value G for units {u, b}. The weights
are always nonnegative, so this bound is the exact value when {u, b} is in the
unit-cap regime. The sets {u, b} and F at the level of the second producer,
with the same constraint, give H for units {u, b}, a_c(1-r^2)/(2r), whenever
a_c(1-r) >= 2a_u. With the ceiling, H_u and the transitional bound this makes
five explicit bounds. In 2393 of the 2400 sampled orderings the smallest of
them is at or below the best family value, which proves Conjecture 6 on those
orderings. The other 7 satisfy the conjecture too, but need further
combinations, and a proof for all shares still needs an analytic argument
that the regions where these bounds are tight cover every case.

**Proposition T (three free producers).** Fix a face with three free
producers and an ordering u, b, c of its memberships, z_u = 1 >= z_b >= z_c.
Unless

    a_u(1+r) < (1-r)(a_b + a_c),   2r(a_u + a_b) > (1-r)a_c   and   (1-r)a_c < 2a_u,

the excess of every membership with that ordering is at most the value of a
two-block family that is attained by an explicit law. If the top producer
is not small, the bound is min{(1-r)T, H_u}, the value for units {u}.
Otherwise the block {u, b} is in one of three regimes. In the unit-cap
regime the bound G_ub is its value; in the ceiling window the ceiling
(1-r)T is its value; and in the H regime with (1-r)a_c >= 2a_u the bound
H_ub is its value. So Conjecture 6 holds for three free producers whenever
no ordering of any face falls in the single open region above. In our
sample 2028 of 2400 orderings lie outside it, and inside it the five bounds
settle 365 of 372 numerically ([three_producers.md](../results/exclusion/three_producers.md)).

## 7. Strict stability and positive definite covariance

The worst-case laws above make some coalition constraints hold with
equality and have singular covariance. Neither is needed for the suprema.

**Proposition 5.** For 0 < r < 1, every supremum in Theorems 1, 2 and 4 is
unchanged if the demand law must in addition have positive definite
covariance and strictly negative excess for every proper coalition. The same
holds for every value attained by a finite symmetric law in Section 6. The
supremum is then approached, not attained.

*Proof.* Let X^s put mass 0.9/P on the atoms +-s(e_i - e_j), spread evenly
over the P = n(n-1)/2 pairs, and mass 0.1 on +-zeta 1. Its cost is

$$
c^s(\mathbf 1_S)=\frac{0.9\,s}{P}\,|S|(n-|S|)+0.1\,\zeta|S| ,
$$

so with 1.8 s/n > 1 every proper coalition has c^s(1_S) > a(S) (because
|S|(n-|S|) >= n-1 and a(S) < 1), while c^s(1) = 0.1 zeta n <= 1 for small
zeta. Its covariance is positive definite: (e_i - e_j) span the complement of
1, and the last atoms cover 1. Fix eps in (0,1), let kappa_j = c^s(e_j)/a_j and
take the worst-case law X at the ratio

$$
r'=\frac{1-\varepsilon}{\min_j\,(1/r-\varepsilon\kappa_j)} ,
$$

which tends to r and lies in (0,1] for small eps since r < 1. Mix the two laws
with weights 1-eps and eps. Both are centrally symmetric about the origin, so
the mixture is too, and its cost is (1-eps)c_X + eps c^s at every
membership. Hence

* every proper coalition is strictly stable: (1-eps)(c_X(1_S)-a(S)) >= 0 and
  eps(c^s(1_S)-a(S)) > 0;
* the standalone caps hold at r, by the choice of r';
* the grand cost is at most one, so L = 1 is kept by the frozen offer;
* the covariance is at least eps times that of X^s;
* at the witness z of X the excess is at least (1-eps)V(r') - eps c^s(z),
  which tends to the worst gap V(r) because the closed forms are continuous.

Mapping the mixture into the unit box changes none of these. QED.

The [mixture checks](../results/exclusion/strict_mixtures.md) build such laws
for a four- and a five-producer window, the four-producer high regime and the
three-producer example of Theorem 2, at eps = 0.05, 0.01 and 0.002, and
evaluate them with the original audit code: every mixed law has strictly
negative excess, positive definite covariance and rho >= r, and its gap
approaches the exact value (for four producers at r = 1/4: 0.4707, 0.5370,
0.5503 against 31/56 = 0.5536).

## 8. What is settled and what is not

Settled with proofs: equal shares, every n, every depth and every r
(Theorems 1 and 4, with Theorem 3 as the three-producer special case);
arbitrary positive shares at depth n-2 (Theorem 2). Every value comes with an
explicit finite demand law, and for r < 1 the same suprema hold under strict
stability and positive definite covariance (Proposition 5).

Determined computationally for arbitrary shares: every one of 68 random
instances with up to six producers (relaxed worst gap), and the 38 of them
where an explicit law was built (worst gap over demand laws).

Proved as a lower bound for arbitrary shares at every depth: the families
of Theorem 5 and the cap-binding family G; the transitional family V is
verified instance by instance. Conjecture 6 says their maximum is the exact
worst gap; it held in all 1068 random instances computed.

Open: a proof of Conjecture 6 (an upper-bound argument for arbitrary shares,
as Theorem 4 gives for equal shares) and general conditions for the family V;
a proof of the realizability conjecture; asymmetric loss, where costs are no
longer seminorms.
