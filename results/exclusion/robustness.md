# Continuous-law and fixed-scale checks

2026-11-06. Deterministic checks of the [proof](../../docs/exclusion_robustness.md).
The midpoint laws below are discrete approximations, not iid experimental samples.

General construction: 18 instances, 66 nonterminal levels and 1932 exact rational coalition-margin checks.

Fixed continuous example: L/A = 1/10, B = 0, and minimum covariance eigenvalue 1/1875. A feasible fractional membership proves (D1-B)/A >= 967/16200 = 0.059691358. This is a lower bound, not an exact optimum.

| Midpoints per coordinate | Discrete D1 | Continuous D1 lower | Continuous D1 upper |
| ---: | ---: | ---: | ---: |
| 3 | 0.090987438 | 0.089537037 | 0.117654105 |
| 7 | 0.090063111 | 0.089537037 | 0.101491683 |
| 15 | 0.089921862 | 0.089537037 | 0.095255196 |

Each row uses three independent membership/offer primal LPs and three existing dual LPs; all nine comparisons agree to 1e-9. The intervals use the proved midpoint coupling error 2*epsilon/order, intersected with analytical bounds; they are deterministic enclosures, not confidence intervals.

Adaptive two-dimensional quadrature agrees with E|U1+(2/3)U3| = 31/54 to 1e-12. Exact scalar coalition costs agree with each discrete grid. Forecast-derived shares and the grand offer agree with the specified rule; individual forecast means also equal the true means.

Reproduce: python scripts/check_exclusion_robustness.py. Source hashes and unrounded outputs are in [robustness.json](robustness.json). These checks do not establish the general proofs, originality or publication readiness.
