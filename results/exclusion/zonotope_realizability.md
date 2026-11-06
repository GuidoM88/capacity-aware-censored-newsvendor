# Realizability of relaxed envelope values

2026-11-06, branch `pulp-fiction`. For each case the seminorm oracle gives a maximizing membership; a zonotope LP finds a finite centrally symmetric law on the unit box; that law is evaluated independently with `ExclusionEnvelope` and `coalition_table`. See [docs/seminorm_envelope.md](../../docs/seminorm_envelope.md), Section 6.

| case | shares | r | relaxed gap | verified law gap | atoms | proved bound | exact at r |
| --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |
| three equal shares, C39 low regime | (0.333, 0.333, 0.333) | 0.20 | 0.533333 | 0.533333 | 6 | 0.533333 | yes |
| three equal shares, C39 high regime | (0.333, 0.333, 0.333) | 0.50 | 0.250000 | 0.250000 | 8 | 0.250000 | yes |
| three unequal shares | (0.6, 0.25, 0.15) | 0.20 | 0.607143 | 0.607143 | 6 | 0.607143 | yes |
| three unequal shares | (0.7, 0.2, 0.1) | 0.30 | 0.497872 | 0.497872 | 6 | 0.497872 | yes |
| three proportional charges | (0.333, 0.333, 0.333) | 0.17 | 0.104608 | 0.104608 | 8 | 0.104608 | yes |
| three proportional charges | (0.333, 0.333, 0.333) | 0.30 | 0.233333 | 0.233333 | 8 | 0.233333 | yes |
| four equal shares, C31 regime | (0.25, 0.25, 0.25, 0.25) | 0.15 | 0.637500 | 0.637500 | 8 | 0.637500 | yes |
| four equal shares, window | (0.25, 0.25, 0.25, 0.25) | 0.25 | 0.553571 | 0.553571 | 14 | 0.562500 | no |
| four equal shares, window | (0.25, 0.25, 0.25, 0.25) | 0.30 | 0.518421 | 0.518421 | 10 | 0.525000 | no |
| four equal shares, high regime | (0.25, 0.25, 0.25, 0.25) | 0.60 | 0.266667 | 0.266667 | 8 | 0.266667 | yes |
| four proportional charges, strong pooling | (0.25, 0.25, 0.25, 0.25) | 0.04 | 0.540000 | 0.540000 | 8 | 0.720000 | no |
| four proportional charges | (0.25, 0.25, 0.25, 0.25) | 0.14 | 0.640000 | 0.640000 | 8 | 0.645000 | no |

12 of 12 relaxed values are attained by an explicit law with zero integer excess and rho = r, both up to the solver tolerance 1e-06. In 8 cases the attained value equals a proved upper bound, so it is the exact worst gap at that ratio. Elsewhere it is a lower bound on the exact worst gap; the relaxation's own maximum there is not certified.

Reproduce: `python scripts/check_zonotope_realizability.py`. The [JSON](zonotope_realizability.json) stores each law (states, probabilities, offer).
