# Where the face-price certificate loses precision

Post-run decomposition at 4,096 pilot and 4,096 validation observations. All amounts are divided by the maximum grand loss A.
The population calculation retains the very same pilot-fitted prices. It replaces estimated moments by their exact expectations under the known synthetic law.

| Group | True D1−B, mean | Same-price population gap bound, mean | Finite gap bound, mean | Population gap bound ≤ 5% A | Finite gap bound ≤ 5% A |
| --- | ---: | ---: | ---: | ---: | ---: |
| original | 0.000081 | 0.022144 | 0.134655 | 90/100 | 3/100 |
| heterogeneous | 0.000168 | 0.026120 | 0.149803 | 41/48 | 1/48 |
| mixtures | 0.000000 | 0.011348 | 0.098914 | 4/4 | 1/4 |

## Upper-bound slack decomposition

| Group | Population upper minus B | Finite upper minus population upper | Finite upper minus B |
| --- | ---: | ---: | ---: |
| original | 0.019878 | 0.125354 | 0.145232 |
| heterogeneous | 0.021398 | 0.128226 | 0.149625 |
| mixtures | 0.011348 | 0.141194 | 0.152541 |

This isolates conservative statistical estimation within this implementation. It does not prove that uncertainty is intrinsically this large or that a different certificate will achieve a particular rate.
All 48 heterogeneous population gaps are at most 5% A. This grid tests certification of small gaps, rather than balanced classification of small and large gaps. The explicit 7/50 structural obstruction is checked separately in the regression tests.
