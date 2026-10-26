# Elementary reductions for the population model

Derived during the originality audit on 2026-10-26. These are mathematical
background results, **not claims of publishable novelty**. The arguments below
are the evidence for their stated scope; numerical checks are supplementary.

## Assumptions and two compatible completions

Use the model in [formulation.md](formulation.md): positive costs and resource
weights, finite capacity, fixed positive censoring levels, and the exact joint
law of `S = min(D,c)`. The ambiguity class contains **every** nonnegative,
finite-mean joint demand law producing that sales law. No additional support,
moment, smoothness, or dependence restrictions are imposed.

Write `u_i = B/a_i`, and choose `U_i > max(c_i,u_i)`. Define compatible demand
vectors on the same probability space as the observed sales vector:

$$D_i^L=S_i,\qquad
D_i^U=\begin{cases}S_i&S_i<c_i,\\U_i&S_i=c_i.\end{cases}$$

These transformations preserve the **entire joint sales law**, even when sales
are dependent. Both completions have finite means. The numerical value of `U_i`
does not affect cost differences between feasible decisions.

Let `p_i = P(S_i=c_i)` and `d_i = (b_i+h_i)(1-p_i)-b_i`. Define the observable
convex function

$$H(q)=\sum_i\left[(b_i+h_i)\mathbb E[(q_i-S_i)_+]-b_iq_i
 -(b_i+h_i)p_i(q_i-c_i)_+\right].$$

For feasible quantities, `H(q) = C_U(q)-C_U(0)`: move the censored atom from
`c_i` to `U_i`, which lies beyond all feasible orders. Below `c_i`, the marginal
slope of `H` follows the observed CDF. Above `c_i`, it is the constant `d_i`.
Its slopes are nondecreasing, so it is convex despite the subtractive formula.

## Proposition 1: exact common-action characterization

Let `O_U = argmin_{q in Q_B} H(q)`. Then

$$\bigcap_{F\in\mathcal A(S,c)}\arg\min_{q\in Q_B} C_F(q)
=O_U\cap\{q:q_i\leq c_i\ \forall i\}.$$

**Necessity.** A common optimizer must optimize the compatible upper completion.
It must also have `q_i <= c_i`: under the lower completion, decreasing any
coordinate strictly above `c_i` to `c_i` reduces cost by `h_i(q_i-c_i)>0` and
preserves feasibility.

**Sufficiency.** Fix an upper-completion optimizer `q <= c`. For any feasible `z`
and compatible `F`, consider each coordinate. If `z_i <= c_i`, its cost
difference between `q_i` and `z_i` is completely determined by observed demand
below `c_i` and the censored mass. If `z_i > c_i`, the derivative of its true
cost beyond `c_i` is at least `d_i`, the upper completion's derivative.
Integration gives

$$C_F(z)-C_F(q)\ \geq\ H(z)-H(q)\ \geq\ 0.$$

This also covers atoms: CDF integrals determine cost differences, and the value
of a derivative at an isolated point does not change the integral. QED.

An equivalent value test is

$$\min_{q\in Q_B,\ q\leq c}H(q)=\min_{q\in Q_B}H(q).$$

Both problems are convex. Thus, the existence of a common optimal action in
this model does not require a new statistical estimator or an elaborate
identification theorem. For one resource, standard multiplier methods apply.

**Uniqueness is a different question.** Every compatible model has the same
unique optimizer if and only if `O_U` is a singleton contained in `q <= c`.
Necessity uses the compatible upper completion itself. Sufficiency follows from
the strict cost-difference inequality for every `z != q` when the upper
completion has a unique optimizer. A unique point in `O_U intersect [0,c]`
alone is insufficient: the upper completion might also have optima outside it.

For example, with one product, `b=h=c=1`, `B=2`, and observed law
`0.5 Uniform[0,1] + 0.5 delta_1`, `O_U=[1,2]`. The only common optimizer is 1,
but the upper completion has multiple optimal quantities.

## Proposition 2: exact endpoint reduction of worst-case regret

