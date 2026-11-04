# Standalone-cost certificate: fresh iid comparison

Generated from results.json. M pilot plus M validation observations; all methods use the same draws.
Each method-size pair has delta = 0.05/18; the 18 guarantees are simultaneous per instance at level 0.95.
This is not a 95% joint guarantee over all instances, and one draw per law is not a power study.
The estimand is D1−B, the relaxation error, not B itself. A is maximum possible grand loss.

## Mean certified gap divided by A

| Group | M | Paired | Bonferroni | DKW, 2M | Capacity, 2M | Face | Blocks | Paired + face |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| original | 256 | 0.25646 | 0.26540 | 0.21995 | 0.23639 | 0.44630 | 0.43104 | 0.25646 |
| original | 1024 | 0.17170 | 0.17819 | 0.16195 | 0.18702 | 0.27530 | 0.33506 | 0.16924 |
| original | 4096 | 0.13974 | 0.14078 | 0.13584 | 0.16412 | 0.13013 | 0.21319 | 0.10211 |
| heterogeneous | 256 | 0.31436 | 0.32209 | 0.27539 | 0.28857 | 0.41026 | 0.38948 | 0.31436 |
| heterogeneous | 1024 | 0.22194 | 0.22876 | 0.20843 | 0.23308 | 0.29096 | 0.31151 | 0.21746 |
| heterogeneous | 4096 | 0.17644 | 0.17791 | 0.17027 | 0.20169 | 0.14360 | 0.21770 | 0.12827 |
| controls | 256 | 0.33137 | 0.33137 | 0.28819 | 0.28819 | 0.66881 | 0.63629 | 0.33137 |
| controls | 1024 | 0.26165 | 0.26165 | 0.24198 | 0.24198 | 0.48030 | 0.45720 | 0.26165 |
| controls | 4096 | 0.22778 | 0.22778 | 0.21912 | 0.21912 | 0.21834 | 0.23318 | 0.20705 |

## Number certifying a gap at most 5% of A

| Group | M | Paired | Bonferroni | DKW, 2M | Capacity, 2M | Face | Blocks | Paired + face |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| original | 256 | 8/96 | 7/96 | 14/96 | 10/96 | 0/96 | 0/96 | 8/96 |
| original | 1024 | 24/96 | 21/96 | 23/96 | 10/96 | 0/96 | 0/96 | 24/96 |
| original | 4096 | 29/96 | 28/96 | 23/96 | 16/96 | 2/96 | 0/96 | 29/96 |
| heterogeneous | 256 | 0/47 | 0/47 | 0/47 | 0/47 | 0/47 | 0/47 | 0/47 |
| heterogeneous | 1024 | 0/47 | 0/47 | 1/47 | 0/47 | 0/47 | 0/47 | 0/47 |
| heterogeneous | 4096 | 5/47 | 4/47 | 1/47 | 0/47 | 0/47 | 0/47 | 5/47 |
| controls | 256 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| controls | 1024 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| controls | 4096 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |

## Conditional detection at M=4096

| Group | True rho ≥ 0.6 | Paired | Bonferroni | DKW, 2M | Capacity, 2M | Paired grid alone ≥ 0.5 | Grid strictly improves cap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| original | 35 | 35 | 35 | 35 | 24 | 36 | 61 |
| heterogeneous | 9 | 9 | 9 | 9 | 2 | 10 | 30 |
| controls | 6 | 6 | 6 | 6 | 6 | 6 | 0 |

The last two columns count all cases in the group, not only rho ≥ 0.6 cases.
Conditional gate passed: **True** (35/35; false half-certifications: 0).
Broad precision gate passed: **False**. Combined precision gate: **False**.

## Exchangeable controls at M=4096

All controls have true B=D1=0; standalone ratios need not explain their exactness.

| Case | True rho | Paired grid | Capacity rho | Final rho | Paired gap/A | Face gap/A | Blocks gap/A |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| exchangeable_n6_rho0.4 | 0.40 | 0.35 | 0.36796 | 0.36796 | 0.22257 | 0.18918 | 0.20558 |
| exchangeable_n6_rho0.5 | 0.50 | 0.40 | 0.46334 | 0.46334 | 0.23410 | 0.16631 | 0.20651 |
| exchangeable_n6_rho0.6 | 0.60 | 0.50 | 0.56405 | 0.56405 | 0.22785 | 0.24583 | 0.21217 |
| exchangeable_n6_rho0.8 | 0.80 | 0.70 | 0.77673 | 0.77673 | 0.15486 | 0.18232 | 0.22331 |
| exchangeable_n12_rho0.4 | 0.40 | 0.35 | 0.36871 | 0.36871 | 0.24707 | 0.22315 | 0.23588 |
| exchangeable_n12_rho0.5 | 0.50 | 0.40 | 0.47733 | 0.47733 | 0.25880 | 0.21624 | 0.23756 |
| exchangeable_n12_rho0.6 | 0.60 | 0.50 | 0.57224 | 0.57224 | 0.24945 | 0.21625 | 0.23792 |
| exchangeable_n12_rho0.8 | 0.80 | 0.70 | 0.77683 | 0.77683 | 0.17049 | 0.19547 | 0.23856 |
| exchangeable_n24_rho0.4 | 0.40 | 0.30 | 0.36817 | 0.36817 | 0.26079 | 0.24895 | 0.25067 |
| exchangeable_n24_rho0.5 | 0.50 | 0.40 | 0.47430 | 0.47430 | 0.27116 | 0.23519 | 0.24978 |
| exchangeable_n24_rho0.6 | 0.60 | 0.50 | 0.57383 | 0.57383 | 0.26047 | 0.28910 | 0.25001 |
| exchangeable_n24_rho0.8 | 0.80 | 0.70 | 0.78150 | 0.78150 | 0.17571 | 0.21213 | 0.25026 |

## Diagnostics and exclusions

Gap coverage failures: `{'paired': 0, 'bonferroni': 0, 'dkw_full': 0, 'capacity_full': 0, 'face': 0, 'blocks': 0}`.
Rho coverage failures: `{'paired': 0, 'bonferroni': 0, 'dkw_full': 0, 'capacity_full': 0}`. Numerical fallbacks: 0.
These observations check this run; finite-sample coverage follows from the assumptions and proof.
Four original cases were excluded before sampling because their shares were not strictly positive:

- `three_matched`
- `three_dependence`
- `n5_matched_seed104729_over3_under1`
- `n5_same_total_seed104729_over3_under1`

The block baseline solves n LPs per block. Recorded elapsed times exclude the shared pilot audit fit;
they are descriptive single-process timings, not a controlled scalability benchmark.
