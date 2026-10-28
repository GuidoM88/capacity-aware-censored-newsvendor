# Claim register

| ID | Statement | Evidence | Scientific status |
| --- | --- | --- | --- |
| C1 | A and B induce exactly the same sales law at stock 40 | Explicit CDFs; common-uniform coupling test | Analytical identity for the example |
| C2 | The toy action is identified exactly for capacity at most 80 over the stated population ambiguity class | Proof in formulation.md, section 4; analytical and numerical tests | Elementary illustrative proposition; novelty not claimed |
| C3 | At capacity 120, the four-scenario minimax decision (60,60) has worst regret 5/3 | Symmetry/convexity argument; exact loss integration; solver test | Finite-family reference only |
| C4 | Under the stated population ambiguity class, common optimal actions are exactly the upper-completion optimizers lying at or below the censoring levels | Proof in population_reduction.md, Proposition 1; independent atomic LP checks | Elementary background characterization; unique identification treated separately; novelty not claimed |
| C5 | A proposed algorithm achieves finite-sample minimax guarantees for the full ambiguity class | No algorithm/proof yet | Not established |
| C6 | The method improves operational performance on real retail data | No real-data experiment | Not established |
| C7 | The project contains a publishable original contribution | Identification audit, 2026-10-26; computational assessment, 2026-10-27; comparative selection, 2026-10-28 | Not established; selecting a question for investigation is not a publication verdict |
| C8 | Full-class worst-case regret reduces exactly to at most 2^n endpoint completions | Proof in population_reduction.md, Proposition 2; independent LP checks | Population result under unrestricted compatible tails; no polynomial complexity or novelty claim |
| C9 | At capacity 120, the toy full-class minimax value is 60 | Symmetry and explicit lower bound; independent quadrature and grid checks | Exact illustrative calculation; distinct from C3's supplied A/B family |
| C10 | Under the unrestricted population-tail model and continuous compact packing constraints, at most rank(A) upper tails suffice for worst regret at every decision; one resource needs at most n+1 worlds | Proof in sparse_scenarios.md; full endpoint enumeration checks; prior-art comparison in computational_prior_art.md | Retained as supporting work; exact full prior equivalence not established; standalone direction deprioritized by a provisional significance judgment |
| C11 | With explicit finite rational sales supports, full-class minimax admits polynomial-size LP computation for fixed rank(A), including a final LP with 3n+1 variables | Construction in sparse_scenarios.md; separate full and shared-epigraph LP checks | Population algorithm; no finite-sample guarantee or polynomial claim for growing rank or arbitrary implicit distributions |
| C12 | Ignoring individual order caps invalidates the one-upper reduction | Three-product analytical counterexample; saved LP results give true minimax 1.5 versus incorrect value 1 and actual regret 3 | Negative result preserved; all order constraints must enter the geometry |
| C13 | The full fixed-prefix rank theorem has already been published in an equivalent form | No complete reduction or identical theorem established by the inspected sources | Not established; the negative research decision is not a proof of duplication |
| C14 | Identical binary individual and aggregate laws can conceal different coalition incentives; the stated three-player ambiguity class has exact common least-core tolerance 1/3 | Analytical argument in research_directions.md; rational cost calculations and independent LP in coalition_information.json | Correct diagnostic under its stated cost and allocation model; novelty not claimed |
| C15 | A useful new finite-data certificate for forecast-based coalition stability has been obtained | A precise target and existing baselines are specified; no new estimator or guarantee proved | Not established; selected research hypothesis only |
| C16 | With the correct aggregate law and a common optimal symmetric-loss dual score, worst coalition excess is at most half the L1 error between forecast and true dual allocations | Direct weak-duality argument in research_directions.md | Elementary baseline; not a new theorem or a guarantee under arbitrary aggregate forecast error |

The current research priority is recorded in
[research_directions.md](research_directions.md). The earlier
[computational assessment](computational_prior_art.md) remains available with a
dated clarification: a provisional significance judgment is not a proof of
duplication or a prediction that every venue would reject a short extension.

Numerical tests support implementation correctness and can refute a conjecture.
They cannot certify an unrestricted mathematical theorem or establish originality.
Record counterexamples and failed checks next to the affected claim before
changing its wording or scope.
