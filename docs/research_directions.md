# Research direction selection

Decision date: **2026-10-28**. This is a comparison of research questions, not a
claim that any candidate is already original or publishable.

**Progress later on 2026-10-28:** the [first certificate cycle](coalition_certificate.md)
is complete. It proves a standard finite-sample bound, compares 100 synthetic
instances, and identifies an exact fractional-coalition obstruction. The current
target is reducing that structural gap; the original selection rationale remains
below for traceability.

## Decision and correction to the earlier process

Give the next bounded investigation to **finite-data certification of coalition
stability after probabilistic forecast reconciliation**. It is close to the
existing forecasting/energy work, has an explicit operational failure to measure,
and permits small mathematical checks before a forecasting implementation.

The earlier process promoted a topic before specifying its contribution, then
treated nearby literature as grounds for overly categorical rejection. We now
distinguish: a false conjecture, a result implied by a named theorem, an unresolved
overlap, and a project-priority judgment. These are different conclusions.
The previous censored-newsvendor results remain reproducible supporting work.
Their complete duplication was not established, and the earlier standalone
significance judgment was provisional, not a publication verdict.

## Three candidates compared

| Candidate and precise question | Closest work and first check | Decision |
| --- | --- | --- |
| **A. Forecasts and coalition stability.** Given a fixed forecast-based offer and cost-sharing rule, can synchronized validation observations certify the largest incentive to leave the coalition, with useful finite-sample accuracy and manageable computation? | Wen–Pinson supplies forecast-game core allocations. Doan–Nguyen already studies robust stability under partial distributional information; Wang et al. already uses robust cost sharing and constraint generation. Tran et al. learns an expected core under a different observation model and strict convexity. The three-producer example below demonstrates the forecast-to-truth distinction. | **First priority for a bounded investigation.** The possible contribution is a sharper statistical/computational guarantee, not the invention of a robust core. |
| **B. Reusable decision-focused predictions.** When the budget or feasible set changes after training, which predictions remain sufficient and how much decision quality is lost? | Tang–Khalil already trains for multiple optimization problems, including different feasible regions. In the basic risk-neutral linear-objective model, the conditional mean is sufficient for every known feasible set: see the identity below. | **Hold in its broad form.** A substantive question must specify misspecification, restricted representations, nonlinear recourse, or uncertain constraints. None is selected merely to make the problem look new. |
| **C. Targeted exploration under censored demand.** With a fixed pilot budget and shared stock capacity, which observations should be acquired to reduce final decision regret beyond the irreducible ambiguity floor? | Hssaine–Sinclair treats offline censored newsvendor learning. Wan et al. studies decision-focused experimental design with complete cost-vector labels. Online censored inventory/resource allocation is also an existing field. Endogenous censoring and final simple regret require an explicit comparison, not a generic claim about active learning. | **Backup.** Strong connection to this repository, but it needs a new experimental information model and a sharper lower-bound target before implementation. |

For B, if the only unknown is an integrable random objective vector `C`, then

$$\arg\min_{z\in Z_b(x)}\mathbb E[C^Tz\mid x]
=\arg\min_{z\in Z_b(x)}\mathbb E[C\mid x]^Tz.$$

This holds for each known `Z_b(x)`, including nonconvex feasible sets. It is a
population sufficiency statement, not a claim that finite-data training or
misspecified predictors are equally good. It refutes a blanket impossibility
of reusable forecasts in this basic model.

For C, the pilot protocol would choose stock vectors `q_t` before seeing
`min(D_t,q_t)`, under the same declared resource limits. A final policy would then
be evaluated on expected operational cost, separately from pilot-period costs.
Neither fully observed experimental-design labels nor cumulative online regret
automatically answer that question. We have not established a new rate.

## A: an explicit target, comparator, and observation model

Start with one period, bounded nonnegative production `0 <= Y_i <= R_i`, known
common imbalance penalties, and risk-neutral transferable costs. No time-series
or conditional-coverage guarantee is assumed at this stage. Let

$$\ell(q,t)=\psi^-(q-t)_++\psi^+(t-q)_+,\qquad
c_P(S)=\min_{0\le q\le R(S)}\mathbb E_P\ell(q,Y(S)).$$

A coherent predictive joint law `Q` gives an aggregate offer `q_Q` and a
forecast-core allocation `a_Q`. When `C_Q=c_Q(N)>0`, set `w_i=a_{Q,i}/C_Q`.
The implemented charge is `w_i ell(q_Q,Y(N))`, so the charges sum to realized
aggregate cost. Signed shares are allowed; nonnegative-share restrictions would
define a different problem.

Freeze `Q`, `q_Q`, and `w` before observing a validation sample of `m` iid joint
production vectors from `P`. The primary quantity to certify is

