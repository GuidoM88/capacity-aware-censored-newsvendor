# Realizability conjecture: cases outside the theorems

2026-11-06. Conjecture and method: [docs/seminorm_envelope.md](../../docs/seminorm_envelope.md), Section 6; theorems: [docs/exact_envelopes.md](../../docs/exact_envelopes.md).

Relaxed gap: best value of the seminorm relaxation found by grid search and refinement. Law gap: value of the explicit finite symmetric law built by the zonotope LP at that membership, re-evaluated with the original audit code.

| family | shares | depth | r | relaxed gap | law gap | atoms | chambers | realized |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| four producers, unequal shares | (0.310, 0.207, 0.379, 0.103) | 1 | 0.60 | 0.358621 | 0.358621 | 12 | 250 | yes |
| four producers, unequal shares | (0.231, 0.346, 0.038, 0.385) | 1 | 0.40 | 0.576923 | 0.576923 | 8 | 257 | yes |
| four producers, unequal shares | (0.133, 0.267, 0.300, 0.300) | 1 | 0.60 | 0.320000 | 0.320000 | 6 | 238 | yes |
| four producers, unequal shares | (0.370, 0.111, 0.148, 0.370) | 1 | 0.20 | 0.711111 | 0.711111 | 8 | 255 | yes |
| four producers, unequal shares | (0.100, 0.200, 0.600, 0.100) | 1 | 0.50 | 0.450000 | 0.450000 | 8 | 238 | yes |
| four producers, unequal shares | (0.040, 0.040, 0.480, 0.440) | 1 | 0.40 | 0.546000 | 0.546000 | 8 | 238 | yes |
| four producers, equal-share window | (0.250, 0.250, 0.250, 0.250) | 1 | 0.21 | 0.589663 | 0.589663 | 10 | 249 | yes |
| four producers, equal-share window | (0.250, 0.250, 0.250, 0.250) | 1 | 0.23 | 0.570621 | 0.570621 | 12 | 257 | yes |
| four producers, equal-share window | (0.250, 0.250, 0.250, 0.250) | 1 | 0.27 | 0.538315 | 0.538315 | 12 | 257 | yes |
| four producers, equal-share window | (0.250, 0.250, 0.250, 0.250) | 1 | 0.32 | 0.506939 | 0.506939 | 10 | 255 | yes |
| five producers, equal-share window | (0.200, 0.200, 0.200, 0.200, 0.200) | 1 | 0.35 | 0.511429 | 0.511429 | 26 | 7213 | yes |
| five producers, equal-share window | (0.200, 0.200, 0.200, 0.200, 0.200) | 1 | 0.40 | 0.460000 | 0.460000 | 20 | 7273 | yes |
| five producers, equal-share window | (0.200, 0.200, 0.200, 0.200, 0.200) | 1 | 0.45 | 0.424444 | 0.424444 | 16 | 7312 | yes |
| five producers, depth two, equal-share window | (0.200, 0.200, 0.200, 0.200, 0.200) | 2 | 0.25 | 0.442857 | 0.442857 | 18 | 7310 | yes |
| five producers, depth two, equal-share window | (0.200, 0.200, 0.200, 0.200, 0.200) | 2 | 0.30 | 0.414737 | 0.414737 | 18 | 7246 | yes |
| five producers, depth two, unequal shares | (0.205, 0.154, 0.282, 0.282, 0.077) | 2 | 0.15 | 0.653846 | 0.653846 | 10 | 6994 | yes |
| five producers, depth two, unequal shares | (0.125, 0.375, 0.344, 0.125, 0.031) | 2 | 0.15 | 0.717188 | 0.717187 | 10 | 7165 | yes |

17 of 17 cases are realized by an explicit law (tolerance 1e-06, zero integer excess, rho >= r).

In the depth-one windows the realized values are lower bounds on the exact worst gap, strictly below the C31 ceiling: n=4, r=0.21: 0.589663 against 0.592500; n=4, r=0.23: 0.570621 against 0.577500; n=4, r=0.27: 0.538315 against 0.547500; n=4, r=0.32: 0.506939 against 0.510000; n=5, r=0.35: 0.511429 against 0.520000; n=5, r=0.40: 0.460000 against 0.480000; n=5, r=0.45: 0.424444 against 0.440000.

Reproduce: `python scripts/check_realizability_conjecture.py` (about 15 minutes on four cores). The [JSON](realizability_conjecture.json) stores every attempt.
