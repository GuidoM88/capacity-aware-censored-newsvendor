# A baseline certificate and its structural limitation

Date: **2026-10-28**. This completes the first bounded investigation in
[research_directions.md](research_directions.md): a proved baseline, a small
prespecified comparison, and a precise obstruction to improving it solely with
more observations. These are research derivations and diagnostics; novelty and
publication readiness are not established.

The main finding is that a common-dual certificate can remain conservative even
with the true distribution known. On finite supports its best possible version
equals a **fractional-coalition relaxation**. The gap can therefore be a coalition
approximation error rather than a statistical error.

## 1. Fixed rule and target

Let `n>=2`, `0<=Y_i<=R_i`, and let `alpha>0` and `beta>0` penalize generation
above and below an offer, respectively. Write

$$\ell(q,t)=\alpha(t-q)_++\beta(q-t)_+.$$

Fix an offer `q0` in `[0,R(N)]` and signed shares `w` with `sum_i w_i=1`,
independently of the validation data. Realized charges are
`w_i ell(q0,Y(N))`. Define

$$L=\mathbb E\ell(q_0,Y(N)),\quad a_i=w_iL,\quad
c(S)=\min_{0\le q\le R(S)}\mathbb E\ell(q,Y(S)),$$

$$B=\max\{0,\max_{\varnothing\ne S\subsetneq N}[a(S)-c(S)]\}.$$

The deviating coalition knows the true law when optimizing its offer. The target
excludes the grand coalition: it audits incentives to leave, not aggregate offer
optimality. Those two properties must not be silently identified.

The implemented forecast rule uses an optimal forecast quantile and dual
allocation divided by forecast expected cost. It rejects forecast cost at or below
`1e-12` to avoid undefined/numerically unstable division. The certificate itself
applies to any supplied finite signed shares summing to one, including a separately
specified zero-cost fallback. No such fallback is selected here.

## 2. Population bound from one frozen score

Take a measurable score `nu(Y)` in `[-beta,alpha]`, fixed before validation.
Define `mu=E nu`, `m_i=E[Y_i nu]`, and

$$d_i(L)=w_iL-m_i+R_i(\mu)_+.$$

For a vector `v`, let

$$H(v)=\max\{0,\max_{\varnothing\ne S\subsetneq N}\sum_{i\in S}v_i\}
=\sum_i(v_i)_+-\min_i(v_i)_+.$$

**Proposition 1 (elementary population bound).**

$$B\le U_0:=\min\{H(d(L)),H(w)L\}.$$

**Proof.** The pointwise loss representation gives
`ell(q,Y(S)) >= nu(Y)(Y(S)-q)`. Taking expectations and minimizing over
`q in [0,R(S)]` gives

$$c(S)\ge m(S)-R(S)(\mu)_+.$$

Consequently `a(S)-c(S)<=d(S)`. The separate bound `c(S)>=0` gives
`B<=H(w)L`. The expression for `H` keeps every positive coordinate unless all
coordinates are positive, in which case the smallest must be omitted. This
accounts for the proper-coalition restriction. Both bounds cost `O(n)` after
the moments are available. No correct-aggregate or mean-zero-score assumption
is required. This is ordinary weak duality, not a new general principle. QED.

## 3. Finite-sample certificate, including signed shares

Let `Y^(1),...,Y^(M)` be iid validation vectors independent of the fixed rule
and score. A model trained on a separate sample is allowed by conditioning on
that training sample. Reusing validation data to choose the score invalidates
this argument unless a suitable simultaneous bound or fresh split is supplied.

Put

$$A=\max\{\beta q_0,\alpha(R(N)-q_0)\},\qquad
e=\sqrt{\frac{\log((n+3)/\delta)}{2M}}.$$

Using sample means denoted by hats, form

$$L_-=(\widehat L-Ae)_+,\quad L_+=\min\{A,\widehat L+Ae\},$$

$$m_i^- =\max\{-\beta R_i,\widehat m_i-(\alpha+\beta)R_i e\},\quad
\mu^+=\min\{\alpha,\widehat\mu+(\alpha+\beta)e\}.$$

Let `b_i=-m_i^-+R_i(mu^+)_+`. The certificate is

$$U_M=\min\left\{\max\{H(wL_-+b),H(wL_++b)\},\ H(w)L_+\right\}.$$

**Proposition 2 (standard concentration applied to Proposition 1).**
For every bounded joint law in the stated model,

$$\Pr\{B\le U_M\}\ge1-\delta.$$

**Proof.** The loss lies in `[0,A]`; the score has range width `alpha+beta`;
and `Y_i nu` lies in `[-beta R_i,alpha R_i]`. Hoeffding's inequality bounds
each one-sided failure by `exp(-2Me^2)`. There are `n` lower moment failures,
one upper score-mean failure, and two loss-mean failures. Their union has
probability at most `(n+3)exp(-2Me^2)=delta`. Independence between coordinates
or between these statistics is not required.