$$B_P(Q)=\max_{\varnothing\ne S\subsetneq N}
\left[w(S)\,\mathbb E_P\ell(q_Q,Y(N))-c_P(S)\right]_+.$$

The comparator allows each deviating coalition to optimize its offer under
the true law `P`. This is a distribution-aware benchmark, not a prediction of
what poorly informed producers actually do. A certificate `U_m` should satisfy
`Pr{B_P(Q) <= U_m} >= 1-delta` under stated assumptions. Reporting `U_m` must
include its conservatism; an always-large upper bound is not a useful result.
The zero-forecast-cost case and very large signed shares require separate
treatment before generalization.

**Research hypothesis to test:** the shared production observations and
imbalance-cost structure permit a substantially sharper certificate than
generic uncertainty propagation, without enumerating every coalition. No such
improvement is established here. The statistical rate, class of instances, and
computational qualification must be part of the eventual theorem.

## A diagnostic example already proved and checked

Take three binary outputs and symmetric unit penalties, so
`ell(q,t)=abs(q-t)`. For `k=1,2,3`, law `Q_k` puts equal probability on `e_k`
and `1-e_k`. Every individual output is Bernoulli with probability `1/2`, and
the aggregate output is `1` or `2` with equal probability in every world.
Thus individual distributions, the entire aggregate distribution, and scenario
coherence all agree exactly. This is stronger than passing a finite calibration
test, but weaker than a correct joint distribution.

| Optimal expected cost | Q1 | Q2 | Q3 |
| --- | ---: | ---: | ---: |
| Each singleton | 1/2 | 1/2 | 1/2 |
| Coalition 12 | 0 | 0 | 1 |
| Coalition 13 | 0 | 1 | 0 |
| Coalition 23 | 1 | 0 | 0 |
| Grand coalition 123 | 1/2 | 1/2 | 1/2 |

Under `Q1`, the vector `a=(-1/2,1/2,1/2)` is in the cost core: its sum is
`1/2` and every coalition is charged at most its standalone expected cost.
It also equals the dual allocation with scenario prices `-1,+1` for total
production `1,2`. Under `Q2`, the same allocation charges coalition 23 a cost
of `1`, while its own optimal expected cost is `0`. Both members can benefit
by leaving.

Choose `q_Q=3/2`, a valid optimal aggregate offer. Realized aggregate cost is
`1/2` in every listed state, so the proportional ex-post scaling factor is
exactly one. It does not remove this example. This does not contradict the
forecast-distribution core guarantee or demonstrate failure of the paper's
multivariate calibration diagnostic.

There is also an exact information limit. Let a *common epsilon-core allocation*
have sum `1/2` and satisfy `a(S) <= c_P(S)+epsilon` for all compatible laws.
Each pair has cost zero in at least one of these three worlds. Summing the three
pair constraints yields `1 <= 3 epsilon`. Equal charges `a_i=1/6` attain
`epsilon=1/3`. They do so for **every binary joint law with the stated individual
and aggregate distributions**, since singletons and grand cost stay fixed and
all pair costs are nonnegative. Therefore the exact common least-core tolerance
is `1/3`, not just a value from a selected finite scenario family.

The [check script](../scripts/check_coalition_information.py) uses exact rational
costs and a separate linear program. The [saved output](../results/audit/coalition_information.json)
records all worlds, coalition costs, the violating coalition and the numerical
LP check (`0.33333333333333337`). The argument above proves the extension beyond
the three enumerated worlds. **Novelty of this example is not claimed.**

## Strong existing baselines that the proposal must exceed

1. **A coherent forecast-game core.** Wen–Pinson (2025), Proposition 2 and
   equations 10–16, provides the dual allocation and proportional realized-cost
   rule. Transferring its stability statement to a different true distribution
   requires additional control. This distinction alone is not a new method.
2. **Robust core existence from partial information.** Doan–Nguyen (2020),
   accepted manuscript section 3.2, already relates stability to known marginals;
   Theorem 2 proves existence when all leave-one-out joint marginals are known.
   Its proof in Appendix C.2 was inspected. Their older 2016 preprint also has a
   three-player empty-core example with an unchanged aggregate distribution.
   Neither “dependence matters” nor “more marginal information can help” is a
   defensible novelty claim.
   Their contracts split profits proportionally; translating those conclusions
   to a cost-sharing audit requires an explicit model comparison.
3. **Robust allocation and coalition separation.** Wang et al. (2026) combines
   pessimistic grand-coalition costs, optimistic subcoalition costs and constraint
   generation. Simply adding an ambiguity set or a separation loop is insufficient.
4. **Learning a core.** Tran et al. (NeurIPS 2024) queries one coalition reward
   at a time, assumes the grand expected value is known, and obtains guarantees
   using strict convexity. Our proposed joint-observation audit has a different
   data model and does not assume a strictly convex game. That difference is a
   comparison to investigate, not proof that their results are irrelevant.
