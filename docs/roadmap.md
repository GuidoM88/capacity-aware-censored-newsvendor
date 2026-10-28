# Research milestones

## Completed foundation

- [x] Specify the offline population information model and regret comparator.
- [x] Construct observationally identical worlds with different tails.
- [x] Derive the exact threshold for the two-product example.
- [x] Implement exact expected costs and a resource-multiplier oracle.
- [x] Implement sales-as-demand, fixed-tail and finite-scenario references.
- [x] Add analytical and independent numerical checks.
- [x] Create a literature map and an explicit claim register.
- [x] Audit identification as a proposed central contribution.
- [x] Derive the general common-action and full endpoint reductions.
- [x] Derive the rank-bounded family, including `n+1` worlds for one resource.
- [x] Implement a compact finite-atomic LP and compare it with full enumeration.
- [x] Preserve the counterexample when individual caps are ignored.
- [x] Retrieve and compare the relevant Roels thesis section and proofs.
- [x] Decide whether the current computational result justifies the planned paper.

## Current priority, 2026-10-28

The [comparative selection](research_directions.md) gives the first investigation
to finite-data certification of coalition stability after forecast reconciliation.
It records three candidates, their closest work, and why the other two are held
or retained as a backup.

- [x] Compare the candidate questions before expanding implementation.
- [x] Specify the forecast-based rule, true-law comparator and validation data.
- [x] Prove and independently check the three-producer information diagnostic.
- [x] Identify robust-game, core-learning and elementary duality baselines.
- [ ] Derive the baseline certificate for frozen offers and signed cost shares.
- [ ] Measure certificate slack against exact coalition checks on small cases.
- [ ] Formulate and assess one sharper statistical or computational proposition.
- [ ] Decide whether its precise difference warrants a larger study.

There is no new statistical method or publication-ready theorem yet. The next
cycle has a written proof/comparison deliverable; it does not start with a new
neural model, dataset collection or manuscript claim.

## Previous decision, 2026-10-27; clarified 2026-10-28

**Deprioritize the population identification or sparse-scenario results alone
as the central paper contribution.** Retain them as supporting material. The
[completed assessment](computational_prior_art.md) records the evidence and
distinguishes this significance judgment from an unproved claim of duplication.
The judgment is provisional, not a conclusion that the results are unpublishable.
The earlier [identification audit](novelty_audit.md) is preserved as history.

## Backup within censored demand

A concrete candidate question is whether coupled capacity changes the sharp
finite-sample cost of learning beyond the irreducible regret from hidden demand.
This is a question to investigate, not a verified original direction.

1. Specify finite iid censored observations, the admissible demand class and the
   comparator. Distinguish learning error from the population minimax floor.
2. Check whether scalar finite-sample results already imply the intended rate.
   Identify precisely where coupling prevents their direct application.
3. Seek a matching lower bound and an attaining allocation method, with explicit
   dependence on the information and resource geometry. Generic concentration
   for the existing plug-in LP is not enough for the intended contribution.
4. If no substantive gap survives, redirect before adding a forecasting model,
   a large dataset or a manuscript draft.

An alternative computational continuation would require a meaningful new
tractability boundary under additional tail information. No hardness theorem or
new algorithm for that extension is currently established.

## Stages conditional on a defensible contribution

- Prespecify comparisons with strong censoring-aware baselines under identical
  information, including splits, costs, capacities and evaluation metrics.
- Separate population-known prefixes from finite-sample certificates.
- For contextual or time-dependent demand, state assumptions and use rolling
  evaluation with controlled censoring; iid results do not automatically apply.
- Seek independent mathematical review before asserting publication readiness.
