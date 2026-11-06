# Exact worst-case gaps under a standalone floor

November 6, 2026, branch `pulp-fiction`. Companion to
[seminorm_envelope.md](seminorm_envelope.md), whose notation and upper
bounds are used throughout. Code: `censored_newsvendor/exact_envelopes.py`;
checks: [results/exclusion/exact_envelopes.md](../results/exclusion/exact_envelopes.md).

The question is the one raised by C39: given positive shares w, an
exclusion depth k and a floor r on the standalone ratio rho, how large can
(D_k - B)/L be? Upper bounds were already available (C31, and Propositions 2
and 3 of the seminorm note). What was missing were demand laws that attain
them. This note gives explicit laws, and with them two exact results:

* **Theorem 1.** Equal shares, any n and any depth: the worst gap is known in
  closed form for every r outside a finite union of explicit "windows".
* **Theorem 2.** Arbitrary positive shares at the last nonterminal depth
  k = n-2 (for three producers, depth one): the worst gap is known in closed
  form for every r, with three regimes per ordered pair of producers.

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
to about 1.3). Inside a window the explicit laws found by the realizability
LP give lower bounds strictly below C31 at every sampled ratio, e.g. 31/56
against 9/16 for n = 4, r = 1/4. The exact window values are open.

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

`python scripts/check_exact_envelopes.py` verifies, in exact arithmetic,
1910 equal-share constructions (n = 3..10, every depth, r = k/60 outside the
windows) and 600 random rational instances of Theorem 2 (n = 3..6), compares
the closed forms with the upper bounds, and re-evaluates 111 of the laws with
the original audit code. `tests/test_exact_envelopes.py` contains fast
versions of the same checks.

## 5. What is settled and what is not

Settled: the worst gap for equal shares at every depth outside the windows,
and for arbitrary shares at depth n-2. In particular the elementary C31
ceiling is exact on the intervals I_p, and the only general improvement over
it for equal shares is the regime r >= (m-1)/(m+1) and the windows.

Open: the window values; arbitrary shares at depths 1..n-3 (for n >= 4);
asymmetric loss, where costs are no longer seminorms.