For each vector `e in {L,U}^n`, form a compatible completion by choosing its
endpoint separately for every product. For every feasible `q`,

$$\sup_{F\in\mathcal A(S,c)}R_F(q)
=\max_{e\in\{L,U\}^n}\left[C_e(q)-\min_{z\in Q_B}C_e(z)\right].$$

**Proof.** Fix feasible `q,z`. For one product, let

$$\ell_i(x,d)=b_i(d-x)_++h_i(x-d)_+.$$

On the unobserved region `d >= c_i`, the difference
`ell_i(q_i,d)-ell_i(z_i,d)` is nonincreasing in `d` when `q_i >= z_i` and
nondecreasing when `q_i < z_i`. In the first case its maximum is attained at
`c_i`; in the second it is attained at any `U_i` beyond both quantities.
Everything below `c_i` is already fixed by the sales law. Therefore

$$\sup_F[C_F(q)-C_F(z)]=\max_e[C_e(q)-C_e(z)].$$

The coordinatewise endpoint transformations above attain these bounds while
preserving the joint sales law. Interchanging two suprema, then a finite maximum
with a supremum, gives

$$\sup_F\sup_{z\in Q_B}[C_F(q)-C_F(z)]
=\max_e\sup_{z\in Q_B}[C_e(q)-C_e(z)].$$

Compactness and continuity ensure the scenario oracles exist. QED.

There are at most `2^n` endpoint scenarios. This is an exact finite reduction,
not by itself a polynomial-time algorithm. The subsequent
[sparse-tail note](sparse_scenarios.md) reduces the one-resource family to `n+1`
worlds and treats general packing constraints. This is distinct from the four A/B scenarios in
the original experiment, which are supplied complete distributions rather than
extremal completions of all compatible tails.

No uniform demand-mean bound is needed for finite regret here. For
`L_i=max(b_i,h_i)`, the loss is `L_i`-Lipschitz in the order quantity, giving

$$0\leq R_F(q)\leq\sum_i L_i B/a_i.$$

Individual absolute costs still depend on unobserved means and can be
arbitrarily large across the ambiguity class. Adding a demand-mean bound would
change the class and may exclude the constructed endpoints.

## Exact comparison for the existing example at capacity 120

Take the observed law `0.4 Uniform[0,40] + 0.6 delta_40`, costs `b=4,h=1`, and
two products with unit resource weights. Choose `U=121`. At `q=(60,60)`:

| Endpoint world | One capacity-feasible oracle | Regret |
| --- | --- | ---: |
| LL | (40,40) | 40 |
| LU | (40,80) | 60 |
| UL | (80,40) | 60 |
| UU | (60,60) | 0 |

The full-class minimax value is **60**. To see this, convexity and symmetry allow
a symmetric optimizer `(s,s)`, with `0 <= s <= 60`. For `40 <= s <= 60`, the
mixed LU regret is `120-s >= 60`. For `s < 40`, its regret is
`s^2/20 - 8s + 320 >= 80`. The table attains the lower bound at `s=60`.

The original A/B-family value `5/3` remains correct for that smaller family.
The two values answer different information problems. Sales-as-demand `(40,40)`
has full-class worst-case regret 80 at this capacity.

Checking only LL and UU would miss the mixed worst cases: their two-scenario
minimax value is `80/3`, attained at `(160/3,160/3)`, whose full-class regret is
`200/3`. This is a concrete reason not to extrapolate from a convenient scenario
subset.

## Computational checks and limits

Run `python scripts/check_population_reduction.py`. The saved
[check report](../results/audit/population_reduction.json) records its cases,
tolerance, dependency versions and source hash. The script uses linear programs
for atomic distributions and separate quadrature/grid checks for the continuous
toy example. It does not call the production allocation or robust solvers.

The results apply only to the stated population model. Finite samples, extra
distribution restrictions, substitution, nonseparable losses, and dynamic
inventory decisions require separate arguments. These reductions do not
establish novelty, finite-sample optimality, or practical superiority.
