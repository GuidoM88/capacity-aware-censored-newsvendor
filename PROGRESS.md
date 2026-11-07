# Progress report

**Exact worst-case error of fractional coalition audits in pooled newsvendor games**

Last updated: 7 November 2026 · branch `pulp-fiction`

This page summarizes where the project stands: what has been proved, how it
has been checked, what is still open and what comes next. The detailed
research log, with the reasons behind each step, is in
[PULP_FICTION.md](PULP_FICTION.md).

## The question

Producers that pool their imbalance risk share the expected cost of a joint
offer. A cost split is stable if no group of producers would pay less on its
own, but checking every group is NP-hard, so in practice the check is relaxed
to fractional memberships. The relaxation can only overstate the saving
available to a real coalition. We ask by how much, in the worst case over all
demand distributions, when every producer is known to pay at least a fraction
r of its standalone cost and k producers are excluded from the search.

The November 5 draft answered only the case without this information: the
overstatement can be as large as the trivial bound. That result was correct
but thin. Everything below is new since then.

## Main results

| # | Result | Status | Where |
| --- | --- | --- | --- |
| 1 | Equal shares, every n, depth k and r: the elementary ceiling (1-r)(n-k)/n is exact on explicit intervals of r; above (m-1)/(m+1), with m = n-k, the exact value is (m-1)(1-r^2)/(2nr) | Proved; algebra verified symbolically | Theorem 1, [notes](docs/exact_envelopes.md) |
| 2 | Equal shares, the "windows" between those intervals: the exact value is the larger of two explicit families, and the sign of Q(r) = mr^2 + 2(p-1)r + 2 + 2p - m decides which | Proved; algebra verified symbolically | Theorem 4 |
| 3 | Consequence: closed form for equal shares at every n, depth and r (e.g. the complete four-producer curve) | Proved | Corollary, Figure |
| 4 | Arbitrary shares at the deepest level k = n-2: closed form with three regimes per pair of producers | Proved; algebra verified symbolically | Theorem 2 |
| 5 | Arbitrary shares at every depth: four explicit families of worst-case laws | Three families proved in general; the fourth checked instance by instance | Theorem 5 |
| 6 | Arbitrary shares at every depth: the worst case equals the best of the four families | Conjecture; held in 1068 of 1068 random instances against a certified upper bound | Conjecture 6 |
| 7 | Requiring positive definite covariance and strict stability of every coalition changes none of the worst cases | Proved; algebra verified symbolically | Proposition 5 |
| 8 | Every worst case is attained by an explicit finite demand law (at most 2n atoms) | Proved for results 1 to 5 | Constructions |
| 9 | Asymmetric penalties (surplus and shortfall priced differently, ratio kappa): the elementary ceiling stays valid and every symmetric worst case stays attainable, so asymmetry can only increase the overstatement | Proved | Lemma 1 to Corollary 3, [notes](docs/asymmetric_penalties.md) |
| 10 | Asymmetric penalties, last depth, arbitrary shares: closed form for every kappa (three regimes) | Proved; algebra verified symbolically | Theorem A |
| 11 | Asymmetric penalties, equal shares, every depth: closed form outside windows that shrink as kappa grows and vanish for kappa >= 2(m-1)/m; for kappa >= 2 always a two-piece formula | Proved; algebra verified symbolically | Theorem B |
| 12 | Inside the windows that remain for 1 < kappa < 2(m-1)/m (and in 3 of 204 arbitrary-share instances with 1 < kappa < 2) | Open: relaxation known, best laws found within 1.8e-3 of it | Section 6 of the notes |
| 13 | Asymmetric penalties, arbitrary shares, every depth: the two-producer formula applied to the best split of the free producers into two blocks is a lower bound for every kappa | Proved; algebra verified symbolically | Theorem C |
| 14 | Conjecture C: for kappa >= 2 that lower bound is the exact worst case | **Refuted.** Exact counterexample at kappa = 10 (an explicit law reaches 0.2664, the best two-block law 0.2496); failures are rare in random samples (2 of 200 with one small share, 0 of 299 otherwise) | [conjecture_c.md](results/asymmetric/conjecture_c.md) |
| 18 | Gaussian demand with nonnegative correlations: the overstatement is at most a_1(1 - sqrt(1 - h)), independent of r; for equal shares (1/n)(1 - sqrt(1 - H_m)), i.e. 0.061, 0.079, 0.086, 0.090, 0.093 at depth one for n = 3..7, attained for r <= 1/sqrt(2n-1) | Proved; algebra verified symbolically; 9 of 9 configurations match the SDP computation | Theorem G, [notes](docs/gaussian_envelopes.md), Section 8 of the paper |
| 19 | Gaussian demand, any correlations: as bad as all laws at small r (0.675 for n = 4, r = 0.1) but far below as r grows (0.116 against 0.375 at r = 0.5); on the wind panels the Gaussian worst case is 1/6 to 1/2 of the general one, 0.08 against 0.41 for the distant sites | Computed (SDP per membership, search over memberships); every law re-checked | [gaussian_envelopes.md](results/gaussian/gaussian_envelopes.md) |
| 17 | Two-sided audit: for every law with floor r, D_k - Gamma_k(w,r) <= B <= D_k, so a fractional audit reporting more than the worst-case overstatement proves that an actual coalition gains | Proved (corollary of the definitions) | Corollary 2 of the paper |
| 16 | On real hourly wind production (three panels of four producers, 24 audits) the observed overstatement is at most 0.0013 of the pooled cost, while the worst case for the same shares and floor ranges from 0.005 to 0.41 | Computed exactly on the empirical laws | [wind_audit.md](results/illustration/wind_audit.md), Section 8 of the paper |
| 15 | Ceiling criterion, for every kappa (symmetric case included): the elementary ceiling is exact whenever a subset of a largest face has share in [(1-r)/(1+kappa), kappa(1-r)/(r+kappa)] a(F), in particular when every producer is small enough | Proved; algebra verified symbolically | Proposition D |

