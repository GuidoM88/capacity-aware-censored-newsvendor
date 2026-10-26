# Claim register

| ID | Statement | Evidence | Scientific status |
| --- | --- | --- | --- |
| C1 | A and B induce exactly the same sales law at stock 40 | Explicit CDFs; common-uniform coupling test | Analytical identity for the example |
| C2 | The toy action is identified exactly for capacity at most 80 over the stated population ambiguity class | Proof in formulation.md, section 4; analytical and numerical tests | Elementary illustrative proposition; novelty not claimed |
| C3 | At capacity 120, the four-scenario minimax decision (60,60) has worst regret 5/3 | Symmetry/convexity argument; exact loss integration; solver test | Finite-family reference only |
| C4 | Under the stated population ambiguity class, common optimal actions are exactly the upper-completion optimizers lying at or below the censoring levels | Proof in population_reduction.md, Proposition 1; independent atomic LP checks | Elementary background characterization; unique identification treated separately; novelty not claimed |
| C5 | A proposed algorithm achieves finite-sample minimax guarantees for the full ambiguity class | No algorithm/proof yet | Not established |
| C6 | The method improves operational performance on real retail data | No real-data experiment | Not established |
| C7 | The project contains a publishable original contribution | Novelty audit dated 2026-10-26 | Not established; identification alone rejected as the proposed central contribution |
| C8 | Full-class worst-case regret reduces exactly to at most 2^n endpoint completions | Proof in population_reduction.md, Proposition 2; independent LP checks | Population result under unrestricted compatible tails; no polynomial complexity or novelty claim |
| C9 | At capacity 120, the toy full-class minimax value is 60 | Symmetry and explicit lower bound; independent quadrature and grid checks | Exact illustrative calculation; distinct from C3's supplied A/B family |

Numerical tests support implementation correctness and can refute a conjecture.
They cannot certify an unrestricted mathematical theorem or establish originality.
Record counterexamples and failed checks next to the affected claim before
changing its wording or scope.
