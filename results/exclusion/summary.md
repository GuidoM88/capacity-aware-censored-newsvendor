# Exclusion diagnostic

Computed from saved outcomes, with tolerance 1e-8.

| Original comparisons | Level | Strict gaps | Largest gap | Mean gap | LP calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| Population vs actual excess | 0 | 5/100 | 0.1875 | 0.0030019842 | 100 |
| Population vs actual excess | 1 | 1/100 | 0.024150693 | 0.00024150693 | 446 |
| Population vs actual excess | 2 | 0/100 | 8.0491169e-16 | 7.8062556e-17 | 834 |
| Validation vs exhaustive confidence bound | 0 | 104/300 | 0.27496153 | 0.024142188 | 600 |
| Validation vs exhaustive confidence bound | 1 | 1/300 | 0.0063053127 | 2.1017709e-05 | 2676 |
| Validation vs exhaustive confidence bound | 2 | 0/300 | 2.220446e-16 | 4.4381816e-18 | 5004 |

## Validation slack above actual population excess

| Sample size | Level 0 | Level 1 | Level 2 | Exhaustive |
| ---: | ---: | ---: | ---: | ---: |
| 256 | 1.24938 | 1.23579 | 1.23579 | 1.23579 |
| 1024 | 0.707782 | 0.678145 | 0.678145 | 0.678145 |
| 4096 | 0.355056 | 0.325922 | 0.325859 | 0.325859 |

## Analytical examples

| Case | Actual | Root | One exclusion | Two exclusions |
| --- | ---: | ---: | ---: | ---: |
| Four producers | 0 | 0.1875 | 0 | 0 |
| Three asymmetric producers | 0 | 0.17142857 | 0.14 | 0 |

The validation reference is the exhaustive upper confidence bound on the same observations.
Residual statistical uncertainty is reported in the second table. Each level uses the same DKW event.
A solver call has a different cost from one coalition evaluation. The counts alone do not measure speed.
