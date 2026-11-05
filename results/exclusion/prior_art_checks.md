# Checks for the prior-art comparison

2026-11-05. Deterministic algebra checks; no bibliographic-priority inference.

All 18 bounded two-state instances match the independent root LP, the existing dual implementation and the sign-clipped fixed-allocation program from Burer and Dror (2005), equation 19.

The rank-one norm and physical costs agree at 1968 membership points (all nonempty vertices plus each root LP maximizer).

| n | m | Share units | Root gap / L | Sharp supremum |
| ---: | ---: | --- | ---: | ---: |
| 3 | 2 | [1, 1, 1] | 0.666666667 | 2/3 |
| 3 | 20 | [1, 1, 1] | 0.666666667 | 2/3 |
| 3 | 200 | [1, 1, 1] | 0.666666667 | 2/3 |
| 3 | 2 | [3, 1, 2] | 0.800000000 | 5/6 |
| 3 | 20 | [3, 1, 2] | 0.826086957 | 5/6 |
| 3 | 200 | [3, 1, 2] | 0.832512315 | 5/6 |
| 6 | 2 | [1, 1, 1, 1, 1, 1] | 0.833333333 | 5/6 |
| 6 | 20 | [1, 1, 1, 1, 1, 1] | 0.833333333 | 5/6 |
| 6 | 200 | [1, 1, 1, 1, 1, 1] | 0.833333333 | 5/6 |
| 6 | 2 | [6, 1, 2, 3, 4, 5] | 0.935064935 | 20/21 |
| 6 | 20 | [6, 1, 2, 3, 4, 5] | 0.945812808 | 20/21 |
| 6 | 200 | [6, 1, 2, 3, 4, 5] | 0.951469583 | 20/21 |
| 8 | 2 | [1, 1, 1, 1, 1, 1, 1, 1] | 0.875000000 | 7/8 |
| 8 | 20 | [1, 1, 1, 1, 1, 1, 1, 1] | 0.875000000 | 7/8 |
| 8 | 200 | [1, 1, 1, 1, 1, 1, 1, 1] | 0.875000000 | 7/8 |
| 8 | 2 | [8, 1, 2, 3, 4, 5, 6, 7] | 0.961111111 | 35/36 |
| 8 | 20 | [8, 1, 2, 3, 4, 5, 6, 7] | 0.967171717 | 35/36 |
| 8 | 200 | [8, 1, 2, 3, 4, 5, 6, 7] | 0.971439750 | 35/36 |

All actual proper coalitions are strictly stable in these 18 laws.

For the separate exact three-producer example, z=(1,0,2/3): physical cost 0, assigned charge 5/18, canonical extension cost 2/3. Both extensions agree on every actual coalition.

An additional algebra-only case checks positive-part clipping when the unmodified minimum is +1/2. Its charges are deliberately not budget balanced; it is not an additional calibrated example.

Reproduce with `python scripts/check_exclusion_prior_art.py`. The proof and scope are in [the comparison](../../docs/exclusion_prior_art.md).

## Execution and recovery record

The script completed with exit code 0. The observed console result was:

    Passed 18 three-way root comparisons, 1968 cost identities, canonical-extension LP and clipping case.

The four existing tests in `test_exclusion.py` also completed successfully:

- test_exchangeability_can_include_strong_dependence
- test_finite_terminal_level_matches_clipped_enumeration_with_signed_shares
- test_larger_coalitions_are_retained_at_level_two
- test_one_exclusion_closes_the_known_three_sixteenths_gap

The local environment subsequently became unavailable before the GitHub update.
This table is recovered from the displayed, generated Markdown, retaining its
nine-decimal precision. The script is recovered from the recorded source.
No fresh execution after recovery is claimed. The complete new JSON and its
SHA-256 manifest remained in the unavailable environment and are **not included
in this commit**. Re-running the script generates them; no raw solver records
or source hashes have been invented. Previous committed result files are unchanged.
