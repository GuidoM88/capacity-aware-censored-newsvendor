# Closed-form families for arbitrary shares

2026-11-06. Families: [docs/exact_envelopes.md](../../docs/exact_envelopes.md), Section 6.

* 1000 random instances (n = 3..6, random depth and r = k/50, shares k/sum).
* The best explicit law is valid in exact arithmetic in 1000 of 1000.
* Its value equals the certificate bound, valid for every demand law, in 1000 of 1000; then the worst gap is given by the closed-form families.
* Attaining family: C31 482, G 24, H 467, V 27.

Reproduce: `python scripts/check_general_formula.py`.
