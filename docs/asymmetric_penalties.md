# Asymmetric imbalance penalties

November 7, 2026, branch `pulp-fiction`. Companion to
[exact_envelopes.md](exact_envelopes.md), whose notation is used throughout.
Code: `censored_newsvendor/asymmetric.py` (plus a `kappa` argument in
`minimal_cost` and `certificate_bound`); checks:
[results/asymmetric/asymmetric_checks.md](../results/asymmetric/asymmetric_checks.md)
and group K of [the symbolic report](../results/verification/symbolic_checks.md).

Everything so far assumed that a surplus and a shortfall of the same size
cost the same. In most balancing markets they do not: with dual imbalance
pricing a shortfall is typically settled at a worse price than a surplus,
and the ratio between the two unit penalties moves with the system state.
A referee would ask first whether the results survive this. Short answer:

* the elementary ceiling (1-r)s_k(w) remains an upper bound for every pair
  of penalties, because its proof never used symmetry (Section 2);
* every worst-case law found for symmetric loss remains attainable, so
  asymmetry can only make the audit's overstatement worse (Section 2);
* at the last depth k = n-2, for arbitrary shares, the worst gap has a closed
  form for every penalty ratio (Theorem A);
* for equal shares at every depth the worst gap has a closed form outside a
  set of windows that shrinks as the penalties drift apart and disappears
  once the ratio reaches 2(m-1)/m, which is below 2 (Theorem B);
* for arbitrary shares at every depth, the two-producer formula applied to
  the best split into two blocks is a lower bound for every ratio
  (Theorem C). It is usually the exact answer, but not always: our
  conjecture that it is exact for ratios of at least 2 is false
  (Section 7). The ceiling is exact whenever a subset of a largest face
  has a share in an explicit window (Proposition D);
* inside the windows that survive for ratios between 1 and 2(m-1)/m, and in
  a few arbitrary-share instances below 2, the question is open: the
  relaxation and the best laws found differ slightly (Section 6).

## 1. Model

A producer that offers q and delivers X pays lam_plus (X-q)^+ for a surplus
and lam_minus (q-X)^+ for a shortfall. Dividing by lam_plus + lam_minus gives
the pinball loss of level tau = lam_plus/(lam_plus + lam_minus),

$$
\ell_\tau(u)=\tau u^+ + (1-\tau)u^-,\qquad u = X-q,
$$

