# Sparse upper-tail scenarios under resource constraints

Working derivation, **2026-10-26**. This note gives a proof for the stated
population model and a reproducible computational check. **Originality and
publication significance remain unestablished.** The vertex argument is standard;
its application must still be compared with the closest full prior papers.

## 1. Exact statement

Keep the information and loss assumptions in
[population_reduction.md](population_reduction.md): the exact joint law of
`S = min(D,c)` is known; the ambiguity class contains all compatible nonnegative,
finite-mean demand laws; costs `b_i,h_i` and censoring levels `c_i` are positive.
There are no additional demand-support, moment, smoothness or dependence
restrictions. Quantities are continuous.

Replace the single capacity constraint with a **compact packing polytope**

$$Q=\{q\in\mathbb R_+^n:Aq\le B\},\qquad A\ge0,\quad B\ge0.$$

All constraints on the order vector must be included. Write `r = rank(A)`.
Choose `U_i > max(c_i, max_{q in Q} q_i)`. For each subset `J` of products,
completion `F_J` places the censored mass at `U_i` for `i in J` and at `c_i`
otherwise, preserving the full joint sales law by coordinatewise transformations.
Let

$$R_J(q)=C_J(q)-\min_{z\in Q}C_J(z).$$

**Theorem (rank-bounded endpoint family).** For every `q in Q`,

$$\boxed{\sup_{F\in\mathcal A(S,c)}R_F(q)
=\max_{J\subseteq[n]:\ |J|\le r}R_J(q).}$$

The selected family is independent of `q`. Therefore the equality also holds
after minimizing both sides over `q`.

For one shared positive resource, `r=1`: **all-low plus the `n` single-upper
completions suffice**. The number of scenarios is at most `n+1`, rather than
`2^n`. With multiple resources it is at most

$$K(n,r)=\sum_{j=0}^{\min(r,n)}\binom nj.$$

This is a bound, not a claim that all listed scenarios are necessary in each
instance. It is polynomial in `n` for fixed `r`, and may be exponential when
`r` grows with `n`.

## 2. Proof

Define `p_i=P(S_i=c_i)`, `k_i=(b_i+h_i)p_i`, and `d_i=h_i-k_i`. Use the observable
normalized upper-completion cost

$$H_i(x)=(b_i+h_i)\mathbb E[(x-S_i)_+]-b_ix-k_i(x-c_i)_+,
\qquad H(q)=\sum_i H_i(q_i).$$

For feasible `x`, the normalized lower-completion cost is
`H_i(x)+k_i(x-c_i)_+`; above `c_i`, `H_i` has constant slope `d_i`.
Normalization subtracts a constant separately in each world and does not change
regret.

**Step 1: the pairwise adversarial objective.** The endpoint argument in
Proposition 2 of the population note applies to any compact feasible set.
For fixed `q,z in Q`, it gives

$$g(q,z):=\sup_F[C_F(q)-C_F(z)]
=H(q)-H(z)+\sum_i k_i\left[(q_i-c_i)_+-(z_i-c_i)_+\right]_+.$$

Thus the full worst-case regret is `max_{z in Q} g(q,z)`.

**Step 2: hold the observed prefix fixed.** Fix any such comparator `z`.
Put `t_i=min(z_i,c_i)` and `I={i:t_i=c_i}`. Write
`z=t+delta`, where `delta_i>=0` on `I` and `delta_i=0` elsewhere. Since
`A>=0`, the prefix `t` remains feasible. The possible tail increments form

$$P(t)=\{\delta_I\ge0:A_I\delta_I\le B-At\}.$$

This is a nonempty compact polytope: it contains zero, and every feasible tail
increment corresponds to a point of compact `Q`. For `v_i=(q_i-c_i)_+`,

$$g(q,t+\delta)-g(q,t)
=\sum_{i\in I}\big[-d_i\delta_i-k_i\min\{\delta_i,v_i\}\big].$$

Each summand is convex in `delta_i`: its slope increases from `-h_i` to
`-d_i=-h_i+k_i` at `v_i`. Consequently this objective has a maximizer at a
vertex of `P(t)`. To see this without an extra regularity assumption, express
any point as a convex combination of vertices and apply convexity; at least
one vertex has objective value no smaller.

**Step 3: a vertex has at most `r` positive tail increments.** Suppose a vertex
`delta*` had positive support `T` with more than `rank(A_I)` elements.
The columns `A_T` would be linearly dependent. There would then be a nonzero
vector `w`, supported on `T`, with `A_I w=0`. For sufficiently small `epsilon>0`,
both `delta* + epsilon w` and `delta* - epsilon w` would be nonnegative,
distinct and feasible. Their midpoint is `delta*`, contradicting extremality.
Hence `|T|<=rank(A_I)<=r`.

We have constructed `z'=t+delta*` with `g(q,z')>=g(q,z)` and at most `r`
coordinates strictly above `c`.

**Step 4: choose the associated endpoint world.** In the formula of Step 1,
the upper endpoint is needed only where

