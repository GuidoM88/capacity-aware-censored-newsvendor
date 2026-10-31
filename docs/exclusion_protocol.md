# Exclusion experiment protocol

Recorded on 2026-10-31 before running the comparison. The target is the maximum
expected saving a proper coalition could achieve by leaving a frozen cost-sharing
rule. Compare three relaxations with the integer reference. Level zero uses the
original cardinality constraint. Level one solves a face for each excluded player.
Level two checks the coalitions that omit exactly one player and solves a face
for each excluded pair. Compare against the exact population excess and, separately,
against the exhaustive upper confidence bound on the same validation data.

Reuse all 100 cases and the three validation prefixes from the first diagnostic.
Treat them as exploratory paired comparisons. Keep the original DKW and grand-loss
intervals, signed shares, nonnegative-cost clipping, and per-entry failure budget
0.05/6. All levels use the same simultaneous event for integer coalitions.

Add twelve population checks with 3 through 8 exchangeable producers and equal
shares. Use Bernoulli outputs with probability 0.37, either independent or mixed
equally with a comonotone law with the same marginals. Use the symmetric two-state
forecast on all-zero and all-one vectors with equal probabilities and unit penalties.
Check the closed form based on any one coalition of size n-1.

Add a three-producer asymmetric construction. Its equiprobable true outputs are
(1,0,0) and (0,3/5,2/5). The forecast allocates production proportionally to
(3/5,1/5,1/5) with total 3/4 or 5/4 at probabilities 3/4 and 1/4. Check that a
single exclusion can leave a strict gap. Retain both successful and loose bounds.

Record root and strengthened upper bounds, direct coalition evaluations, LP calls,
and a feasible integer witness. A verified integer witness can certify computation
has reached the exhaustive confidence bound. Distinguish that from proving the
true incentive is equal to the bound. Cross-check population and finite-sample
envelopes against standard binary MILP on the four original analytical cases,
and the additional asymmetric population case. Test monotonicity and domination of
the exhaustive answer in every row with numerical tolerance 1e-8. Report solver
work as operation counts. These small cases are unsuitable for a speed comparison.
