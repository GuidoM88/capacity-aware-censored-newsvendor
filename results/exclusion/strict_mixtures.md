# Strictly stable, positive definite mixtures

2026-11-06. Argument: [docs/exact_envelopes.md](../../docs/exact_envelopes.md), Section 7.

Every mixed law below has strictly negative excess for every proper coalition, positive definite covariance and standalone ratio at least r; its gap approaches the exact worst gap as eps shrinks.

| case | r | eps | gap of the mixed law | exact worst gap | largest excess / L | min covariance eigenvalue |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| four equal shares, window | 0.25 | 0.050 | 0.470699 | 0.553571 | -3.08e-02 | 1.50e-03 |
| four equal shares, window | 0.25 | 0.010 | 0.536996 | 0.553571 | -6.15e-03 | 4.48e-04 |
| four equal shares, window | 0.25 | 0.002 | 0.550256 | 0.553571 | -1.23e-03 | 9.97e-05 |
| five equal shares, window | 0.40 | 0.050 | 0.357934 | 0.460000 | -2.40e-02 | 1.37e-03 |
| five equal shares, window | 0.40 | 0.010 | 0.439178 | 0.460000 | -4.80e-03 | 3.85e-04 |
| five equal shares, window | 0.40 | 0.002 | 0.455822 | 0.460000 | -9.60e-04 | 8.41e-05 |
| four equal shares, high regime | 0.60 | 0.050 | 0.135917 | 0.266667 | -3.08e-02 | 4.42e-03 |
| four equal shares, high regime | 0.60 | 0.010 | 0.241056 | 0.266667 | -6.15e-03 | 1.64e-03 |
| four equal shares, high regime | 0.60 | 0.002 | 0.261563 | 0.266667 | -1.23e-03 | 9.04e-04 |
| three unequal shares | 0.20 | 0.050 | 0.523839 | 0.607143 | -3.30e-02 | 3.84e-04 |
| three unequal shares | 0.20 | 0.010 | 0.590584 | 0.607143 | -6.60e-03 | 1.67e-04 |
| three unequal shares | 0.20 | 0.002 | 0.603835 | 0.607143 | -1.32e-03 | 5.20e-05 |

Reproduce: `python scripts/check_strict_mixtures.py`.