whose optimal offer is a tau-quantile. The coalition cost becomes
c(x) = min_q E l_tau(x'Y - q) and nothing else in the game changes: charges,
the standalone ratio rho (now computed with this cost), the integer excess B
and the exclusion hierarchy D_k are defined as before. Write

$$
\kappa=\frac{\max(\lambda_+,\lambda_-)}{\min(\lambda_+,\lambda_-)}=\frac{\max(\tau,1-\tau)}{\min(\tau,1-\tau)}\ \ge 1
$$

for the penalty ratio; kappa = 1 is the symmetric case.

**Lemma 1.** c is sublinear (positively homogeneous and subadditive),
nonnegative, and c(-x) <= kappa c(x) for every x.

*Proof.* Sublinearity is as in the symmetric case (minimize a jointly convex,
positively homogeneous function over q). Since l_tau(-u) = l_{1-tau}(u) and
l_{1-tau} <= kappa l_tau pointwise,
c(-x) = min_q E l_{1-tau}(x'Y - q) <= kappa c(x). ∎

So c is no longer a seminorm but a "kappa-quasi-symmetric gauge": its unit
dual set K satisfies -K ⊆ kappa K. Only the values of c on [0,1]^n enter the
game; the bound c(-e_i) <= kappa c(e_i) is what the proofs below use.

## 2. Which costs occur, and two consequences

Call a **kappa-segment** a triple (d, alpha, beta) with d in R^n, alpha, beta >= 0
and alpha/beta in [1/kappa, kappa]; its cost is alpha (d'x)^+ + beta (d'x)^-,
the support function of the segment [-beta d, alpha d].

**Proposition 2.** For every finite family of kappa-segments there is a finite
demand law on [0,1]^n whose pinball cost (level tau, ratio kappa) is a
positive multiple of the sum of the segment costs.

*Proof.* Assume tau <= 1/2 (otherwise exchange the roles of the two sides) and
put p = tau. For each segment solve alpha = tau A + (1-tau) B,
beta = (1-tau) A + tau B; the solution has A, B >= 0 exactly when
alpha/beta lies in [1/kappa, kappa] (group K of the symbolic checks). Let V
take the values A/p and -B/p with probability p each and 0 otherwise. Then
P(V < 0) <= tau and P(V > 0) <= tau, so 0 is both a tau- and a
(1-tau)-quantile of V, and E l_tau(sV) = alpha s^+ + beta s^- for every real s.
Choose a segment uniformly among K and move a common centre along K V d.
Every component has zero as an optimal offer whatever x is, so the
components share their optimal offer and their costs add. An affine map
puts the law in the unit box and multiplies all costs by the same factor. ∎

For kappa = 1 this is the generator construction of the symmetric notes
(alpha = beta). Hence:

**Corollary 3.**
(a) Every explicit law of the symmetric notes has an asymmetric counterpart
with the same normalized costs on every coalition and membership. Every
lower bound proved for kappa = 1 holds for every kappa.
(b) A value attained with ratio kappa' by segment laws is attained with every
kappa >= kappa'. Where the worst gap is known exactly (Theorems A and B) it is
therefore nondecreasing in kappa.
(c) The ceiling (1-r)s_k(w) bounds the worst gap for every kappa.

*Proof of (c).* Let z live on a face F with a'z - B - c(z) > 0. Since
1_F - z >= 0, subadditivity and the caps give
c(1_F) <= c(z) + sum_{i in F} (1-z_i) a_i/r, and stability gives c(1_F) >= a(F) - B.
So the excess is at most (1/r - 1)(a(F) - a'z), and also at most a'z.
The minimum of the two is at most (1-r)a(F). Only sublinearity and c >= 0
were used. ∎

## 3. Relaxation and certificates

For a fixed membership z, the smallest value of c(z) over all sublinear c
with c(-x) <= kappa c(x) satisfying the caps, c(1) <= 1 and stability is

$$
\max_S\ \min\Bigl\{\max\Bigl(\pi^\top z,\ -\tfrac{1}{\kappa}\pi^\top z\Bigr):\
-\kappa\tfrac{a_j}{r}\le\pi_j\le\tfrac{a_j}{r},\ -\kappa\le \mathbf 1^\top\pi\le 1,\
\pi^\top\mathbf 1_S\ge a(S)-B\Bigr\}.
$$

The argument is that of the symmetric gauge duality: the smallest dual set
containing points pi_S that witness the lower bounds and satisfying
-K ⊆ kappa K is conv(P ∪ -P/kappa). This is `minimal_cost(..., kappa=...)`.

The triangle certificates become

$$
\nu\,c(\mathbf 1_S)\le c(z)+\sum_{i\in S}\frac{a_i}{r}\bigl[(\nu-z_i)^+ +\kappa(z_i-\nu)^+\bigr]
+\kappa\sum_{i\in F\setminus S}\frac{a_i}{r}z_i ,
$$

because a coordinate that has to be lowered is a shortfall direction and
costs at most kappa a_i/r per unit. This is `certificate_bound(..., kappa=...)`.

## 4. Theorem A: the last depth, arbitrary shares

Let k = n-2, so a face has two free producers. For an ordered pair (u, j)
(u the unit coordinate, j the fractional one) put x = a_u/a_j and

$$
\Psi_\kappa(u,j)=
\begin{cases}
\dfrac{a_j(1-r)(r+\kappa)}{r(1+\kappa)} & x\ge \dfrac{\kappa(1-r)}{r(1+\kappa)}\quad\text{(shortfall regime)}\\[2ex]
(1-r)(a_u+a_j) & \dfrac{1-r}{r+\kappa}\le x\le\dfrac{\kappa(1-r)}{r(1+\kappa)}\quad\text{(ceiling regime)}\\[2ex]
\dfrac{a_u(r+\kappa)(a_u+a_j)}{a_u(r+\kappa)+r\,a_j} & x\le\dfrac{1-r}{r+\kappa}\quad\text{(unit-cap regime)}.
\end{cases}
$$

**Theorem A.** For positive shares, 0 < r <= 1 and kappa >= 1 the worst value of
(D_{n-2} - B)/L over all demand laws equals max over ordered pairs of
Psi_kappa(u, j). With kappa = 1 this is Theorem 2.

*Upper bound.* Scale z so that z_u = 1, z_j = t. Four certificates matter:
S = F with nu = 1 and with nu = t, S = {u} with nu = 1, and c >= 0. The first
two give excess bounds that decrease linearly to 0 at t = 1, with slopes
a_j(1-r)/r and a_u(r+kappa)/r. The last two give increasing bounds
t a_j (r+kappa)/r and a_u + t a_j. The maximum over t of the minimum of all
four is min(V1, V2), where V1 crosses the steeper decreasing line with the
first increasing one and V2 with the second. Working out the three cases gives
Psi_kappa. Each regime boundary is the sign change of an explicit factor; for
instance V2 - V1 = (1-r)(r(1+kappa)a_u - kappa(1-r)a_j)/(r(1+kappa)).

*Laws.* Producers outside the pair get the symmetric segment (e_k, a_k, a_k).
On the pair:

* shortfall regime, t = (1-r)/(1+kappa): the segment along d = t e_u - e_j with
  alpha = kappa a_j/r, beta = a_j/r, plus the symmetric segment along e_u with
  weight a_u - kappa(a_j/r)t. The ratio of the first segment is exactly kappa:
  the law uses the full asymmetry.
* ceiling regime, t = 1 - r - r x: one segment along t e_u - e_j with
  beta = a_j/r and alpha anywhere in
  [max(a_u/t, a_j/(r kappa)), min(a_u/(r t), kappa a_j/r)], an interval that is
  nonempty exactly in this regime. The symmetric choice alpha = a_j/r is used
  whenever it lies in the interval.
* unit-cap regime, t = kappa a_u/(a_u(r+kappa) + r a_j): one segment along
  e_u - e_j/t with alpha = a_u/r and beta = kappa a_u/r.

In each case c(z) and the binding constraints are those the certificates
predict, and the remaining constraints hold with the stated factorizations
(group K). ∎

As kappa grows the shortfall regime shrinks to x >= (1-r)/r with value
a_j(1-r)/r, the unit-cap regime disappears, and the ceiling (1-r)(a_u + a_j)
becomes exact for every pair with a_u/a_j <= (1-r)/r.

## 5. Theorem B: equal shares, every depth

Let a = 1/n, M = a/r, m = n-k free producers and

$$
H_p^\kappa(r)=\frac{(m-p)\,a\,(1-r)(r+\kappa)}{r(1+\kappa)},\qquad
I_p^\kappa=\Bigl[\max\Bigl(0,\frac{m-(1+\kappa)p}{m}\Bigr),\ \frac{\kappa(m-p)}{\kappa m+p}\Bigr].
$$

With kappa = 1, H_p is the family of Section 5 of the exact notes and I_p the
interval of Theorem 1.

**Theorem B.** For equal shares, any depth 1 <= k <= n-2 and kappa >= 1:

1. the worst gap is at most min{(1-r)ma, H_1^kappa(r)} for every r;
2. the ceiling (1-r)ma is attained on every I_p^kappa, p = 1, ..., m-1;
3. H_p^kappa is attained for r >= kappa(m-p)/(kappa m + p); with p = 1 this is
   where H_1^kappa drops below the ceiling.

Consequently the worst gap equals min{(1-r)ma, H_1^kappa(r)} for every r
outside the windows

$$
W_p^\kappa=\Bigl(\frac{\kappa(m-p-1)}{\kappa m+p+1},\ \frac{m-(1+\kappa)p}{m}\Bigr),
$$

and W_p^kappa is nonempty iff kappa < (p+1)(m-p)/(pm). The bound decreases in p,
so all windows close once kappa >= 2(m-1)/m.

**Corollary.** If kappa >= 2(m-1)/m, in particular if a shortfall costs at
least twice as much as a surplus,

$$
\sup\frac{D_k-B}{L}=
\begin{cases}(1-r)\dfrac{m}{n}, & r\le\dfrac{\kappa(m-1)}{\kappa m+1},\\[2ex]
\dfrac{(m-1)(1-r)(r+\kappa)}{n\,r(1+\kappa)}, & r\ge\dfrac{\kappa(m-1)}{\kappa m+1}.\end{cases}
$$

*Proof of 1.* Sort the free coordinates as 1 = z_1 >= z_2 >= ... and put
sigma = z_2 + ... + z_m. The certificates S = F, nu = 1 and S = {1}, nu = 1 bound
the excess by (M-a)(m-1-sigma) and by sigma(a + kappa M). Their minimum is
largest at sigma* = (1-r)(m-1)/(1+kappa), where it equals H_1^kappa. Together
with Corollary 3(c) this gives the claim.

*Proof of 2.* Put p producers at 1 and q = m-p at t = 1 - mr/q, and give each
fractional j the segment along d_j = (t/p) 1_units - e_j with beta = M and
alpha in [max(ap/(qt), M/kappa), min(Mp/(qt), kappa M)]. Then c(z) = 0, the
excess is (1-r)ma, the fractional caps bind and the grand cost is exactly
one. For a coalition with p' units and s fractional producers the stability
slack is bilinear in (p', s), so it is enough to check the corners of
[0,p] x [0,q]; they reduce to the two ends of the alpha interval. That
interval is nonempty exactly on I_p^kappa.

*Proof of 3.* Same directions with alpha = kappa M, beta = M and
t = (1-r)/(1+kappa), plus a symmetric segment of weight
w = (ma - qM(1-t))/p on each unit. The units' own coalition and the whole
face are exactly tight, every unit costs a, and the bilinear slack is
nonnegative at all corners. The weight w is nonnegative iff
r >= kappa(m-p)/(kappa m+p).

*Windows.* W_p^kappa is the gap between the top of I_{p+1}^kappa and the bottom
of I_p^kappa, and

$$
(m-(1+\kappa)p)(\kappa m+p+1)-m\kappa(m-p-1)=(1+\kappa)\bigl(m(p+1-p\kappa)-p(p+1)\bigr).
$$

For kappa = 1 this is the condition p^2 + p < m of the exact notes. ∎

**Example.** Four producers, depth one, r = 1/4. With symmetric penalties
r lies in the window and the worst gap is 31/56 ≈ 0.554. With kappa = 2 the
window is gone and the worst gap is the ceiling 9/16 = 0.5625. At r = 0.7 the
worst gap is H_1^kappa: 0.182 for kappa = 1, 0.193 for kappa = 2, 0.208 for
kappa = 10 and 3/14 ≈ 0.214 in the limit.

## 6. Inside the surviving windows

For 1 < kappa < 2(m-1)/m some windows remain, narrower than for kappa = 1. There
the ceiling is not attained by the families above, and H_{p+1}^kappa is a
valid lower bound. Part D of the checks compares, for four producers at depth
one, the certificate bound, the exact relaxation at its maximizer and the best
explicit law found by an LP over kappa-segment laws plus a local search over
the membership. The certificate bound equals the relaxation in every case
tried (nine), but the best law found stays below it, by 4e-4 to 1.3e-3. So
inside these windows we know the answer only within that margin.

Two explanations are possible, and we cannot yet tell them apart. Either the
relaxation is not attained, or it is attained by laws outside the segment
class. Under pinball loss the costs of general laws, support functions of
zonoid trimmed regions shifted to the mean, are richer than sums of segments.
For kappa = 1 the symmetric family V_p closed this gap (Theorem 4 of the exact
notes). An asymmetric analogue of V_p has not been found yet.

A local search over general finite laws tried to tell the two explanations
apart ([general_law_probe.md](../results/asymmetric/general_law_probe.md)).
Once the order of the atoms along every test vector is fixed, the pinball
cost is linear in the atom positions, with the optimal offer at the atom
where the cumulative mass reaches tau, so the best law in an order cell is an
LP; random hops move between cells. Starting from the best segment law, 150
hops with 36 to 72 atoms found no improvement in any of three cases: two
equal-share windows and the open arbitrary-share instance of Section 7 with
seed 7591. This points to the first explanation. Unlike the symmetric case,
where the relaxation was attained in every case tested, with asymmetric
penalties the relaxation may overstate the true worst case inside these
narrow regions. A local search is evidence, not proof.

**Where extra inequalities would come from.** For a law with mean mu,

$$
c(x)=\tau\bigl(x^\top\mu-\mathrm{LCVaR}_\tau(x^\top Y)\bigr)=h_{\tau(\mu-D_\tau)}(x),
\qquad D_\tau=\{\mathbb E[Y\xi]:0\le\xi\le1/\tau,\ \mathbb E\xi=1\},
$$

where D_tau is the zonoid trimmed region of Koshevoy and Mosler, that is the
section at height tau of the lift zonoid of Y (whose support function is
E(t + x'Y)^+), divided by tau. So pinball costs are support functions of
reflected sections of zonoids. Segment sums are the special case in which the
section is itself a zonotope. Sections of zonoids are not zonoids in general,
which is why general laws give more costs than segment sums. Any inequality
that all such sections satisfy, beyond -K ⊆ kappa K, would tighten the
relaxation and could settle the open regions. Finding one is the natural
next step on this question.

## 7. Arbitrary shares at intermediate depths

**Theorem C (two-block lower bound).** For positive shares, any depth
1 <= k <= n-2 and kappa >= 1,

$$
\Gamma_k^\kappa(w,r)\ \ge\ \max_{K,\ I}\ \Psi_\kappa\bigl(a(I),\,a(F\setminus I)\bigr),
$$

where K runs over the excluded sets of size k, F = N \ K, I over the nonempty
proper subsets of F, and Psi_kappa is the function of Theorem A with the two
producers replaced by two blocks: the units I and the fractional producers
J = F \ I, with share totals a(I) and A_J. At the last depth this is
Theorem A. With kappa = 1 it is the best of the families C31, H and G of
Theorem 5 of the exact notes.

*Laws.* Give each fractional j one segment along
d_j = (t a_i/a(I) on the units, -1 on j), so that d_j'z = 0 for
z = 1_I + t 1_J, with coefficients proportional to a_j:

* shortfall regime: alpha_j = kappa a_j/r, beta_j = a_j/r, t = (1-r)/(1+kappa),
  plus a symmetric segment of weight omega a_i on each unit, with
  omega = 1 - kappa(1-r)A_J/(r(1+kappa)a(I));
* ceiling regime: beta_j = a_j/r and alpha_j = lambda a_j/r, with lambda in
  [1/kappa, kappa] and r a(I) <= lambda t A_J <= a(I), t = 1 - r - r a(I)/A_J;
* unit-cap regime: alpha_j = s a_j, beta_j = kappa s a_j, s = a(I)/(r t A_J),
  t = kappa a(I)/(a(I)(r+kappa) + r A_J).

The cost of a coalition S inside the face depends only on
theta = a(S ∩ I)/a(I) and A' = a(S ∩ J), and its stability slack is bilinear
in (theta, A'). So the four corners (the empty set, J, I and F) suffice, and
they reduce to the conditions of Theorem A (group L of the symbolic checks).
Excluded producers get symmetric segments of weight a_k, as before.

**Computation** ([general_shares.md](../results/asymmetric/general_shares.md)).
600 random instances with n = 4, 5, 6, intermediate depths 1 <= k <= n-3,
r = k/50 and kappa drawn from {1, 5/4, 3/2, 2, 3, 10}. Every two-block law passes
the exact verification. Compared with the certificate bound:

| kappa | instances | two-block value = certificate | otherwise an explicit law reaches it | open |
| --- | ---: | ---: | ---: | ---: |
| 1 | 97 | 89 | 8 (the transitional family of Conjecture 6) | 0 |
| 5/4 | 104 | 103 | 0 | 1 (difference 7.9e-4) |
| 3/2 | 100 | 98 | 0 | 2 (difference up to 1.8e-3) |
| 2 | 101 | 101 | | 0 |
| 3 | 93 | 93 | | 0 |
| 10 | 105 | 105 | | 0 |

For kappa >= 2 the two-block formula equals the certificate bound in all 299
instances, so in each of them it is the worst gap, attained by an explicit
law. For 1 < kappa < 2 the three open instances look like the equal-share
windows: the certificate bound equals the exact relaxation at its maximizer,
and the best segment law stays slightly below.

**Conjecture C (refuted).** We conjectured from these numbers that for
kappa >= 2, every depth and all positive shares, the worst gap equals the
two-block bound of Theorem C. It is false
([conjecture_c.md](../results/asymmetric/conjecture_c.md)). Take four
producers with shares (1, 24, 24, 1)/50, depth one, r = 33/50 and kappa = 10.
The best two-block value is 0.249614. An explicit finite law with 24 atoms,
checked in exact rational arithmetic on every coalition (all producers pay at
least 66% of their standalone cost, every proper coalition is strictly
stable), reaches 0.266393 at the membership (1, 0.4098, 0.1035, 0). Its three
levels make it a transitional law, like the family V of the symmetric notes.
The certificate bound for this instance is 0.278674, so the true worst case
lies between 0.2664 and 0.2787.

The counterexample needs a particular shape: a very small producer at level
one next to two large producers at different fractional levels. Random
sampling missed it. Among 200 random four-producer instances with one small
share, an explicit law beat the two-block value in 2 instances, both at
kappa = 2 and by at most 0.0032, and in none at kappa = 3 or 10. It came out of
the attempt to prove the conjecture, described below.

**How the proof attempt went.** Every certificate bound can be written as
sum_i a_i d(z_i), where d is an asymmetric distance from z to the points
nu 1_S, with weight (r+kappa)/r above nu and (1-r)/r below it. On the region where
the coordinates of z are sorted, the certificate LP is a finite zero-sum
game: the maximizer mixes the vertices 1_{U_s} (indicators of the top-s sets),
the minimizer mixes certificates. Two-block laws are exactly the mixtures of
two columns, s and m. The conjecture therefore said that for kappa >= 2 two
columns suffice. To prove it we grouped the producers into the units, the
producer at which the cumulative share jumps over the ceiling window below,
and the rest. Six certificates then depend only on three aggregate numbers,
and the bound becomes an LP in three variables. Testing that LP on a grid
first produced a false alarm, a comparison against the top sets of one
ordering only. Once every union of the three blocks was allowed, the LP
still exceeded the two-block value by up to 0.03. The full certificate LP
and then an explicit law confirmed the excess.

**What survives** is Theorem C and the following criterion, valid for every
kappa >= 1, the symmetric case included.

**Proposition D (ceiling criterion).** Let F be a face with total share
T = a(F). If some nonempty proper subset I of F has

$$
\frac{1-r}{1+\kappa}\,T\ \le\ a(I)\ \le\ \frac{\kappa(1-r)}{r+\kappa}\,T ,
$$

the two-block law of Theorem C for the split (I, F \ I) is in its ceiling
regime and attains (1-r)T. If F is a largest face, the worst gap therefore
equals the elementary ceiling (1-r)s_k(w). In particular this holds whenever
every producer of a largest face has a share of at most W a(F), with

$$
W=\frac{(1-r)(\kappa^2-r)}{(r+\kappa)(1+\kappa)} ,
$$

the width of the window: adding producers one at a time, the first partial
sum that reaches the window cannot jump over it, and the window ends below T.

*Proof.* The two ends of the window are the two ends of the ceiling regime,
a(I)/A_J = (1-r)/(r+kappa) and a(I)/A_J = kappa(1-r)/(r(1+kappa)). The upper bound is
Corollary 3(c). The algebra is group M of the symbolic checks. ∎

For kappa = 1 the window is [(1-r)/2, (1-r)/(1+r)] a(F). At r = 0.2 it is
[0.4, 0.67] a(F); at r = 0.4 it is [0.3, 0.43] a(F); at r = 0.7 it shrinks to
[0.15, 0.18] a(F). This is consistent with, and largely explains, the
empirical pattern recorded with Theorem 5 of the exact notes: the ceiling was
exact in every random instance with r <= 0.4 and in none with r >= 0.7. The
criterion is sufficient, not necessary.

## 8. What changes for the overall message

Asymmetric penalties make the audit's overstatement larger, never smaller.
The elementary ceiling becomes exact on a wider range of r, and at the top of
the range the exact value increases from (m-1)(1-r^2)/(2nr) towards
(m-1)(1-r)/(nr). For ratios of at least 2 the equal-share answer is a
two-piece formula with no windows. For arbitrary shares the two-block
formula is usually, but not always, the answer. The qualitative conclusion of
the paper, that fractional audits can be badly wrong even with a high
standalone floor, is therefore robust to asymmetric pricing, and in fact
strengthened by it.

## Checks

* `scripts/check_asymmetric_penalties.py` (results in
  [results/asymmetric/](../results/asymmetric/asymmetric_checks.md), about
  100 s): 300 random last-depth instances with arbitrary shares (construction
  exact, explicit law exact under pinball loss, certificate LP equal to the
  closed form: 300 of 300 each); 5565 equal-share constructions on a grid of
  n = 3..8, every depth, seven ratios and r = k/40 (all exact), 1305 of them
  also as explicit laws; agreement with Theorem 1 at kappa = 1 on all 819 grid
  points; 288 of 288 certificate cross-checks outside the windows; and the
  window probe of Section 6.
* `scripts/check_asymmetric_general.py` (results in
  [general_shares.md](../results/asymmetric/general_shares.md)): the 600
  random arbitrary-share instances of Section 7.
* `scripts/refute_conjecture_c.py` (results in
  [conjecture_c.md](../results/asymmetric/conjecture_c.md)): the exact
  counterexample to Conjecture C and the sample with one small share.
* `scripts/probe_general_laws.py` (results in
  [general_law_probe.md](../results/asymmetric/general_law_probe.md)): the
  local search over general finite laws of Section 6.
* `scripts/verify_symbolic.py`, groups K, L and M: 41 + 19 + 6 identities and
  factorizations (pinball inequality, three-point law, the three regimes of
  Theorem A, the certificate pair, both families of Theorem B, the window
  condition, the bilinear slacks of the two-block families, and the window
  of Proposition D).
* `tests/test_asymmetric.py`.
