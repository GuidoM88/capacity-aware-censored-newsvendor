# Computational prior art and publication decision

Updated **2026-10-27** after retrieving the Roels thesis. This supersedes the
2026-10-26 access limitation and pending decision for the
[sparse-tail derivation](sparse_scenarios.md).

**Decision: do not pursue the current population theorem alone as the central
contribution of a substantial research paper.** Retain the proof, solver and
checks as supporting material. This is a research-selection judgment based on
overlap and significance; it is not a proof that the entire theorem is already
published, incorrect, or unpublishable in every possible format.

## 1. The decisive comparison

[Roels (2006), MIT thesis](https://dspace.mit.edu/entities/publication/683dc5a1-2bc8-49c4-a19b-d6ab7e3273eb),
section 1.6.2, p. 58, gives a single-resource complete-demand-uncertainty case
with only one high-demand product in each of `M` scenarios. Its allocation
minimizes `max_j p_j(B-y_j)` subject to `sum_j y_j <= B`.
The model has zero ordering cost and no known CDF prefix. It therefore supplies
a direct predecessor for the mechanism, not the full fixed-prefix theorem.

Crucially, **Theorem 9, pp. 56–57, solves a relaxation** allowing a randomized
comparator `Z` with `A E[Z] <= B`. Feasibility is imposed in expectation rather
than in every realization. We do not cite it as an exact LP for our model.

The [official full PDF](https://dspace.mit.edu/server/api/core/bitstreams/c159b5e9-9e69-4605-ac0b-8d877a220027/content)
was downloaded; its checksum matches MIT's record. Reading covered pp. 49–60
and the relevant Lemma 1 / Theorem 9 proofs on pp. 181–182. Pages 56 and 58 were
also checked visually. [Access provenance](../results/audit/literature_access.json)
records the URLs, hashes and reading depth. The previously missing chapter is
no longer an obstacle to this decision.

## 2. What survives the comparison

The following is our reconstruction of the structural overlap, not a claim
that Roels states our assumptions. In the zero-cost, uninformative case, the
pairwise adversarial objective is

$$\max_{z\ge0,\;\mathbf 1^Tz\le B}\sum_i p_i(z_i-y_i)_+.$$

It is convex in `z`. The feasible simplex has vertices `0` and `B e_i`, so the
maximum is `max_i p_i(B-y_i)` for a feasible `y`; the zero vertex is redundant.
This verifies the one-high mechanism without relying on the relaxed comparator.

Our proof adds an observed prefix `t=min(z,c)`. Conditional on that prefix,
the remaining adversarial problem is convex maximization over

$$\{\delta\ge0:A_I\delta\le B-At\}.$$

The upper-tail count follows from the standard fact that a vertex has at most
`rank(A_I)` positive components. Positive overage costs can make the all-low
scenario relevant, and the prefix may have arbitrary observed marginals. These
are real differences. The zero-cost/no-prefix model is a boundary analogue,
not literally inside the positive-cost assumptions of our theorem.

We have **not** established a published theorem implying the complete
fixed-prefix rank statement. Nevertheless, the current proof uses an established
extreme-point mechanism, and the finite-atomic LP uses conventional epigraphs.
The potential contribution is consequently a model-specific extension. Its
standalone significance is insufficient for the project's intended scope,
without another substantive result or demonstrated operational consequence.
The argument is not that short proofs cannot be publishable.

## 3. Other primary-source checks

| Work and inspected location | Established content relevant here | Limit of the comparison |
| --- | --- | --- |
| [Averbakh (2004)](https://doi.org/10.1016/S0167-6377(03)00091-9), publisher abstract and introduction | Polynomial algorithms for interval-data linear resource allocation; continuous case `O(n log n)` | Linear uncertain coefficients, not our nonlinear known prefixes; full proofs not obtained |
| [Conde (2005)](https://doi.org/10.1016/j.orl.2004.11.003), publisher abstract and problem formulation | An `O(n)` algorithm for interval-profit continuous unbounded knapsack regret | Does not establish an algorithm for our whole model; full proofs not obtained |
| [Park, El-Amine and Mutlu (2021)](https://doi.org/10.1287/ijoc.2020.0999), primary abstract and online supplement A–B | Resource-allocation regret with separable convex objectives; endpoint uncertainty reduction and a shared-epigraph scenario master | Their uncertainty weights fixed cost functions; no fixed-prefix rank reduction identified in inspected material; main text not obtained |
| [Perakis and Roels (2010), companion](https://mitsloan.mit.edu/shared/ods/documents/?PublicationDocumentID=2281), proofs of Propositions 2(a) and 5 | Convex maximization/knapsack with individual bounds; a small scenario LP for single-resource nested controls | Different booking policy and comparator; its hardness does not transfer automatically |
| [van der Haar et al. (2026), arXiv v2](https://arxiv.org/abs/2610.17465v2), abstract and section 3.1, Assumptions A1–A3 / Theorem 1 | A feature-based censored-newsvendor loss characterization under conditional independence, exploration and uniqueness | Requires observation coverage around the optimal quantile; does not settle fixed-prefix coupled minimax regret |

Park et al.'s [publisher supplement](https://pubsonline.informs.org/doi/suppl/10.1287/ijoc.2020.0999/suppl_file/ijoc.2020.0999.sm1.pdf)
was directly inspected. It is sufficient evidence that these endpoint and
epigraph techniques predate the project, but not evidence of a full equivalence.
The recent contextual paper also prevents treating the addition of covariates
or a generic machine-learning model as a new direction by itself.

An, Mikhaylov and Jung (2021), previously inspected at publisher abstract and
section-excerpt level, remains adjacent interval-demand booking-control work.
Full propositions were not obtained and no equivalence is asserted. The same
access limitation remains for Vairaktarakis (2000). These limits narrow what can
be claimed about duplication; they do not require postponing our project choice.

## 4. Operational consequence for this project

- Preserve the mathematics and saved checks. No counterexample to the stated
  rank theorem was found by this literature comparison.
- Stop presenting `2^n` to `n+1` or the compact LP alone as the intended novelty.
- Do not expand benchmark volume or draft an originality claim to compensate
  for the missing central contribution.
- Reopen the publication direction only with a separately specified result:
  for example, matching statistical lower and upper bounds for coupled
  allocation beyond irreducible censoring regret, or a new tractability boundary
  under useful additional information. These are research targets, not claims
  of novelty or results already obtained.

For the statistical target, the first gate is a precisely defined sample model,
oracle and excess-risk quantity, followed by comparison against the scalar
finite-sample results in the [literature map](literature.md). A routine union
bound over retained worlds is not, by itself, the sought contribution.

The current decision is complete. A literature search cannot certify global
absence, and an internal assessment cannot guarantee acceptance. The appropriate
claim is narrower and actionable: the present evidence does not justify making
this theorem the centerpiece of the planned paper.