On the simultaneous event, `d_i(L)<=w_iL+b_i`. The function `H` is coordinatewise
nondecreasing and convex. Therefore its maximum over the single common interval
`L in [L_-,L_+]` is attained at an endpoint, including when some `w_i` are
negative. The nonnegative-cost cap also holds. Proposition 1 proves the claim.
QED.

The prototype uses the forecast's aggregate threshold score, with a bounded
tie value at atoms. Complexity is `O(Mn)` time and `O(n)` auxiliary storage if
moments are streamed; the current batch implementation keeps observations and
intermediate arrays in memory. It imposes no enumeration of coalitions. It is a conservative
baseline, not a sharp sample-complexity result, and it does not establish coverage
for time-dependent production or conditional forecasts.

### Enumeration reference under identical sample information

For each of `K=2^n-2` proper nonempty coalitions, compute its empirical minimum
cost `chat(S)`. With

$$e_c=\sqrt{\log(4K/\delta)/(2M)},\qquad
e_L=\sqrt{\log(4/\delta)/(2M)},$$

the DKW--Massart inequality and a union bound give simultaneous empirical-CDF
error at most `e_c`, with failure budget `delta/2`. Integration against the
piecewise-linear loss yields, uniformly in the offer,

$$|\widehat c(S)-c(S)|\le\max(\alpha,\beta)R(S)e_c.$$

This follows because the total variation of `t -> ell(q,t)` on `[0,R(S)]` is
`beta*q+alpha*(R(S)-q)`, bounded by `max(alpha,beta)R(S)`. Taking minima preserves
the uniform bound. Hoeffding gives the separate loss interval using `e_L` and
failure budget `delta/2`. Upper-bound `w(S)L` using its correct sign and subtract
`max(0,chat(S)-max(alpha,beta)R(S)e_c)`, then maximize over the coalitions and zero.

This benchmark is statistically valid and structurally exact in the population
limit, but enumerates exponentially many coalitions. The moment certificate
converges to `U0`, which need not equal `B`.

## 4. What even the best common score certifies

Here assume **an explicitly supplied finite true support** `y^j` with masses
`p_j`. This is a population diagnostic, not a finite-data guarantee. Let

$$V=\{\nu\in[-\beta,\alpha]^s:\sum_jp_j\nu_j=0\},\qquad
D_* =\min_{\nu\in V}H(a-\mathbb E[Y\nu]).$$

For `z in [0,1]^n`, define the cost of its fractional output bundle as
`c(z)=min_q E ell(q,z^T Y)`. The optimum lies in `[0,z^T R]`.

**Proposition 3 (exact interpretation of the relaxation).**

$$D_* = \max_{z\in[0,1]^n,\;\mathbf1^Tz\le n-1}
\{a^Tz-c(z)\},\qquad B\le D_*\le U_0.$$

**Proof.** The polytope
`Z={z in [0,1]^n:sum z<=n-1}` is the convex hull of incidence vectors of
proper coalitions and the empty coalition. To see integrality, a purported
fractional vertex with two fractional coordinates can be perturbed; with just
one, an active integer-sum constraint forces that coordinate to be integral.
Thus `H(v)=max_{z in Z}z^T v`.

The scalar offer LP gives `c(z)=max_{nu in V}E[(z^T Y)nu]`: allow an unrestricted
offer to obtain the mean-zero dual constraint; the optimizer is nonnegative and
within the production range, so this does not change the primal value. Finite
dimensional bilinear minimax/LP duality then gives

$$\min_{\nu\in V}\max_{z\in Z}\{a^Tz-\mathbb E[(z^TY)\nu]\}
=\max_{z\in Z}\{a^Tz-c(z)\}.$$

Binary coalition membership is a subset of `Z`, proving the lower inequality.
Proposition 1's loss lower bound applies equally to fractional bundles with
capacity `z^T R`, so `a^Tz-c(z)<=z^Td(L)`. The nonnegative-cost cap also extends
to `Z`. This proves the upper inequality. QED.

For implementation, use

$$H(v)=\min_{\eta\ge0}\{(n-1)\eta+\sum_i(v_i-\eta)_+\}.$$

The common-score LP has `s+n+1` variables: `s` score values, `n` epigraph
variables and `eta`. Its constraints are the score bounds, mean zero, and
`r_i>=a_i-sum_j p_j y_i^j nu_j-eta`. An independent primal LP uses membership
`z`, a common offer and scenario surplus/shortfall variables. Requiring binary
membership yields the exact mixed-integer reference. Polynomial size here means
polynomial in the **explicit support size**, which can itself be exponential in
the producer count.

### A useful general obstruction

Homogeneity gives `c(lambda*1)=lambda*c(N)`. Substituting
`z=(n-1)/n * 1` in Proposition 3 yields

$$D_*\ge\frac{n-1}{n}\,[L-c(N)].$$

