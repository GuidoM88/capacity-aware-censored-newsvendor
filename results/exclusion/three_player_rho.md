# Three-player structural-envelope checks

2026-11-06. See the [full proof](../../docs/three_player_rho.md).
These are deterministic checks of a derived theorem. No statistical or runtime advantage is claimed.

| Exact rho | Exact gap/L | LP gap/L | Previous ceiling |
| --- | --- | ---: | ---: |
| 1/20 | 19/30 | 0.633333333 | 0.633333333 |
| 1/10 | 3/5 | 0.600000000 | 0.600000000 |
| 1/5 | 8/15 | 0.533333333 | 0.533333333 |
| 1/3 | 4/9 | 0.444444444 | 0.444444444 |
| 2/5 | 7/20 | 0.350000000 | 0.400000000 |
| 1/2 | 1/4 | 0.250000000 | 0.333333333 |
| 4/5 | 3/40 | 0.075000000 | 0.133333333 |
| 9/10 | 19/540 | 0.035185185 | 0.066666667 |
| 1 | 0 | 0.000000000 | 0.000000000 |

All nine attaining laws have B=0. Ten mixture cases have strictly negative excess for every proper coalition and positive definite covariance, while keeping the exact prescribed rho. The eight off-family cases include optimal and shifted offers.

All 81 independent primal/dual face comparisons and 27 MILP/enumeration comparisons pass at 1e-9 tolerance. The MILPs are value checks, not branch-and-bound performance measurements.

Reproduce: python scripts/check_three_player_rho.py. The [JSON](three_player_rho.json) records every case, solver value, exact expression, input law for the off-family checks, and source hashes.
