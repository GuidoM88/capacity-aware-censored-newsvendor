# Originality audit: fixed censoring and shared capacity

Date: **2026-10-26**. Decision: **do not use population identifiability alone as
the central publication contribution**. This is a research judgment supported
by the comparison and elementary derivation below, not a claim that every
possible extension has already been published.

**Subsequent update:** the bounded computational investigation below produced
the [rank-bounded endpoint derivation](sparse_scenarios.md) and a compact LP.
The [follow-up prior-art comparison](computational_prior_art.md) leaves its
originality unresolved. The identification-only assessment remains unchanged.

## Question actually audited

For separable newsvendor loss, fixed historical censoring levels, an exactly
known joint sales law, arbitrary compatible finite-mean demand tails, and one
shared capacity constraint: when is there a decision optimal in every compatible
world? What happens to regret when no such decision exists?

The current code's four A/B scenarios are a narrower information model. They
cannot establish claims about all compatible demand tails.

## Closest results and the remaining differences

The linked [literature map](literature.md) records source URLs and reading depth.

| Prior work | Result or location checked | Consequence for this project |
| --- | --- | --- |
| Hssaine and Sinclair, arXiv v3 | Model in section 2; Proposition 3.3; Theorem 3.4 and its argument | Scalar identification and irreducible regret under an observed CDF prefix are established. Their known bound on the unconstrained optimal quantile is an additional assumption; their theorem is not a coupled-allocation theorem. |
| Kumar and Mouchtaki, arXiv v2 | Definition 1, Theorem 1, Theorem 4 | Exact finite-sample regret reduction and policy optimization already exist for a scalar policy class with bounded demand. A capacity-dependent vector policy needs a separate argument; the scalar reduction cannot simply be claimed for it. |
| Shi, Chen and Duenyas (2016) | Model and Assumption 1; DDM; Theorem 2 | Multiple products, censoring and warehouse capacity already coexist in learning theory. Their adaptive inventory process obtains new observations and handles carry-over; fixed-data nonidentification is a different question. |
| Perakis and Roels (2008) | Expected-regret formulation; section 6, p. 202 | Distributional minimax regret predates this project. The conclusion explicitly points to multiproduct capacity-constrained results in Roels (2006); the thesis comparison remains incomplete. |
| Zheng et al. (2026) | Publisher abstract; companion B.1 and its proof of Proposition 1 | Offline multiproduct learning is established. The companion uses positive probability of inventory covering demand support. This differs from permanently hidden tails. The complete article was not accessible, so its special cases remain unchecked. |

Further prior-art leads are important but are **not** counted as fully audited
equivalences: Vairaktarakis (2000), Perakis and Roels' network revenue-management
work, and robust knapsack ordering. In particular, realized-demand hindsight,
distribution-aware optimal decisions, and worst expected absolute cost are
different comparators. Sharing the word "regret" or "robust" does not make two
theorems interchangeable.

## Why the proposed identification contribution is too small

For a fixed resource price `tau`, the familiar adjusted quantile is

$$F_i^{-1}\left(\frac{b_i-\tau a_i}{b_i+h_i}\right).$$

Consequently, moving the relevant quantile into an observed CDF prefix is already
suggested by standard constrained convex optimization. More decisively,
[Proposition 1 of the population note](population_reduction.md) proves the exact
common-action condition for heterogeneous products, without smoothness or
independence:

$$\operatorname*{argmin}_{q\in Q_B}H(q)\ \cap\ [0,c]\ne\varnothing.$$

Here `H` is a convex function computable from the population sales law. Its proof
uses two compatible tail completions and an elementary cost-difference
inequality. The same note distinguishes common optimality from a uniquely
identified optimizer. This supplies the previously missing general argument,
but the short reduction is insufficient evidence of a substantial research gap.

It would be inaccurate to say that the exact statement was found verbatim in
one of the checked papers. The negative assessment is instead that the proposed
central result is elementary against a well-developed surrounding literature.

## What the audit changed mathematically

The population note also derives an exact reduction to at most `2^n` endpoint
completions for full-class worst-case regret. This is background to be compared
with existing robust optimization methods, not a novelty claim or a scalable
algorithm. The reduction does not require a uniform demand-mean bound because
both the policy and its comparator obey finite capacity.

At capacity 120, the existing example has full-class minimax regret **60**, while
its four supplied A/B worlds give **5/3**. Both calculations are correct under
their respective ambiguity sets. Keeping only the all-low and all-high endpoint
worlds would also underestimate regret: mixed completions are essential.

Independent checks completed successfully:

- 24 atomic-distribution cases with 1--3 products, heterogeneous costs and
  resource weights, zero and positive capacities, and boundary atoms;
- endpoint scenarios compared with families also containing intermediate tails
  and tail mixtures, including 120 additional feasible actions;
- numerical integration and 7,381 feasible integer-grid actions for the
  continuous toy example.

The [saved report](../results/audit/population_reduction.json) contains every
case and the reproducible script hash. These checks can expose implementation
mistakes; they neither prove the general propositions nor certify originality.

## Decision and next bounded investigation

1. Retain the toy example and the new reductions as reproducible background.
2. Stop presenting identification plus capacity as the prospective main theorem.
3. Investigate **the computation of full-class minimax regret without enumerating
   all endpoint worlds**. Compare the adversarial allocation subproblem directly
   with the older budget-constrained and network-regret formulations before
   proposing a new algorithm. Establish either a useful tractable special case,
   a nontrivial complexity result, or a certified approximation beyond those
   existing methods. None is established yet.
4. If that comparison also collapses to known machinery, redirect the static
   model rather than adding forecasting models and calling the combination new.

Finite-sample estimation is still open in this repository. Merely appending a
generic concentration bound to the population reduction would not automatically
provide a sufficient contribution either.

## Search coverage and limits

Two search engines were used, followed by backward citation searches and primary
source inspection. Representative query families:

- `censored newsvendor identifiability capacity`;
- `offline censored multiproduct regret capacity`;
- `newsvendor partial identification constraints`;
- `minimax regret newsvendor capacity`;
- `Roels 2006 thesis minimax multiple products capacity constraints`;
- exact titles of the nearest papers and author/preprint versions.

The search included older work and recent revisions; no publication-year cutoff
was imposed on the main queries. Complete access to Zheng et al. and the relevant
Roels thesis chapter was not obtained. Some additional leads were inspected only
through primary abstracts. No claim of exhaustive coverage or absence of an
identical result is made. The recommendation against an identification-only
paper does not depend on resolving those remaining access gaps.
