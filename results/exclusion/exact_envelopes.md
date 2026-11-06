# Explicit worst-case laws: checks

2026-11-06. Theorems and proofs: [docs/exact_envelopes.md](../../docs/exact_envelopes.md).

* Equal shares, n = 3..10, every depth, r = k/60: 1910 constructions pass the exact rational check of every constraint (standalone caps, all proper coalitions, grand cost, witness value) and match the proved upper bound.
* Arbitrary shares at depth n-2, n = 3..6, 600 random rational instances: 600 constructions pass the same exact check and equal the four-line bound.
* 111 of these laws were also mapped to the unit box and re-evaluated with `ExclusionEnvelope` and `coalition_table`; all reproduce the value with zero integer excess and rho = r (tolerance 1e-6).

## Depth-one windows for equal shares

Ratios in these open intervals are the only ones where the depth-one value is not settled. The same windows appear at depth k for n - k + 1 producers.

| n | windows | total length |
| ---: | --- | ---: |
| 3 | none | 0.0000 |
| 4 | (1/5, 1/3) | 0.1333 |
| 5 | (1/3, 1/2) | 0.1667 |
| 6 | (3/7, 3/5) | 0.1714 |
| 7 | (1/2, 2/3) | 0.1667 |
| 8 | (2/5, 3/7), (5/9, 5/7) | 0.1873 |
| 9 | (5/11, 1/2), (3/5, 3/4) | 0.1955 |
| 10 | (1/2, 5/9), (7/11, 7/9) | 0.1970 |
| 11 | (7/13, 3/5), (2/3, 4/5) | 0.1949 |
| 12 | (4/7, 7/11), (9/13, 9/11) | 0.1908 |
| 13 | (3/5, 2/3), (5/7, 5/6) | 0.1857 |
| 14 | (9/17, 7/13), (5/8, 9/13), (11/15, 11/13) | 0.1892 |
| 15 | (5/9, 4/7), (11/17, 5/7), (3/4, 6/7) | 0.1902 |
| 16 | (11/19, 3/5), (2/3, 11/15), (13/17, 13/15) | 0.1897 |
| 17 | (3/5, 5/8), (13/19, 3/4), (7/9, 7/8) | 0.1880 |
| 18 | (13/21, 11/17), (7/10, 13/17), (15/19, 15/17) | 0.1856 |
| 19 | (7/11, 2/3), (5/7, 7/9), (4/5, 8/9) | 0.1827 |
| 20 | (15/23, 13/19), (8/11, 15/19), (17/21, 17/19) | 0.1795 |
| 21 | (2/3, 7/10), (17/23, 4/5), (9/11, 9/10) | 0.1760 |
| 22 | (8/13, 13/21), (17/25, 5/7), (3/4, 17/21), (19/23, 19/21) | 0.1761 |
| 23 | (17/27, 7/11), (9/13, 8/11), (19/25, 9/11), (5/6, 10/11) | 0.1756 |
| 24 | (9/14, 15/23), (19/27, 17/23), (10/13, 19/23), (21/25, 21/23) | 0.1746 |
| 25 | (19/29, 2/3), (5/7, 3/4), (7/9, 5/6), (11/13, 11/12) | 0.1733 |
| 26 | (2/3, 17/25), (21/29, 19/25), (11/14, 21/25), (23/27, 23/25) | 0.1716 |
| 27 | (21/31, 9/13), (11/15, 10/13), (23/29, 11/13), (6/7, 12/13) | 0.1698 |
| 28 | (11/16, 19/27), (23/31, 7/9), (4/5, 23/27), (25/29, 25/27) | 0.1678 |
| 29 | (23/33, 5/7), (3/4, 11/14), (25/31, 6/7), (13/15, 13/14) | 0.1656 |
| 30 | (12/17, 21/29), (25/33, 23/29), (13/16, 25/29), (27/31, 27/29) | 0.1634 |

## Sample of independently re-evaluated laws

