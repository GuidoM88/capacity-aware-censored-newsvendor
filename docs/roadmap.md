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
- [x] Derive a rank-bounded upper-tail family, with `n+1` worlds for one resource.
- [x] Implement a compact finite-atomic LP and compare it with full enumeration.
- [x] Preserve an explicit counterexample when individual caps are ignored.

## Audit decision, 2026-10-26

The general identification argument is elementary. Keep it as background rather
than treating it as the prospective central theorem. See
[novelty_audit.md](novelty_audit.md) for the evidence and access limitations.

## Computational investigation: current result and remaining gate

The [sparse-tail note](sparse_scenarios.md) now supplies the adversarial reduction
and a polynomial finite-atomic algorithm for fixed resource rank. This is a
candidate structural result, not an established original contribution. The
[prior-art follow-up](computational_prior_art.md) records the comparison so far.

1. Obtain and compare the relevant Roels thesis chapter and closest
   budget-constrained newsvendor theorems, including the exact comparator.
2. Determine whether the rank-bounded family is already implied by those results.
   Seek an independent review of both the mathematics and significance.
3. If it is a routine specialization, retain the result as background and
   redirect. One possible question is how useful restrictions on the unknown
   tails change tractability; no hardness or new statistical claim is proved.
4. Expand empirical work or start a manuscript only after this gate yields a
   defensible contribution. A generic concentration bound is not automatically
   enough to turn the population theorem into a paper.

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
