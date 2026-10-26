# Formulation and preliminary results

## 1. Population problem

For products `i = 1, ..., n`, demand `D_i` is nonnegative with finite mean.
Historical stock limits `c_i > 0` are fixed and known. Observations are

$$S_i=\min(D_i,c_i).$$

Begin with the population law of sales known exactly. This isolates the
information loss caused by censoring from finite-sample estimation error.
It identifies `F_i(x)` for `x < c_i`, but cannot separate demand equal to `c_i`
from demand strictly above it. Allowing atoms at the boundary matters.

For underage costs `b_i > 0`, overage costs `h_i > 0`, weights `a_i > 0` and
capacity `B >= 0`, define

$$Q_B=\{q\geq0:a^\top q\leq B\},\qquad
C_F(q)=\sum_i \mathbb E_F[b_i(D_i-q_i)_++h_i(q_i-D_i)_+].$$

The ambiguity class `A(S,c)` contains all nonnegative finite-mean demand laws
with the same observed sales law. A **common optimal action** is a vector in

$$\bigcap_{F\in\mathcal A(S,c)}\arg\min_{q\in Q_B} C_F(q).$$

When all compatible models have the same unique optimizer, call the optimal
action identified. Nonempty intersection alone is a weaker statement if some
models have multiple optima. Neither statement identifies the optimal cost:
unobserved demand means can change absolute costs while leaving the action fixed.

For a chosen action, regret is

$$R_F(q)=C_F(q)-\min_{z\in Q_B}C_F(z).$$

Product dependence does not affect this separable expectation, though it can
matter in extensions with substitution, joint risk measures, or chance constraints.

## 2. Standard optimality conditions

At a continuity point of the marginal CDF,

$$C'_{F,i}(q_i)=(b_i+h_i)F_i(q_i)-b_i.$$

At an atom, the subgradient interval is

$$\partial C_{F,i}(q_i)=
[(b_i+h_i)F_i(q_i^-)-b_i,\ (b_i+h_i)F_i(q_i)-b_i].$$

For `q_i > 0`, stationarity requires `-lambda a_i` in this interval, where
`lambda >= 0` and `lambda(a^T q-B)=0`. At `q_i=0`, there must be a subgradient
`g_i` with `g_i+lambda a_i >= 0`. For continuous distributions with a strictly
increasing CDF, the positive interior solution is the adjusted quantile

$$q_i(\lambda)=F_i^{-1}\!\left(\frac{b_i-\lambda a_i}{b_i+h_i}\right),$$

with zero chosen when the numerator is nonpositive. If the independent optimum
fits the capacity, `lambda=0`; otherwise solve `a^T q(lambda)=B`.
These are standard convex optimization facts, not an originality claim.

## 3. Elementary observable-prefix certificate

**Sufficient condition.** Suppose a feasible `q` lies strictly below every
historical stock boundary. If the subgradients determined by the observed CDF
prefixes satisfy the preceding stationarity and complementarity conditions with
a common `lambda >= 0`, then `q` is optimal for every compatible completion.

**Proof.** Select those same observable subgradients for each compatible model.
The convex subgradient inequality gives

$$C_F(z)-C_F(q)\geq g^\top(z-q)\geq-\lambda a^\top(z-q)\geq0$$

for any feasible `z`. The middle inequality uses the lower-bound KKT multipliers
at zero quantities; the last uses complementarity. Thus `q` is optimal for every
completion. Local strict convexity along every nonzero feasible direction gives
uniqueness, since any second optimum would force a flat segment from `q`. QED.

This is a direct consequence of standard KKT sufficiency. It is a useful
verification device, not yet a research contribution. Quantities exactly at a
censoring boundary require a separate subgradient argument, as below.

## 4. Exact two-product illustration

Let `n=2`, `b_i=4`, `h_i=a_i=1`, and `c_i=40`. The observed CDF below 40 is
`F_i(x)=x/100` on `[0,40)`. Above the boundary the remaining probability 0.6
is unrestricted, subject to finite means. In particular, both of these models
are compatible:

$$D^A\sim U[0,100],\qquad
D^B\sim0.4U[0,40]+0.6U[40,160].$$

Use independent products for the four example worlds AA, AB, BA, BB. This makes
the **joint** censored observation distribution identical across worlds, not
only their marginal distributions.

**Proposition (illustrative).** In this ambiguity class, the optimal action is
identified exactly for `0 <= B <= 80`, where it is `(B/2,B/2)`.

**Proof for `B < 80`.** For positive `B`, use `q_i=B/2` and
`lambda=4-B/40`. All selected quantities are below 40, and their known marginal
derivatives are `q_i/20-4=-lambda`. The certificate proves optimality. The loss
is strictly convex locally since its second derivative is `1/20`; hence the
optimum is unique. At `B=0`, feasibility itself forces the unique zero vector.

**Boundary `B=80`.** At `q_i=40`, every compatible marginal has left derivative
`-2`; its right derivative is at least `-2`, allowing an arbitrary atom at 40.
Choose the subgradient `-2` and `lambda=2` to certify optimality. Any different
feasible vector decreases at least one coordinate below 40. Along the segment
from `(40,40)` this coordinate contributes strictly positive curvature, so that
the competing vector cannot also be optimal.

**Nonidentification for `B > 80`.** In world AB, for `80 < B < 200`, both
quantities exceed 40 and the binding optimum is

$$q^{AB}(B)=\left(\frac{B+40}{3},\frac{2B-40}{3}\right).$$

For `B >= 200`, its independent optimum is `(80,120)`. World BA swaps the
coordinates. These unique optima differ for every `B>80`, although the entire
joint law of observed sales is identical. Thus no common optimal action exists
over the full ambiguity class in that regime. QED.

This proposition describes a specially constructed population instance. It does
not establish that identification improves monotonically as capacity decreases
for arbitrary heterogeneous costs, observation boundaries, or resource matrices.

## 5. Finite-scenario minimax reference

For the supplied set `W={AA,AB,BA,BB}`, the implemented reference solves

$$\min_{q\in Q_B,t\geq0}t\quad\text{s.t.}\quad
C_w(q)-C_w(q_w^*)\leq t\quad\forall w\in W.$$

This is convex. It differs from minimizing worst-case *absolute cost*, and from
minimax regret over the full censoring ambiguity class. The four complete
scenarios constitute additional prior information supplied to the method.

At `B=120`, swapping products permutes `W`, and the objective is convex and
symmetric. Averaging any feasible decision with its swap cannot increase the
objective, so a symmetric minimizer exists. Along symmetric decisions `(s,s)`
with `s<=60`, every scenario's cost decreases with `s`; hence `(60,60)` is a
minimizer. The AB regret is

$$\frac12\frac1{20}\left(\frac{20}{3}\right)^2+
\frac12\frac1{40}\left(-\frac{20}{3}\right)^2=\frac53.$$

BA has the same regret; AA and BB have zero regret. The worst regret is therefore
`5/3`. By contrast, sales-as-demand selects `(40,40)` and has worst regret 70
over these four worlds. This comparison quantifies the value of the *supplied
scenario information*, not a demonstrated advantage of a data-driven estimator.

## 6. Remaining mathematical work

The research targets are general necessary and sufficient conditions for common
optimal actions, the minimax regret remaining when those conditions fail, and
finite-sample guarantees. A full-class guarantee needs an explicitly specified
ambiguity set and a justified computational reduction. None follows merely from
the four-scenario numerical optimization above.
