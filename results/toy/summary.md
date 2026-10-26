# Population reference experiment

Expected costs are integrated analytically. Capacity is an upper bound, not an equality.
The finite-scenario baseline is given AA, AB, BA, BB in advance.

| Capacity | Policy | Worst regret over AA/AB/BA/BB |
| ---: | --- | ---: |
| 60 | sales_as_demand | 0.000000 |
| 60 | assume_A_tail | 0.000000 |
| 60 | finite_scenario_minimax | 0.000000 |
| 80 | sales_as_demand | 0.000000 |
| 80 | assume_A_tail | 0.000000 |
| 80 | finite_scenario_minimax | 0.000000 |
| 120 | sales_as_demand | 70.000000 |
| 120 | assume_A_tail | 1.666667 |
| 120 | finite_scenario_minimax | 1.666667 |
| 200 | sales_as_demand | 150.000000 |
| 200 | assume_A_tail | 30.000000 |
| 200 | finite_scenario_minimax | 13.333333 |
| 260 | sales_as_demand | 160.000000 |
| 260 | assume_A_tail | 40.000000 |
| 260 | finite_scenario_minimax | 13.725830 |

These results validate the constructed example. They do not establish novelty,
finite-sample guarantees, or performance on retail data.