$$(z'_i-c_i)_+>(q_i-c_i)_+.$$

At equality either endpoint attains the same pairwise difference; choose lower.
The strict inequality implies `z'_i>c_i`, so the chosen upper set `J` has
at most `r` elements. For this set,

$$g(q,z)\le g(q,z')=C_J(q)-C_J(z')\le R_J(q).$$

Taking the maximum over `z` proves one inequality in the theorem. The other
holds because each selected endpoint world is in the ambiguity class. QED.

The proof allows dependent sales, atoms, zero censored mass, slack or zero
capacities, and heterogeneous costs. It does not assume identical products.

## 3. Exact algorithm for finitely supported sales laws

For each retained `J`, solve the convex oracle problem
`v_J=min_{z in Q} C_J(z)`. With finite atomic marginals, each coordinate's
expected cost is a convex piecewise-linear function. Represent its lower and
upper versions as maxima of supporting lines,

$$f_i^e(q_i)=\max_{\ell\in L_i^e}
\{\alpha_{i\ell}^e q_i+\beta_{i\ell}^e\},\qquad e\in\{L,U\}.$$

The minimax problem is then the LP

$$\begin{aligned}
\min_{q,t,\rho}\quad &\rho\\
\text{s.t.}\quad &q\ge0,\ Aq\le B,\ \rho\ge0,\\
&t_i^e\ge\alpha_{i\ell}^e q_i+\beta_{i\ell}^e
&&\text{for all }i,e,\ell,\\
&\sum_{i\notin J}t_i^L+\sum_{i\in J}t_i^U-v_J\le\rho
&&\text{for every retained }J.
\end{aligned}$$

Both cost epigraphs are shared across scenarios, giving **`3n+1` variables**
in this final LP. The representation is exact: epigraph feasibility bounds
every true scenario cost from above, and setting the epigraph variables to
their true costs is feasible. Scenario oracle values must use the same choice
of cost normalization as their epigraphs.

For rational inputs and explicitly supplied finite supports, the number and
size of the oracle LPs and the final LP are polynomial for fixed `r`. This is
not a polynomial-time claim for arbitrary implicit continuous distributions,
nor for unrestricted `r`. Continuous prefixes retain the scenario theorem,
but their integration and optimization costs depend on their representation.

The audit script implements this compact LP and compares it against a separate
formulation with a cost epigraph for each product in each of all `2^n` worlds.
It is research validation code, not yet a general public solver API.

## 4. Why the assumptions matter

**Individual caps count as constraints.** Take three products with `c_i=1`,
`S_i=1` surely, `b_i=h_i=1`, and independent order caps `0<=q_i<=2`.
Here `A=I_3` and `r=3`. Use upper completions at 3. At `q=(1,1,1)`, a world
with `|J|` upper tails has regret `|J|`. The all-upper world is necessary to
recover worst regret 3 at this decision.

More strongly, the correct full minimax value is `3/2`, attained at
`q=(3/2,3/2,3/2)`: each coordinate contributes
`max(q_i-1,2-q_i)` for `1<=q_i<=2`. Quantities below 1 are dominated by 1.
Incorrectly keeping only the all-low and single-upper worlds gives value 1
at `(1,1,1)`, with actual regret 3. For a lower bound on this incorrect value,
sum the three single-upper regrets: the sum is `q_1+q_2+q_3>=3` on `[1,2]^3`.
This is a recorded counterexample to ignoring side constraints.

In the analogous `r`-product example, the all-upper world is the unique
endpoint maximizer at `q=c`; retaining at most `r-1` upper tails underestimates
regret there. Thus the upper-support bound cannot be reduced uniformly over
rank-`r` instances.

**Restricted tails change the ambiguity set.** A known support bound below the
largest feasible order, or moment restrictions, can exclude our upper
completion. The theorem must not be reused for those classes without a new
argument. Integer quantities, substitution, nonseparable loss and dynamic
inventory also require separate analysis.

**Population information is not sample information.** Plugging an empirical
sales distribution into these LPs does not by itself provide a finite-sample
performance guarantee.

## 5. Computational evidence

Run:

```bash
python scripts/check_sparse_scenarios.py
```

The script writes the complete [JSON report](../results/audit/sparse_scenarios.json)
and a [generated summary](../results/audit/sparse_scenarios.md). The design includes
one to three shared resources, redundant rows, independent order caps, unequal
costs and censoring levels, and boundary probabilities. It checks minimax values,
the full regret of both reduced optimizers, and off-optimum decisions. The
incorrect-cap reduction is deliberately tested and preserved as a counterexample.

Finite numerical checks can falsify the proposed theorem or expose coding
errors. Its mathematical support is the argument above, which still merits
independent review. Passing checks does not certify originality.

## 6. Prior-art assessment and next decision

The [follow-up comparison](computational_prior_art.md) records what was read and
what remains inaccessible. In particular, neither extreme-point arguments nor
small scenario reductions in regret optimization are new methods in themselves.
We have not established that the theorem here is absent from the literature,
or that it would constitute a substantial paper contribution if absent verbatim.

The next gate is a direct theorem-by-theorem comparison with the older
capacity-constrained newsvendor work, especially the Roels thesis chapter.
If this is a routine specialization, retain it as background and redirect before
expanding experiments. A possible later question is which additional, useful
information assumptions change tractability; no hardness or statistical result
for those extensions is claimed here.
