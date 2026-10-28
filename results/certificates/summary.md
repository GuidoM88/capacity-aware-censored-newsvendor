# Coalition certificate diagnostic

Generated from `results.json`; exploratory synthetic results.

## Analytical cases

| Case | Actual excess | Fixed score | Best shared score / fractional LP |
| --- | ---: | ---: | ---: |
| three_matched | 0 | 0 | 0 |
| three_dependence | 1 | 1 | 1 |
| four_fixed_score_gap | 0 | 0.075 | 0 |
| four_fractional_gap | 0 | 0.75 | 0.1875 |

## Entire prespecified grid

| Check | Value |
| --- | ---: |
| instances | 100 |
| population_coalitions_evaluated | 2728 |
| independent_lp_equalities | 100 |
| independent_milp_checks | 52 |
| stable_instances | 36 |
| strict_fixed_score_gaps | 48 |
| strict_fractional_gaps | 5 |
| maximum_fixed_score_gap | 1.020942431 |
| maximum_fractional_gap | 0.1875 |
| maximum_lp_disagreement | 6.661338148e-16 |
| finite_certificate_evaluations | 600 |
| moment_coverage_failures | 0 |
| enumeration_coverage_failures | 0 |

## Finite samples

Means below are diagnostic averages over heterogeneous synthetic instances, not estimated deployment performance.

| Validation size | Mean moment bound minus actual excess | Mean enumeration bound minus actual excess |
| ---: | ---: | ---: |
| 256 | 1.45432 | 1.23579 |
| 1024 | 1.1158 | 0.678145 |
| 4096 | 0.810642 | 0.325859 |

Every rule and score is fixed before validation. Each entry uses delta=0.05/6,
covering the two methods and three prespecified sample sizes simultaneously per instance.
Coverage counts do not prove the confidence guarantee. Population inequalities and
independent optimizations are checked separately. All cases and sampling counts are saved.

The population best-score LP knows the true finite law; it is an oracle diagnostic,
not a finite-sample method or an equal-information competitor. Its support size may
grow exponentially in the number of producers.
