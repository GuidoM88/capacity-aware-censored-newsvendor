# Post-run diagnosis of the standalone certificate

These descriptive comparisons were added after inspecting the prespecified results.
They use the saved M=4096 outcomes and do not revise either decision threshold.
The minimum of two already budgeted valid bounds needs no new observations.

## Matched combinations with the preceding face certificate

| Group | Paired + face | Bonferroni + face | DKW + face | Capacity + face | Face alone |
| --- | ---: | ---: | ---: | ---: | ---: |
| original | 0.102110 | 0.102786 | 0.103662 | 0.117914 | 0.130131 |
| heterogeneous | 0.128273 | 0.129244 | 0.129887 | 0.142224 | 0.143603 |
| controls | 0.207054 | 0.207054 | 0.203701 | 0.203701 | 0.218342 |

Entries are mean certified gap divided by maximum loss A.
On heterogeneous cases, paired + face improves this mean over DKW + face by 1.24%.
This small descriptive difference is not a general superiority claim.

## What the conditional success establishes

The paired method certifies rho >= 0.5 in all 35 original cases with true rho >= 0.6.
Bonferroni and full-budget DKW also certify all 35. Thus the conditional screen
establishes feasibility of estimating this condition on the grid, not a unique benefit.
One original law is exactly on the rho=0.5 boundary; none of the four ratio methods
certifies that boundary case. The three corresponding control cases also remain uncertified.
In all 12 exchangeable controls, the deterministic capacity ratio dominates the paired grid.
Those controls therefore do not supply evidence for additional power from the paired test.

## Population limitation versus sampling expansion

The heterogeneous population corollary has mean normalized upper gap 0.131919.
The finite paired certificate gives 0.176440; its excess over this oracle is 0.044520.
Even the exact population bound meets the 5%-of-A criterion in only 8/47 cases.
The finite bound meets it in 5/47, versus 4/47 for Bonferroni, 1/47 for DKW,
and 0/47 for face, capacity-only and 64-sample block bounds on these fresh samples.
The minimum with the face bound also meets it in 5/47. The broad half-of-cases gate fails.
This is a structural limitation of the standalone-ratio corollary on these laws,
not evidence that a different estimator of the same rho can solve the broad target.

## Checks and remaining questions

Observed failures of the four ratio methods' joint events: `{'paired': 0, 'bonferroni': 0, 'dkw_full': 0, 'capacity_full': 0}`.
The standard block baseline used 9,072 blocks and 50,232 LP solves.
It does not meet the small-gap criterion at the fixed block size. This is not a rejection
of SAA gap estimation or of other block sizes and concentration schemes.
Seven added regression tests cover zero aggregate loss, zero capacities, terminal depth,
a missed pilot state, invalid shares/witnesses, dimension penalties and a sharp obstruction.
The complete suite passed 40 tests. Coverage does not follow from that test count.

The next bounded research step is to assess the exact extremal theorem's priority
and significance as a theoretical result. The ratio certificate is now reproducible
supporting material with a measured scope. Another tuning pass on its scalar intervals
cannot remove its documented population limitation. Real-data and time-series claims
still require separate evidence.