5. **Elementary dual error propagation.** In the symmetric-loss case with the
   correct aggregate law, take an optimal aggregate dual score `nu(T)` with
   `abs(nu)<=1` and `E nu=0`. Then `a_i^P=E_P[Y_i nu(T)]` is a true-core
   allocation by weak duality, and has the same total as `a^Q`. Consequently,

   $$\max_S[a^Q(S)-c_P(S)]_+
   \le\sum_i[a_i^Q-a_i^P]_+
   =\tfrac12\|a^Q-a^P\|_1.$$

   This is a direct consequence of standard dual allocation, not a proposed new
   theorem. Bounded-moment confidence intervals already give an elementary
   statistical route under these assumptions. A new certificate must improve
   something explicit over this baseline, or establish a sharp limitation.

## The initial bounded investigation (completed)

The initial deliverable was **one proposition with a proof attempt and one small
comparison**. The following scope was used; its proofs and outcomes are now in
[coalition_certificate.md](coalition_certificate.md):

1. Derive the baseline certificate for the frozen `(q_Q,w)` audit, including
   aggregate forecast error, signed weights, and bounded iid validation data.
   State which part is standard concentration/duality.
2. On small finite-support cases with 3–6 producers, compute the exact worst
   deviating coalition and compare the bound's slack. Keep zero-gain and loose
   cases. This is a structural diagnostic, not evidence of general performance.
3. Formulate one sharpened statement about certificate error or computational
   complexity, with a matching obstruction or a specified class where the
   improvement holds. Compare its assumptions and conclusion line by line
   against the closest results above; obtain Wang's full proofs before any
   claim of a new coalition-separation algorithm.
4. Continue to a larger study only if there is a meaningful surviving difference:
   a sharper guarantee with demonstrated necessity, a proved tractability
   boundary, or a reproducible operational phenomenon missed by strong baselines.
   A renamed robust core, a routine union bound, or another synthetic empty-core
   example does not meet this gate.

Stop this cycle with a written result even if the hypothesis fails. A failure
would reject the specified certificate improvement; it would not show that all
forecasting/cooperative-game research is unoriginal. Candidate C remains the
documented alternative. No new repository or large experiment is needed yet.

## Primary sources and access depth

The [source manifest](../results/audit/research_screening_sources.json) records
versions, reading scope, and hashes of retrieved PDFs. Source PDFs are not
redistributed in this repository.

| Source | Material inspected; limitation |
| --- | --- |
| [Wen & Pinson, Pooling Probabilistic Forecasts for Cooperative Wind Power Offering](https://arxiv.org/abs/2510.12382v1) | arXiv v1 (2025); section III, Propositions 2–3 and proofs, case study and conclusion; PDF pages 4–5 visually checked. arXiv describes a PSCC 2026 submission; acceptance is not asserted. |
| [Doan & Nguyen, Robust Newsvendor Games](https://doi.org/10.1287/opre.2019.1955) | Publisher metadata; [Warwick accepted manuscript](https://wrap.warwick.ac.uk/id/eprint/118743/) sections 2.2 and 3.2, Appendix C.2; Theorem 3 inspected at statement level. Also inspected [2016 arXiv v3](https://arxiv.org/abs/1403.5906v3) definitions, example and computational formulation. The versions are not interchangeable. |
| [Wang et al., Cost allocation in a robust two-stage resource allocation game](https://doi.org/10.1016/j.tre.2025.104633) | Publisher abstract, introduction and section excerpts. Full formulations and proofs not obtained. |
| [Tran et al., Learning the Expected Core of Strictly Convex Stochastic Cooperative Games](https://papers.nips.cc/paper_files/paper/2024/hash/2844b1bec82dd4be201f68715c03ed1b-Abstract-Conference.html) | Proceedings PDF: sections 3 and 5, Theorem 7 statement and accompanying explanation, conclusion. Full algorithm proofs not audited. |
| [Tang & Khalil, Multi-Task Predict-then-Optimize](https://arxiv.org/abs/2212.05403v3) | Abstract and introduction, problem scope; no independent replication. |
| [Hssaine & Sinclair, The Data-Driven Censored Newsvendor Problem](https://arxiv.org/abs/2412.01763v3) | Model and scalar identification results used in the earlier repository audit; literature discussion and conclusion revisited for this selection. |
| [Wan et al., Decision-Focused Sequential Experimental Design](https://arxiv.org/abs/2602.05340v1) | Model, observation step, assumptions and theorem statements; full proofs not audited. |

These checks support the priority decision and identify existing baselines. They
do not establish global absence of a result, empirical superiority, or a
publication-ready contribution.
