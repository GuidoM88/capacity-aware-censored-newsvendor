# Sparse-scenario check results

Exploratory synthetic population checks; not proof of novelty.

Seed: `2026102602`. Tolerance: `1e-07`.

Cases: **33**. Decisions checked: **792**. Maximum discrepancy: **1.137e-13**.

All endpoint worlds, the rank-bounded subset, and the compact shared
epigraph LP agree within tolerance on these cases. Both reduced
optimizers are also evaluated against every endpoint world.

| Case | Design | n | Rank | Full worlds | Selected worlds | Minimax | Max error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | one_resource | 3 | 1 | 8 | 4 | 0.00000000 | 0.000e+00 |
| 1 | one_resource | 4 | 1 | 16 | 5 | 0.97984949 | 1.066e-14 |
| 2 | one_resource | 5 | 1 | 32 | 6 | 30.67701045 | 2.842e-14 |
| 3 | one_resource | 6 | 1 | 64 | 7 | 85.80680095 | 7.105e-14 |
| 4 | one_resource | 3 | 1 | 8 | 4 | 14.63073978 | 2.132e-14 |
| 5 | one_resource | 4 | 1 | 16 | 5 | 34.66039932 | 1.421e-14 |
| 6 | one_resource | 5 | 1 | 32 | 6 | 0.00000000 | 0.000e+00 |
| 7 | one_resource | 6 | 1 | 64 | 7 | 0.02936499 | 2.842e-14 |
| 8 | one_resource | 3 | 1 | 8 | 4 | 16.78636102 | 7.105e-15 |
| 9 | one_resource | 4 | 1 | 16 | 5 | 72.53526662 | 5.684e-14 |
| 10 | one_resource | 5 | 1 | 32 | 6 | 35.99118239 | 1.421e-14 |
| 11 | one_resource | 6 | 1 | 64 | 7 | 112.86918814 | 1.137e-13 |
| 12 | two_resources | 3 | 2 | 8 | 7 | 0.00000000 | 0.000e+00 |
| 13 | two_resources | 4 | 2 | 16 | 11 | -0.00000000 | 1.066e-14 |
| 14 | two_resources | 5 | 2 | 32 | 16 | 2.86952215 | 1.421e-14 |
| 15 | two_resources | 6 | 2 | 64 | 22 | 26.49102683 | 1.421e-14 |
| 16 | two_resources | 3 | 2 | 8 | 7 | 19.04273302 | 0.000e+00 |
| 17 | two_resources | 4 | 2 | 16 | 11 | 28.56091400 | 0.000e+00 |
| 18 | two_resources | 5 | 2 | 32 | 16 | 0.00000000 | 0.000e+00 |
| 19 | two_resources | 6 | 2 | 64 | 22 | 0.83162075 | 1.421e-14 |
| 20 | three_resources | 3 | 3 | 8 | 8 | 0.76576221 | 0.000e+00 |
| 21 | three_resources | 4 | 3 | 16 | 15 | 7.31328366 | 1.066e-14 |
| 22 | three_resources | 5 | 3 | 32 | 26 | 20.23254489 | 1.421e-14 |
| 23 | three_resources | 6 | 3 | 64 | 42 | 111.45578780 | 5.684e-14 |
| 24 | three_resources | 3 | 3 | 8 | 8 | 0.00000000 | 0.000e+00 |
| 25 | three_resources | 4 | 3 | 16 | 15 | 0.00489959 | 1.776e-15 |
| 26 | redundant_rows | 5 | 1 | 32 | 6 | 48.17311026 | 2.842e-14 |
| 27 | redundant_rows | 6 | 1 | 64 | 7 | 40.40122836 | 5.684e-14 |
| 28 | redundant_rows | 3 | 1 | 8 | 4 | 29.53380079 | 7.105e-15 |
| 29 | redundant_rows | 4 | 1 | 16 | 5 | 142.38594063 | 8.527e-14 |
| 30 | individual_caps | 5 | 5 | 32 | 32 | 0.00000000 | 0.000e+00 |
| 31 | individual_caps | 6 | 6 | 64 | 64 | 0.00000000 | 0.000e+00 |
| 32 | individual_caps | 3 | 3 | 8 | 8 | 0.03130759 | 0.000e+00 |

## Counterexample to ignoring individual caps

Three independently capped products have true minimax regret **1.5**. Incorrectly retaining only one-upper worlds gives **1.0** and a decision whose actual regret is **3.0**.

See [JSON](sparse_scenarios.json) for inputs, source hashes and versions.