The right side can be positive even when `B=0`: a suboptimal grand offer can
still leave every actual proper coalition content. Thus optimizing a single
common dual score does not, in general, remove the certificate's structural gap.

## 5. Two analytical diagnostics

Take four independent Bernoulli-half true outputs and symmetric unit loss.
Singleton, pair, triple and grand optimal costs are `1/2`, `1/2`, `3/4`, `3/4`.

**A loose fixed score that can be repaired.** Start from the uniform law on
the 16 binary states. To form the forecast, subtract `3/160` from each of
`e1,1-e1,e2,1-e2`, and add it to `e3,1-e3,e4,1-e4`. Individual marginals and
the total law remain unchanged. The forecast rule gives offer `2` and shares
`(.3,.3,.2,.2)`, hence true charges `(.225,.225,.15,.15)`. All proper-coalition
inequalities hold. The fixed total-only dual gives `U0=3/40`, while `D*=0`.
An attaining mean-zero score uses `sign(T-2)` away from `T=2`, and, at that atom,
`nu(1100)=3/5`, `nu(0011)=-3/5`, zero on the other four states. Its player moments
equal those charges. This calculation proves the repair independently of the LP.

**A gap that no common score repairs.** Let the forecast put probabilities
`3/4,1/4` on output vectors `(1/3,...,1/3)` and `(1/2,...,1/2)`. Its optimal
offer is `q0=4/3`, forecast cost `1/6`, and dual allocation gives equal shares
`w_i=1/4`. Under the true independent law the implemented expected cost is `L=1`.
Each player is therefore charged `1/4`. Every pair is charged `1/2`, and every
triple `3/4`, exactly its standalone cost; singleton charges are smaller. So `B=0`.

The fixed forecast score gives `U0=3/4`. The common-score obstruction gives
`D*>=(3/4)(1-3/4)=3/16`. Conversely, the true aggregate optimal score is
`sign(T-2)` with value zero at `T=2`, and its player moments are `3/16` each.
The residuals are all `1/16`, so `H=3/16`. Thus **D*=3/16=0.1875 exactly**.
Equivalently the fractional bundle `z=(3/4,...,3/4)` attains that excess.
The flaw is not a failed confidence statement: a positive upper bound is
conservative, not evidence that an actual coalition would leave.

## 6. Completed checks and consequence

The [protocol](coalition_certificate_protocol.md) fixes 96 grid settings and four
analytical cases, before execution. The [generated summary](../results/certificates/summary.md)
and [complete outcomes](../results/certificates/results.json) retain every case.
The run checks 2,728 population coalitions, 100 primal/dual LP equalities and 52
independent mixed-integer comparisons. Maximum LP disagreement is approximately
`6.7e-16`. The eight new tests and sixteen existing tests pass.

There are 48 strict gaps for the fixed score and five for the optimized common
score in this grid. The two finite-sample methods produce 600 bounds, with no
observed coverage violation. That count is not a coverage proof; Proposition 2
and the stated DKW construction provide the guarantees. No time-dependent or
real energy data was used. The first run reached result serialization and failed
on a NumPy boolean; the [run log](../results/certificates/run_log.json) records its
fix without changing the grid or excluding any outcomes.

**Next research target:** reduce the fractional-membership gap while retaining
a valid finite-sample certificate and avoiding full coalition enumeration. A
concrete next comparison is a hierarchy that branches on a small number of
membership variables and solves the remaining fractional subproblems, against
the exact enumeration reference and standard mixed-integer bounds. Branching
itself is established optimization machinery; a contribution would require a
proved stopping/certificate guarantee exploiting this game's structure, or a
meaningful class where few branches suffice. Nothing here proves that such a
new contribution exists.

This narrows the selected direction using an identified mathematical mechanism.
It does not reject the research area or require restarting with another topic.

## 7. Existing tools and related prior work

- [Hoeffding (1963)](https://doi.org/10.1080/01621459.1963.10500830) supplies the
  standard bounded-mean inequality used in Proposition 2. The primary paper was
  located through a [university-hosted scan](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).
- [Massart (1990)](https://doi.org/10.1214/aop/1176990746) gives the sharp DKW
  constant. The original full text was not obtained in readable form in this
  cycle; the inequality was cross-checked against the primary research exposition
  and corollaries in [Reeve (2024), arXiv v1](https://arxiv.org/html/2403.16651v1).
  Its stronger local refinements are not claimed or implemented here.
- [Samet & Zemel (1984)](https://doi.org/10.1287/moor.9.2.309) studies the
  distinction between core allocations and dual allocations in LP games.
  The publisher abstract was inspected, not its complete proofs. Thus the general
  existence of a dual/core gap is already known; Proposition 3 is our explicit
  derivation for this audit target, not an originality claim about that principle.
- Wen--Pinson, Doan--Nguyen, Wang et al. and Tran et al. remain the close sources
  mapped in [research_directions.md](research_directions.md). Wang's full algorithm
  comparison remains necessary before claiming a new separation/branching method.
