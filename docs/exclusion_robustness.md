# Continuous distributions and a nonvanishing cost scale

November 6, 2026. Supporting extensions to C30 in the
[working manuscript](../paper/README.md). This note addresses two concrete
objections: the sharp family has only two atoms and rank-one covariance;
its expected-to-maximum cost ratio tends to zero. The proofs below separate
these issues. They do not assert a new general statistical method or settle
bibliographic priority.

Use unit absolute loss, fixed positive shares w summing to one, charges a=Lw,
integer excess B and the exclusion bounds D_k as in the manuscript. All physical
capacities in this note are one. The maximum declared loss of the offer is
A=max(q_0,n-q_0).

## 1. Sharpness survives absolute continuity and positive definite covariance

**Proposition (C37).** For every n>=3, prescribed w>0 and 1<=k<=n-2,

$$
\sup\frac{D_k-B}{L}=s_k(w)
$$

still holds if the true joint law must have a bounded density for each instance
and positive definite covariance, while the aggregate forecast is correct,
the forecast induces w, the implemented grand offer is optimal, and every
proper actual coalition is strictly stable. The same sequence approaches the
suprema at all nonterminal depths.

The proposition imposes no common upper bound on the densities and no fixed
positive lower bound on the covariance eigenvalues across the sequence.
The true law in this extension is a mixture of two continuous boxes, not a
two-atom law. No claim of independent producer outputs or log-concavity follows.

**Proof.** Let X_H be the original unit-capacity two-state construction:

$$
x^+=\frac1H(m,2,\ldots,2,0),\quad
x^-=\frac1H(0,\ldots,0,H-1),\quad H=m+2(n-2),\quad m\ge2.
$$

Put w_max=max_j w_j and choose

$$
\delta_H=\min\left\{\frac{1}{8nH^2},
 \frac{1-w_{\max}}{4(n-1)w_{\max}}\right\},\qquad
\lambda_H=1-2\delta_H.
$$

Independently of X_H, let U have independent uniform [-1,1] coordinates, and set

$$
Y_H=\lambda_H X_H+\delta_H\mathbf1+\delta_H U.
\tag{1}
$$

All coordinates remain in [0,1]. Conditional on either original state, (1)
is uniform on a full-dimensional box. Its mixture density is bounded for
each finite H, and

$$
\operatorname{Cov}(Y_H)
=\lambda_H^2\operatorname{Cov}(X_H)+\frac{\delta_H^2}{3}I
\succ0.
$$

For any nonempty integer coalition, including the grand coalition, the original
two state totals differ by at least 1/H. The added coalition noise has absolute
value at most n*delta_H, and

$$
n\delta_H<\frac{\lambda_H}{2H}.
$$

Thus the two conditional total intervals are separated. An offer between the
intervals is a median. Each conditional perturbation has mean zero, so its
expected absolute loss at any such median is half the difference between
the two conditional means. Consequently

$$
c_{Y_H}(\mathbf1_S)=\lambda_H c_{X_H}(\mathbf1_S)
\quad(\emptyset\ne S\subseteq N),\qquad
L_H=\frac{\lambda_H}{2H}.
\tag{2}
$$

The grand midpoint offer is
q_H=lambda_H*(1-1/(2H))+n*delta_H. Scaling the original strict integer
inequalities by lambda_H proves B_H=0 and strict stability.

For forecast realization, use T_H=Y_H(N) and set
tilde Y_j=w_j*T_H. Its aggregate law is exactly that of T_H. Also

$$
T_H\le1+2(n-1)\delta_H,\qquad
w_{\max}T_H\le\frac{1+w_{\max}}2<1.
$$

The forecast therefore satisfies the same unit capacities. Its optimal dual
score is +1 on the high cluster and -1 on the low cluster, with mean zero.
Since E[T_H*score]=L_H, its normalized dual charges are exactly w.

