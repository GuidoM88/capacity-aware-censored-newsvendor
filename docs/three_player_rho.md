# Exact standalone-ratio envelope for three equal shares

November 6, 2026. This is a mathematical response to the informal critique of
the first manuscript. It develops the suggested structural-parameter direction
in a precisely limited case. It is not a claim of established bibliographic
priority or sufficient publication significance.

## Statement

Use three producers, unit absolute imbalance loss, and equal shares w_j=1/3.
Write L>0 for the expected cost of the fixed grand offer, a_j=L/3, B for
the maximum positive proper-coalition excess, and D_1 for the maximum over
the three zero-coordinate faces, including zero. Set

$$
\rho=\min\bigl(\{1\}\cup\{a_j/c_j:c_j>0\}\bigr),
\qquad c_j=\min_q\mathbb E|q-Y_j|.
$$

For a prescribed threshold r in [0,1], define

$$
F(r)=\sup_{\rho\ge r}\frac{D_1-B}{L},
$$

where the supremum is over bounded nonnegative joint laws and fixed grand
offers with L>0 and these equal shares.

**Theorem (C39).**

$$
F(r)=
\begin{cases}
\dfrac23(1-r), & 0\le r\le\dfrac13,\\[4pt]
\dfrac{1-r^2}{6r}, & \dfrac13\le r\le1.
\end{cases}
\tag{1}
$$

For every r>0, four equiprobable scenarios attain (1) with actual rho=r,
B=0, an optimal true grand offer, unit capacities, positive individual
variances, and a forecast with the correct aggregate distribution and individual
means that induces the equal shares. Some integer coalitions bind in these
attaining examples.

For every 0<r<1, the same supremum holds when every proper integer coalition
must instead be strictly stable and the true covariance must be positive
definite. The last assertion is a supremum statement proved by a mixture,
not finite attainment. At r=1 strict singleton stability is impossible because
rho=1 requires c_j<=a_j.

The result is specific to three equal shares and symmetric loss. It does not
establish the envelope for arbitrary shares, more producers or asymmetric
penalties.

## Upper bound

Normalize all costs and charges by L, so a=1/3. For r>0 put M=a/r.
Then c_j<=M for every j. Under unit absolute loss the optimized cost
extends to a seminorm on signed membership vectors:

$$
c(x)=\min_{q\in\mathbb R}\mathbb E|q-x^\top Y|,
\qquad c(-x)=c(x),\qquad c(x+y)\le c(x)+c(y).
$$

These properties follow by negating or adding feasible offers. In particular,
the reverse triangle argument used below requires symmetric loss.

If D_1>B, a maximizing membership has a positive objective. Positive
homogeneity allows it to be scaled within its face until one free coordinate
is one. Relabel that face's free coordinates i,j and write
z=e_i+t*e_j, 0<=t<=1. From the singleton and pair integer comparisons,

$$
c_i\ge a-B,\qquad c_{ij}\ge2a-B.
$$

Nonnegativity and two triangle inequalities give

$$
\begin{aligned}
f(z)-B&\le a(1+t)-B\le a(1+t),\\
c_i&\le c(z)+t c_j
 \quad\Longrightarrow\quad f(z)-B\le t(a+M),\\
c_{ij}&\le c(z)+(1-t)c_j
 \quad\Longrightarrow\quad f(z)-B\le(1-t)(M-a).
\end{aligned}
\tag{2}
$$

Thus the normalized gap is at most

$$
\max_{0\le t\le1}
\min\{a(1+t),\ t(a+M),\ (1-t)(M-a)\}.
\tag{3}
$$

The first two lines increase in t and the third decreases. If M>=3a
(r<=1/3), the first and third intersect at t=1-2r, where the second
is no smaller. The value is 2a(1-r).
If a<=M<=3a (r>=1/3), the second and third intersect at t=(1-r)/2,
where the first is no smaller. The value is

$$
\frac{M^2-a^2}{2M}=\frac{1-r^2}{6r}.
$$

The case D_1=B is immediate. At r=0 the original share ceiling gives
2/3, also the limit of the constructions below.

## Attainment with four scenarios

Let Z,V be independent equiprobable signs. For coefficient vectors u,v,
put X=uZ+vV. Central symmetry makes zero an optimal absolute-loss offer
for every linear combination. The elementary identity

$$
\mathbb E|pZ+qV|=\frac{|p+q|+|p-q|}{2}
=\max\{|p|,|q|\}
$$

gives the cost

$$
c_X(z)=\max\{|u^\top z|,\ |v^\top z|\}.
\tag{4}
$$

### Low-ratio regime: 0<r<=1/3

Take

$$
u=(M-2a,0,-M),\qquad v=(0,1,0),\qquad a=\frac13,\quad M=\frac1{3r}.
$$

