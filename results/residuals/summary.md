# Residual certificate on fresh iid samples

Slack is the upper bound minus exact B divided by the maximum grand loss A, averaged equally across instances.
M denotes the validation size. The pilot has another M observations.

| Group | M | Fit faces | Fit grand | Forecast faces, 2M | Original moment, 2M | Exhaustive, M | Exhaustive, 2M | Gap ≤ 5% A | Width ≤ 5% A |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| original | 256 | 0.39175 | 0.38369 | 0.33415 | 0.33219 | 0.31096 | 0.23808 | 0/100 | 0/100 |
| original | 1024 | 0.29301 | 0.28340 | 0.23314 | 0.25602 | 0.17028 | 0.11699 | 0/100 | 0/100 |
| original | 4096 | 0.14523 | 0.15076 | 0.14016 | 0.16722 | 0.08084 | 0.05524 | 3/100 | 2/100 |
| heterogeneous | 256 | 0.35934 | 0.35113 | 0.32311 | 0.31394 | 0.30334 | 0.23628 | 0/48 | 0/48 |
| heterogeneous | 1024 | 0.28374 | 0.27832 | 0.26482 | 0.26957 | 0.17131 | 0.11820 | 0/48 | 0/48 |
| heterogeneous | 4096 | 0.14962 | 0.16473 | 0.19165 | 0.20585 | 0.08239 | 0.05660 | 1/48 | 1/48 |
| mixtures | 256 | 0.27590 | 0.26551 | 0.23504 | 0.23377 | 0.25772 | 0.19988 | 0/4 | 0/4 |
| mixtures | 1024 | 0.20136 | 0.19648 | 0.18440 | 0.19356 | 0.14846 | 0.10408 | 0/4 | 0/4 |
| mixtures | 4096 | 0.15254 | 0.15232 | 0.17094 | 0.17828 | 0.07659 | 0.05484 | 1/4 | 1/4 |

## Precision decision

Both prespecified conditions passed: False. The face method certified a small structural gap in 1 of 48 heterogeneous instances at M=4096.

## Four-producer obstruction example

| M | Actual B | Actual D1−B | Certified gap | Lower B | Upper B |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 256 | 0 | 0 | 1.00579 | 0 | 1.00579 |
| 1024 | 0 | 0 | 0.870684 | 0 | 0.870684 |
| 4096 | 0 | 0 | 0.385412 | 0 | 0.430412 |

## Mixture path at M=4096

| Case | B | D1−B | Certified gap/A | Width/A |
| --- | ---: | ---: | ---: | ---: |
| mixture_0 | 0.147085 | 1.38778e-16 | 0.12380 | 0.24993 |
| mixture_0.25 | 0.318647 | 2.22045e-16 | 0.15508 | 0.23622 |
| mixture_0.5 | 0.490209 | 0 | 0.09908 | 0.18006 |
| mixture_1 | 0.833333 | 0 | 0.01769 | 0.01769 |