Let z_{H,k} be the original zero-cost fractional witness that excludes the k
smallest middle shares. Under X_H its weighted output is constant. Under (1)
its only random deviation is delta_H*z_{H,k}'U. Using the constant center
as an offer gives

$$
c_{Y_H}(z_{H,k})\le
\delta_H\mathbb E|z_{H,k}^{\top}U|
\le n\delta_H.
$$

The resulting feasible excess proves

$$
\frac{D_{k,H}-B_H}{L_H}\ge
s_k(w)-w_n\frac{2k-1}{H-1}
-\frac{2Hn\delta_H}{\lambda_H}.
\tag{3}
$$

The last term is at most 1/(4H*lambda_H), which tends to zero. The original
charge-budget bound supplies the upper limit. This proves the proposition
simultaneously for all nonterminal k. QED.

**Scope.** The smallest covariance eigenvalue in this construction is
delta_H^2/3 and tends to zero. Also L_H/A_H still tends to zero. Absolute
continuity and a nonsingular covariance alone do not remove the sharp
expected-cost obstruction. Uniform restrictions on dependence or cost scale
remain a different question. Adding independent noise is an elementary
regularization argument; C37 is support for C30, not an independent novelty claim.

## 2. A continuous example with L/A=1/10 and a gap above 5% of A

**Proposition (C38).** There is a three-producer bounded continuous law with
positive definite covariance, an aggregate-correct forecast with correct individual means, positive shares,
an optimal grand offer and strictly stable actual coalitions such that

$$
\frac{L}{A}=\frac1{10},\qquad B=0,\qquad
\frac{D_1-B}{A}\ge\frac{967}{16200}>0.05969.
\tag{4}
$$

In this example the minimum covariance eigenvalue is 1/1875. Formula (4)
is a proved feasible lower bound, not a claim of the exact fractional optimum.

**Construction.** Let X take the two values

$$
x^+=\left(\frac45,\frac45,\frac1{20}\right),\qquad
x^-=\left(\frac15,\frac15,\frac{19}{20}\right)
$$

with equal probability. Let U again have independent uniform [-1,1] coordinates,
independent of X. Set

$$
Y=X+\varepsilon U,\qquad
\varepsilon=\frac1{25},\qquad
w=\left(\frac9{20},\frac1{10},\frac9{20}\right),\qquad
q_0=\frac32.
\tag{5}
$$

Outputs lie in [0,1]^3 and have a bounded joint density. The grand conditional
means are 33/20 and 27/20. Each total is perturbed by at most 3/25<3/20.
Therefore q_0 lies between the two clusters and is an optimal median, with
L=3/20. Since the declared capacities are one, A=3/2 and L/A=1/10.

For all proper coalitions the same separation and zero-mean argument gives
the following exact costs and charges.

| Coalition | Optimized cost | Assigned charge | Cost minus charge |
| --- | ---: | ---: | ---: |
| {1} | 3/10 | 27/400 | 93/400 |
| {2} | 3/10 | 3/200 | 57/200 |
| {3} | 9/20 | 27/400 | 153/400 |
| {1,2} | 3/5 | 33/400 | 207/400 |
| {1,3} | 3/20 | 27/200 | 3/200 |
| {2,3} | 3/20 | 33/400 | 27/400 |

Every margin is strictly positive, so B=0. Set T=Y(N) and use the forecast

$$
\widetilde Y_j=\frac12+w_j\left(T-\frac32\right).
$$

Its sum is exactly T and its individual means are all 1/2, equal to the true
means. For epsilon=1/25, T lies in [123/100,177/100], so every forecast
coordinate is between 757/2000 and 1243/2000. The common high/low score has
mean zero, and E[tilde Y_j*score]=w_j*L. This realizes the specified shares
under the same capacities. At epsilon=1/20 the forecast coordinates still
lie between 73/200 and 127/200.

The covariance is

$$
\operatorname{Cov}(Y)=vv^\top+\frac1{1875}I,\qquad
v=\left(\frac3{10},\frac3{10},-\frac9{20}\right)^\top,
$$

