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

## Current priority, 2026-11-01

The [comparative selection](research_directions.md) gives the first investigation
to finite-data certification of coalition stability after forecast reconciliation.
It records three candidates, their closest work, and why the other two are held
or retained as a backup.

- [x] Compare the candidate questions before expanding implementation.
- [x] Specify the forecast-based rule, true-law comparator and validation data.
- [x] Prove and independently check the three-producer information diagnostic.
- [x] Identify robust-game, core-learning and elementary duality baselines.
- [x] Derive the baseline certificate for frozen offers and signed cost shares.
- [x] Measure certificate slack against exact coalition checks on small cases.
- [x] Characterize the best common-dual bound as a fractional-coalition relaxation.
- [x] Prove an exact structural gap, separating it from sampling uncertainty.
- [x] Solve a hierarchy of whole-producer exclusions and compare with the exact
  population and finite-sample optimization references.
- [x] Prove an exact exchangeable case and a constant gap at every fixed depth
  in a family with heterogeneous production.
- [x] Construct and prove a validation bound using separately learned face prices,
  including score-mean drift. Record statistical slack and operation counts.
- [x] Compare six methods on fresh samples with equal-total-budget references.
- [x] Execute chronological measured and modeled wind checks and report all outcomes.
- [x] Decide whether the face-price method warrants scaling as the main result.
  It fails the prespecified precision gate. Retain the negative result.
- [x] Isolate the statistical expansion while keeping learned prices unchanged.
- [x] Match the paired block statistic to Mak, Morton and Wood (1999), Theorem 1
  and §3.2. Use it as the statistical comparison.
- [x] Compare core testing and fractional participation to Chen and Zhang,
  Aubin and Denault, and derive the sharp worst-case exclusion error for each
  positive cost split. [Publication assessment](publication_assessment.md)
- [ ] Compare that precise extremal formula with further work and assess whether
  the standalone-cost bound can yield useful finite-data precision.
- [ ] Prespecify a fixed-budget comparison of paired aggregate-gap estimation,
  including block-size bias, a frozen feasible witness, fresh streams and strong
  equal-budget references. Keep the current cases as development data.
- [ ] Derive and test a sharper finite-sample or computational tradeoff. Decide
  whether it goes beyond the standard sample-average optimization baseline.

The first cycle gave a moment certificate and identified its fractional-membership
gap. The second cycle established an exact class and a worst-case boundary for
closing that gap. The comparison isolates the remaining statistical slack even
when the integer optimization has been solved exactly.
[First cycle](coalition_certificate.md) · [Second cycle](exclusion.md) ·
[Third cycle and decision](face_residuals.md)

The third cycle has a valid learned-price certificate but insufficient precision.
The same learned prices satisfy the gap target in 41/48 heterogeneous cases with
exact moments and 1/48 with estimated intervals. The next investigation targets
that statistical expansion. The research question remains unchanged. Runtime
superiority and guarantees under temporal dependence remain unresolved.

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