| family | n | depth | r | regime | value | re-evaluated | atoms |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| equal shares | 3 | 1 | 7/60 | c31 (p=1) | 0.588889 | 0.588889 | 4 |
| equal shares | 3 | 1 | 7/30 | c31 (p=1) | 0.511111 | 0.511111 | 4 |
| equal shares | 3 | 1 | 7/20 | high (p=1) | 0.417857 | 0.417857 | 6 |
| equal shares | 3 | 1 | 7/15 | high (p=1) | 0.279365 | 0.279365 | 6 |
| equal shares | 3 | 1 | 7/12 | high (p=1) | 0.188492 | 0.188492 | 6 |
| equal shares | 3 | 1 | 7/10 | high (p=1) | 0.121429 | 0.121429 | 6 |
| equal shares | 3 | 1 | 49/60 | high (p=1) | 0.067971 | 0.067971 | 6 |
| equal shares | 3 | 1 | 14/15 | high (p=1) | 0.023016 | 0.023016 | 6 |
| equal shares | 4 | 1 | 7/60 | c31 (p=2) | 0.662500 | 0.662500 | 4 |
| equal shares | 4 | 1 | 7/20 | c31 (p=1) | 0.487500 | 0.487500 | 6 |
| equal shares | 4 | 1 | 7/15 | c31 (p=1) | 0.400000 | 0.400000 | 6 |
| equal shares | 4 | 1 | 7/12 | high (p=1) | 0.282738 | 0.282738 | 8 |
| equal shares | 4 | 1 | 7/10 | high (p=1) | 0.182143 | 0.182143 | 8 |
| equal shares | 4 | 1 | 49/60 | high (p=1) | 0.101956 | 0.101956 | 8 |
| equal shares | 4 | 1 | 14/15 | high (p=1) | 0.034524 | 0.034524 | 8 |
| equal shares | 4 | 2 | 7/60 | c31 (p=1) | 0.441667 | 0.441667 | 6 |
| equal shares | 4 | 2 | 7/30 | c31 (p=1) | 0.383333 | 0.383333 | 6 |
| equal shares | 4 | 2 | 7/20 | high (p=1) | 0.313393 | 0.313393 | 8 |
| equal shares | 4 | 2 | 7/15 | high (p=1) | 0.209524 | 0.209524 | 8 |
| equal shares | 4 | 2 | 7/12 | high (p=1) | 0.141369 | 0.141369 | 8 |
| shares 4/19, 6/19, 9/19 | 3 | 1 | 4/15 | g1g3 | 0.578947 | 0.578947 | 4 |
| shares 1/62, 20/31, 21/62 | 3 | 1 | 13/30 | g1g3 | 0.557527 | 0.557527 | 4 |
| shares 6/7, 1/21, 2/21 | 3 | 1 | 29/30 | g2g3 | 0.029064 | 0.029064 | 6 |
| shares 1/5, 7/20, 9/20 | 3 | 1 | 3/20 | g1g3 | 0.680000 | 0.680000 | 4 |
| shares 11/69, 20/69, 38/69 | 3 | 1 | 3/20 | g1g3 | 0.714493 | 0.714493 | 4 |
| shares 22/39, 1/39, 16/39 | 3 | 1 | 23/30 | g2g3 | 0.151654 | 0.151654 | 6 |
| shares 11/13, 1/39, 5/39 | 3 | 1 | 37/60 | g1g4 | 0.277001 | 0.277001 | 4 |
| shares 33/98, 31/98, 17/49 | 3 | 1 | 1/4 | g1g3 | 0.512755 | 0.512755 | 4 |
| shares 13/42, 5/42, 4/7 | 3 | 1 | 23/30 | g2g3 | 0.153623 | 0.153623 | 6 |
| shares 3/10, 7/18, 14/45 | 3 | 1 | 47/60 | g2g3 | 0.095912 | 0.095912 | 6 |
| shares 5/43, 11/43, 27/43 | 3 | 1 | 1/10 | g1g3 | 0.795349 | 0.795349 | 4 |
| shares 37/68, 19/68, 3/17 | 3 | 1 | 3/4 | g2g3 | 0.158701 | 0.158701 | 6 |

Reproduce: `python scripts/check_exact_envelopes.py`.
