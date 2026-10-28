# First certificate diagnostic: prespecified scope

Recorded on 2026-10-28 before executing the new comparison script. This is a
synthetic structural investigation, not a forecasting benchmark or a novelty test.

## Model and comparisons

Use bounded nonnegative production, common positive imbalance penalties, a frozen
forecast-derived offer and signed cost shares, and iid validation vectors. The
true joint law is available only to the diagnostic evaluator. The candidate
certificate receives the fixed rule, capacity bounds and validation observations.

Compare:

1. Actual maximum coalition excess, by enumeration and weighted quantiles.
2. A fixed-score population dual upper bound, including aggregate misspecification.
3. The best common mean-zero dual-score population upper bound, by linear programming.
4. An independent fractional-coalition primal LP for the same relaxation.
5. A bounded-moment finite-sample certificate using Hoeffding and a union bound.
6. An enumeration certificate using uniform empirical-CDF bounds for coalition costs.

Items 1--4 have population information and diagnose approximation error. They are
not learning methods competing with items 5--6 under equal information. Items
5--6 use the identical validation sample. No new scientific originality is claimed
for concentration, LP duality, or fractional-coalition relaxations.

## Fixed grid

- Producer counts: 3, 4, 5, 6; capacities all one.
- Penalty pairs `(over-production, under-production)`: `(1,1)`, `(1,3)`, `(3,1)`.
- Two seeds per setting: 104729 and 130363.
- Four forecast/true-law families: identical laws; equal aggregate distribution
  with different conditional allocation across producers; independent forecasts
  versus a comonotone true law with equal individual marginals; a 30% shift of
  forecast mass to the all-one outcome.
- All 96 combinations are retained, including stable cases and zero improvements.
- Four analytical cases: matched three-producer law; its dependence-misspecified
  counterpart; four-producer stable shares with correct marginals and total law
  but a loose fixed dual score; four-producer stable shares with a suboptimal
  aggregate offer and a strict fractional-relaxation gap.
- Validation sample sizes: 256, 1024, 4096, using prefixes of one fresh draw per
  case. No selection of a preferred seed or sample size after seeing the results.
- Failure budget 0.05 per instance, split across the two certificate methods and
  three prespecified sample sizes: each entry uses `delta=0.05/6`.

The resulting simultaneous statement is per fixed instance. It is not a 95%
simultaneous guarantee across all 100 instances. Empirical coverage counts are
implementation diagnostics, not a proof of coverage or a calibration study.

## Checks and recorded outputs

Check population-bound ordering and agreement of the two LP formulations for
every instance. Independently compare enumeration against a mixed-integer model
on the four analytical cases and the first seed of each grid setting. Save every
case, forecast rule, population distribution, certificate value and sampled-state
counts, together with source hashes and dependency versions. Generate the summary
from those saved values.

Separate structural gap, sampling slack and failures. Any validation failure is
retained and inspected; a finite-sample upper bound is probabilistic, whereas a
violated population inequality or disagreement between equivalent optimizations
is an implementation/model error requiring resolution.

## Decision at the end of this cycle

Produce a proved baseline and a precise account of its limitations. If a gap
persists with known population moments, improve the coalition approximation before
investing in larger samples or a neural model. A useful next proposition must
identify how to reduce that gap, or a class where it vanishes, against existing
cooperative-game and optimization results.
