# Research milestones

## Current foundation

- [x] Specify the offline population information model and regret comparator.
- [x] Construct observationally identical worlds with different tails.
- [x] Derive the exact threshold for the two-product example.
- [x] Implement exact expected costs and a resource-multiplier oracle.
- [x] Implement sales-as-demand, fixed-tail and finite-scenario reference policies.
- [x] Add analytical and independent numerical checks.
- [x] Create a literature map and an explicit claim register.
- [x] Audit the proposed identification contribution against nearby theorems.
- [x] Derive a general common-action characterization for the population model.
- [x] Derive an exact endpoint reduction and check mixed-tail worst cases.

## Audit decision, 2026-10-26

The general identification argument is elementary. Keep it as background rather
than treating it as the prospective central theorem. See
[novelty_audit.md](novelty_audit.md) for the evidence and access limitations.

## Next bounded investigation: computational substance

1. Derive the adversarial allocation subproblem behind the exact `2^n` endpoint
   reduction, with the distribution-aware, capacity-feasible comparator explicit.
2. Compare it against older budget-constrained regret and network revenue
   management formulations, including the relevant Roels thesis chapter.
3. Seek a tractable special case, a meaningful complexity characterization, or
   a certified approximation that is not already supplied by those methods.
4. If the result is a routine reformulation, redirect the static model before
   expanding experiments or writing a paper draft.

## Conditional next stages

- Develop a useful decision rule for the full censoring ambiguity class. Finite
  capacity already bounds regret without a common demand-mean bound; extra
  support or moment information would define a different problem.
- Introduce finite iid samples and quantify estimation error separately from
  nonidentification. Population-known prefixes are not finite-sample certificates.
- Prespecify and run comparisons with strong censoring-aware baselines under the
  same information. Use multiple demand shapes, costs, capacities and seeds.
- Consider contextual and time-dependent demand only with explicit assumptions,
  rolling evaluation and controlled censoring. Do not import iid guarantees into
  time-series experiments without justification.
- Request an independent mathematical assessment before making publication claims.