so its smallest eigenvalue is exactly 1/1875.

**Fractional witness.** Take z=(1,0,2/3), which is feasible at depth one.
Its noiseless weighted output is 5/6 in both states; its assigned charge is
9/80. Its optimized cost is

$$
c(z)=\varepsilon\,\mathbb E|U_1+(2/3)U_3|
=\frac{31\varepsilon}{54}.
\tag{6}
$$

Indeed, symmetry makes the center a median. Conditional on V uniform [-1,1],
integration over an independent U uniform [-1,1] gives
E_U|U+rV|=(1+r^2 V^2)/2 for 0<=r<=1. Averaging V^2=1/3 and taking r=2/3
gives 31/54. Thus

$$
D_1-B\ge\frac9{80}-\frac{31}{1350}
=\frac{967}{10800}.
$$

Dividing by A=3/2 proves (4). QED.

The argument holds throughout 0<epsilon<=1/20: all integer costs, L, A and
the forecast shares remain the same, and

$$
\frac{D_1-B}{A}\ge\frac3{40}-\frac{31\varepsilon}{81}
\ge\frac{181}{3240}>0.05586.
\tag{7}
$$

At epsilon=1/20 the grand intervals touch at their median, which does not
change the expected-cost calculation. The explicit value 1/25 in (5) leaves
strict separation. This is a family of continuous counterexamples with fixed
cost scale, rather than a limit in which L/A vanishes.

**Scope.** This example proves persistence at a fixed scale for one positive
split and depth, not sharpness at fixed L/A for every split and depth.
The producer outputs remain strongly dependent through their shared state.
Correct individual means do not imply correct individual distributions or
dependence forecasts. The result does not establish independence, a nonsingular
forecast covariance, or generality over practical production laws. It also does not explain away
or reverse the saved statistical comparison's failed precision screen.

## 3. Reproducible checks

The [script](../scripts/check_exclusion_robustness.py) checks the proof's
conditions with exact rational arithmetic for n in {3,6,8}, m in {2,20,200},
and the two share choices used by the original sharpness check.

For (5), it checks all six coalition costs, the covariance, forecast realization
and (6) by separate adaptive quadrature. It also uses product midpoint
approximations with 3, 7 and 15 points per noise coordinate and compares three
membership/offer primal face LPs to the existing dual LP for each approximation.
These are deterministic checks of an analytically chosen example, not a
prespecified statistical superiority experiment.

Couple each uniform coordinate to its bin midpoint. Its output error is at most
epsilon/order. On any depth-one face at most two coordinates are free, so
the optimized cost differs by at most 2*epsilon/order, uniformly in membership.
Grand cost and integer costs are unchanged on these symmetric separated grids.
Therefore the same bound encloses the continuous D1 around the grid D1.
These enclosures are deterministic, not statistical confidence intervals.
The [generated report](../results/exclusion/robustness.md) and
[full records](../results/exclusion/robustness.json) retain every checked grid.

## 4. Consequence for the manuscript and external review

These extensions address two specific objections to the construction:
exact atoms and singular covariance are not necessary, and a nonzero
maximum-loss-scale gap is possible with positive charges and continuous output.
The general fixed-L/A extremal formula is still open. The limiting sharp
sequence remains specialized. No new assessment of global priority follows
from regularization or these numerical checks; the
[source comparison](exclusion_prior_art.md) remains the bibliographic record.

The November 5 PDF is retained as the first assembled draft. This dated note
is the mathematical addendum for the next manuscript revision and independent
review. A reviewer can now assess the following concrete questions:

1. Are the exclusion definition, sharp construction and continuous extension
   correct under the stated fixed-allocation and forecast restrictions?
2. Does an existing theorem imply the exact depth/share formula, beyond the
   already identified root relaxation and two-state cost device?
3. Does the extremal formula together with (4) support a useful short note,
   or would a fixed-cost-scale extremal characterization be needed?

No review request or manuscript has been sent to another person.
