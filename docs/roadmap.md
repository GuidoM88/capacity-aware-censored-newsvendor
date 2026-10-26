# Research milestones

## Current foundation

- [x] Specify the offline population information model and regret comparator.
- [x] Construct observationally identical worlds with different tails.
- [x] Derive the exact threshold for the two-product example.
- [x] Implement exact expected costs and a resource-multiplier oracle.
- [x] Implement sales-as-demand, fixed-tail and finite-scenario reference policies.
- [x] Add analytical and independent numerical checks.
- [x] Create a literature map and an explicit claim register.

## Next decision: is there a substantive theoretical gap?

1. Reproduce the central identification argument of Hssaine and Sinclair.
2. Inspect the exact reductions of Kumar and Mouchtaki and the full offline
   multiproduct substitution paper; document whether relevant special cases
   already cover the proposed result.
3. Seek a sharp characterization for heterogeneous costs, stock boundaries and
   one shared resource. Test candidate conditions against adversarial tails.
4. Determine whether the resulting characterization exceeds a routine KKT
   reformulation. If not, keep it as background and redirect the question.

## Conditional next stages

- Specify support or moment assumptions for the full censoring ambiguity class;
  derive irreducible regret and a tractable robust decision rule.
- Introduce finite iid samples and quantify estimation error separately from
  nonidentification. Population-known prefixes are not finite-sample certificates.
- Prespecify and run comparisons with strong censoring-aware baselines under the
  same information. Use multiple demand shapes, costs, capacities and seeds.
- Consider contextual and time-dependent demand only with explicit assumptions,
  rolling evaluation and controlled censoring. Do not import iid guarantees into
  time-series experiments without justification.
- Request an independent mathematical assessment before making publication claims.