In plain terms: with four producers each paying at least a quarter of their
standalone cost, the audit can still report a saving of 31/56, about 55%, of
the expected pooled cost while no coalition actually gains anything. With
generic shares the elementary ceiling (1-r)(n-k)/n turned out to be the exact
answer whenever r <= 0.4 in our samples, and never when r >= 0.7. If a
shortfall costs twice as much as a surplus, the four-producer figure rises
from 31/56 to 9/16 = 56.25%: asymmetric prices make the audit worse, not
better.

The figure [results/exclusion/exact_envelopes.png](results/exclusion/exact_envelopes.png)
shows the exact curves for 4, 5, 6 and 8 producers against the elementary
ceiling.

## How the results are checked

1. **Exact arithmetic on the constructions.** Every explicit law is checked
   with rational arithmetic on every coalition constraint: 1910 equal-share
   and 600 last-depth constructions, 324 window ratios and 1068 random
   arbitrary-share instances (all saved under `results/exclusion/`); for
   asymmetric penalties 300 last-depth and 5565 equal-share constructions,
   1605 of them also as explicit laws evaluated directly under the
   asymmetric loss, and 600 random arbitrary-share instances at intermediate
   depths (`results/asymmetric/`).
2. **Symbolic verification of the proofs.** The algebra of every proof
   (identities, corner values of the stability checks, dual weights, sign
   factorizations) is checked with sympy for general sizes: **212 of 212
   checks pass** ([report](results/verification/symbolic_checks.md)).
3. **Independent evaluation.** Samples of the explicit laws are re-evaluated
   with the project's original audit code, which computes the relaxation and
   the coalition excesses from scratch.
4. **Upper bounds by linear programming.** A certificate LP, valid for every
   demand law, matches the explicit laws in every instance computed, except
   inside the asymmetric windows of result 12.

What this does not replace: the reading of the proofs by an expert. The
convex-analysis lemmas are short arguments that are not machine-checked, and
the conjecture for arbitrary shares is supported by computation, not proved.

## Next steps

### Done (5 to 7 November)

- [x] **Symbolic verification of all proof algebra**: now 212 checks, all
      passing. It also turned "the window value is the larger of the two
      families" into an identity, V_p - H_{p+1} = a(m+p+1)(r - r_L)Q(r)/(2rD).
- [x] **Asymmetric imbalance penalties**: results 9 to 15
      ([notes](docs/asymmetric_penalties.md)). The results survive and get
      stronger; Conjecture C was refuted by an exact counterexample, and the
      ceiling criterion came out of the attempt.
- [x] **Systematic literature review**
      ([literature_review.md](docs/literature_review.md)): 25 logged queries,
      30 verified references, novelty assessed contribution by
      contribution. No prior work bounds the overstatement of a fractional
      audit.
- [x] **Illustration on real data**: result 16. On real wind production the
      audit was essentially exact, so the bounds are guarantees, not
      predictions.
- [x] **Full re-reading of the draft** (now 12 pages): two passages
      corrected (a misattributed certificate in the proof of the last-depth
      theorem, a notation clash), discussion updated, every number checked
      against the saved results; a
      [guide for the expert reading](docs/proof_guide.md) lists the seven
      steps that rest on reasoning alone.

### Before submission (needs a person)

- [ ] **Expert reading of the proofs**, starting from the
      [guide](docs/proof_guide.md): Lemmas 2 and 3, then Theorem 7, Theorems
      4 and 5, and Section 7.
