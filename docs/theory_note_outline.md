# Sharp overstatement of coalition savings in newsvendor relaxations

Internal theoretical-note outline, 2026-11-05. Not submitted. This title does
not claim a new relaxation or a new general forecasting algorithm.

## Proposed abstract

Fractional coalition optimization provides a tractable upper bound on the
largest saving available to a coalition under a fixed cost allocation.
We characterize its worst-case overstatement for an exclusion hierarchy in
a newsvendor cost game. For any prescribed positive allocation shares, the
supremum of the gap divided by expected grand-coalition cost equals the sum
of the largest retained shares at every nonterminal exclusion depth.
A common sequence of bounded two-state instances approaches these values,
has a correct forecast of total output, and gives strictly negative excess
to every actual proper coalition. The construction also yields an immediate
sharp root bound and a norm-cost representation. A standalone-cost condition
reduces the bound, with an iid validation procedure as supporting material.
The result describes an intrinsic limitation of fractional certification;
it does not establish general statistical or computational superiority.

## Argument and evidence

1. **Question and established baseline.** Define fixed charges, true optimized
   coalition cost, positive excess, and the physical extension. Credit the
   fractional-game literature and the 2005 fixed-allocation newsvendor
   relaxation. Use [the exact mapping](exclusion_prior_art.md), including its
   distinction from optimizing the allocation.
2. **One central theorem.** State C30 with all quantifiers: each $n\ge3$,
   every prescribed $w>0$, every $1\le k\le n-2$, supremum over compatible
   bounded laws. State terminal exactness separately.
3. **Proof.** Give the charge-budget upper bound and the two-state family.
   Include integer strict stability, realization of the prescribed shares
   by an aggregate-correct forecast, and the fractional zero-cost witness.
   The [complete existing derivation](publication_assessment.md) supplies
   these steps. Do not describe the absolute-sum construction device as new.
4. **Interpretation.** Add the root corollary and norm-cost transfer. Explain
   why canonical extension results do not imply exactness for the physical
   extension, using the three-producer calculation.
5. **Scope of improvement.** Present the $1-\rho$ refinement as a short
   sufficient-condition corollary. Put the full statistical conversion and
   experiment tables in an appendix or companion material. Report the
   matched-baseline conditional successes and broad precision failure.
6. **Limitations.** The sharpness scale is expected cost $L$, not maximum
   loss $A$; their ratio vanishes in the bounded limiting family.
   Aggregate calibration permits individual forecast errors.
   The result is not a lower bound for every efficient certificate and does
   not assess a reoptimized allocation or full nucleolus procedure.

## Reviewer-facing statement of the proposed increment

The manuscript's claim would be the exact extremal value for prescribed
shares and exclusion depth under the stated realizability restrictions.
The convex relaxation, core/dual distinction, two-state cost identity,
coordinate restrictions and statistical tools all have precedents.
The focused comparison found no identical quantitative statement in the
inspected results; it does not rule out an uninspected equivalent theorem.

The note is ready to be assembled from the linked proofs for a significance
review, not certified ready for submission. A substantive objection would
identify an existing theorem that implies the exact formula, a flaw in the
realization/quantifiers, or why the quantitative limitation is too incremental
for the intended readership. Mere overlap with cooperative games is not
such an objection. No external review or submission has occurred.