The grand cost is max(2a,1)=1. The singleton costs are
M-2a, 1 and M, so rho=r. Pair costs are

$$
c_{12}=\max(M-2a,1),\qquad c_{13}=2a,\qquad c_{23}=M.
$$

Since M>=1, every singleton costs at least a and every pair at least
2a. Hence B=0. At z=(1,0,1-2r), both terms in (4) vanish, and

$$
f(z)=a(2-2r)=\frac23(1-r).
$$

### High-ratio regime: 1/3<=r<=1

Take

$$
u=(a,a,-M),\qquad v=(2a-M,a,M).
$$

Here a<=M<=3a. The grand cost is 1, singleton costs are a,a,M, and
pair costs are 2a,2a,a+M for pairs 12,13,23 respectively.
Thus rho=r and B=0. With t=(1-r)/2 and z=(1,0,t), both absolute
terms in (4) equal (3a-M)/2. Consequently

$$
f(z)=a(1+t)-\frac{3a-M}{2}
=\frac{M^2-a^2}{2M}.
$$

This matches (3). At r=1 it gives zero, as required.

### Bounded outputs and forecast realization

Let R=max_j(|u_j|+|v_j|)>0 and set

$$
Y_j=\frac12+\frac{X_j}{2R},\qquad q_0=\frac32.
$$

Then 0<=Y_j<=1, all individual variances are positive, the grand offer
is optimal, and L=1/(2R). All normalized gaps and cost ratios are unchanged.
For T=Y(N), the forecast tilde Y_j=T/3 has the correct aggregate law,
unit capacities, and individual mean 1/2, equal to the true means.
Its normalized optimal dual allocation has equal shares.

For the displayed constructions R=M in the low-ratio regime and R=2M
in the high-ratio regime. With A=3/2 this gives L/A=r and L/A=r/2,
respectively. For each fixed r>0 these values do not vanish.
This is still an analytically constructed law, not a realistic-data evaluation.

## Strict stability and positive definite covariance

Let U_j be independent uniform variables on the three-point set {-1,0,1},
and let X^s=(9/10)U. Direct enumeration gives

$$
c^s(N)=1,\qquad c^s_j=\frac35,\qquad c^s_{ij}=\frac45.
$$

Its equal allocation is strictly stable, and its covariance is (27/50)I.
Both this law and each four-scenario law above are centrally symmetric.
Their mixture therefore has cost equal to the same mixture of costs for
every membership vector: zero remains a common optimal offer.

Fix 0<r<1 and let epsilon>0 be sufficiently small. Define

$$
r_\varepsilon=\frac{1-\varepsilon}{1/r-(9/5)\varepsilon}.
$$

This lies in (0,1) and tends to r. Mix the attaining law at r_epsilon
with weight 1-epsilon and X^s with weight epsilon. The grand cost
remains 1. The largest singleton cost becomes

$$
(1-\varepsilon)\frac1{3r_\varepsilon}
+\varepsilon\frac35=\frac1{3r},
$$

so the actual ratio is exactly r. Every proper coalition now has strictly
larger cost than its charge, and the covariance is at least
epsilon*(27/50)I before the common unit-capacity scaling.

At an optimal base witness z_epsilon,

$$
f_{\rm mix}(z_\varepsilon)
=(1-\varepsilon)F(r_\varepsilon)
 +\varepsilon\{a^\top z_\varepsilon-c^s(z_\varepsilon)\}
\ge(1-\varepsilon)F(r_\varepsilon)-\frac65\varepsilon.
$$

This tends to F(r), which proves the strict-stability supremum.
A common translation and scaling again gives unit capacities and the
aggregate-correct, individual-mean-correct forecast T/3. For fixed r the
scaling radius stays bounded and positive, so this strict approximation
does not force L/A to zero. QED.

## What changes, and what remains open

The previous bound (2/3)*(1-rho) is sharp in this case up to rho=1/3.
For 1/3<rho<1 it is strictly loose. The singleton reverse-triangle
constraint is then active and the optimal fractional witness has positive
cost. This gives a change of regime that the share-only ceiling misses.

The finding does not establish a computational advantage over branch-and-bound,
a finite-data detection benefit, a general n-player characterization or
bibliographic novelty. It makes the structural-parameter direction testable
before expanding the manuscript. The next mathematical question is whether
the three-line face argument extends to arbitrary positive shares and then
larger faces, with matching constructions or a rigorous obstruction.

The [deterministic check](../scripts/check_three_player_rho.py) compares exact
formulas with coalition enumeration, independent primal face LPs, existing dual
LPs and an exact MILP. The [saved report](../results/exclusion/three_player_rho.md)
labels attaining cases, strict approximations and off-family checks separately.
These are proof checks, not a computational-performance benchmark.