- [ ] **Choice of venue and length.** At 12 pages the draft is too long
      for Operations Research Letters. Either a letter with the symmetric
      theory (Sections 2 to 6) and the rest in a supplement, or the full
      version for MMOR, TOP or IJGT.
- [ ] **Database search** (Scopus, Web of Science, MathSciNet) and full-text
      checks of the seven references seen only as abstracts.

### Research that would strengthen the paper (optional)

- [x] **Realistic laws: Gaussian demand** (done 7 November: results 18 and
      19). For positively correlated Gaussian producers the overstatement is
      bounded by an explicit constant, whatever r (about 9% of the pooled
      cost for up to seven equal producers), and the bound is attained. This
      explains most of the distance between the worst case and the wind data.
      Open: arbitrary shares beyond the closed form, elliptical laws, and a
      certified outer search for correlations of any sign.

- [ ] **Prove Conjecture 6** (the upper bound for arbitrary shares with
      symmetric penalties), along the lines of the equal-share proof. First
      step done: for three free producers the optimum of the certificate LP
      uses at most three certificates of the window-proof types, with one
      fixed pattern per family ([active_certificates.md](results/exclusion/active_certificates.md)),
      so a dual-weight proof regime by regime looks feasible. Second step
      done: in the transitional regime the three active certificates have
      explicit dual weights, which prove the upper bound V there (lemma in
      [exact_envelopes.md](docs/exact_envelopes.md), symbolic group N). Still
      needed: the other regimes and a proof that the regions cover all cases.
- [ ] **The open asymmetric regions**: the remaining equal-share windows for
      1 < kappa < 2(m-1)/m and transitional laws for arbitrary shares
      (counterexample value between 0.2664 and 0.2787). The likely tool is an
      inequality satisfied by all pinball costs (sections of lift zonoids)
      beyond quasi-symmetry. Hlawka's inequality, the obvious candidate, is
      ruled out: general laws violate it ([hlawka.md](results/asymmetric/hlawka.md)).

## Publication outlook

The equal-share theory and the last-depth theorem form a complete, proved
core with a non-obvious structure (intervals, windows, a switching
quadratic), which seems sufficient for a short paper in a journal such as
Operations Research Letters, TOP, Mathematical Methods of Operations Research
or the International Journal of Game Theory. The extension to asymmetric
penalties answers the most likely referee objection and adds a second
non-obvious structure (windows that close at kappa = 2(m-1)/m), together
with a criterion for when the elementary ceiling is exact (Proposition D).
A proof of either conjecture and a data illustration would strengthen the
paper further.
Before submission: the expert reading of the proofs, the literature review,
and a check of the chosen journal's policies.

## Timeline

| Date | Milestone |
| --- | --- |
| 5 Nov | First draft: trivial bound shown to be tight; judged too thin |
| 6 Nov | Three-producer case with the standalone ratio (C39) |
| 6 Nov | Computational map of the worst case; explicit laws found by linear programming |
| 6 Nov | Theorems 1 and 2: equal shares outside the windows, arbitrary shares at the last depth |
| 6 Nov | Theorem 4: the windows; closed form for equal shares |
| 6 Nov | Four families and the conjecture for arbitrary shares; first paper draft |
| 7 Nov | Symbolic verification of all proof algebra (134 checks) |
| 7 Nov | Asymmetric penalties: Theorems A and B, windows close for kappa >= 2(m-1)/m (175 symbolic checks) |
| 7 Nov | Asymmetric penalties, arbitrary shares: Theorem C and Conjecture C (299 of 299 for kappa >= 2; 194 symbolic checks) |
| 7 Nov | Proof attempt for Conjecture C: counterexample found and verified exactly; ceiling criterion proved (Proposition D; 200 symbolic checks) |
| 7 Nov | Systematic literature review; bibliography corrected and extended to 30 entries |
| 7 Nov | Guide for the expert reading; illustration on real wind data (24 exact audits) |
| 7 Nov | Two-sided audit corollary; Gaussian demand: Theorem G (bound independent of r) |

## Reproducing everything

```bash
python -m pip install -r requirements.txt -r requirements-verify.txt
python -m pip install --no-deps -e .
python -m unittest discover -s tests
python scripts/verify_symbolic.py
python scripts/check_asymmetric_penalties.py
python scripts/check_asymmetric_general.py
python scripts/probe_general_laws.py
python scripts/refute_conjecture_c.py
python scripts/illustrate_wind_audit.py   # downloads about 180 MB of public data
```

The other scripts are listed in [PULP_FICTION.md](PULP_FICTION.md); each
writes its outcomes to JSON under `results/` before generating a summary.
