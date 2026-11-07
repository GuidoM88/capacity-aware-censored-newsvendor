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
   factorizations) is checked with sympy for general sizes: **200 of 200
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

- [x] **Symbolic verification of all proof algebra** (done 7 November: 134
      checks; it also turned the claim "the window value is the larger of the
      two families" into an identity, V_p - H_{p+1} = a(m+p+1)(r - r_L)Q(r)/(2rD)).
- [x] **Asymmetric imbalance penalties** (done 7 November: results 9 to 12;
      [notes](docs/asymmetric_penalties.md), [checks](results/asymmetric/asymmetric_checks.md)).
      The results survive and get stronger; one narrow region is left open.
- [x] **Asymmetric penalties with arbitrary shares at intermediate depths**
      (done 7 November: results 13 and 14,
      [checks](results/asymmetric/general_shares.md)). The three families of
      Theorem 5 extend to every kappa. For kappa >= 2 the transitional family
      is never needed in our sample.
- [x] **Attempted proof of Conjecture C** (7 November). The conjecture is
      false. The attempt produced an exact counterexample (result 14) and
      the ceiling criterion (result 15).
- [ ] **Transitional laws for arbitrary shares under asymmetric penalties**:
      an explicit family playing the role of V for every kappa, and the
      exact worst case of the counterexample (between 0.2664 and 0.2787).
- [ ] **The remaining asymmetric windows** (1 < kappa < 2(m-1)/m): find an
      asymmetric analogue of the family V_p, or laws outside the segment class.
- [x] **Systematic literature review** (done 7 November:
      [literature_review.md](docs/literature_review.md)). 25 web queries,
      30 verified references. No prior work bounds the overstatement of a
      fractional audit; the closest are the relaxation itself (Burer and
      Dror 2005), fuzzy-game results on when fuzzy and crisp cores coincide,
      and the NP-hardness of core membership (Chen and Zhang 2009). The zonoid
      identity is classical and credited. Still open: a database search
      (Scopus, Web of Science) and full-text checks of seven items seen only
      as abstracts.
- [ ] **Revise the paper draft** ([paper_exact/main.pdf](paper_exact/main.pdf),
      now 11 pages) and have the proofs read by an expert. Prepared on
      7 November: a [guide for the expert reading](docs/proof_guide.md) (which
      half of each proof comes from where, what is machine-checked, and the
      seven steps that rest on reasoning alone); the formal statements were
      re-read for consistency. At 11 pages the draft is too long for
      Operations Research Letters; MMOR, TOP or IJGT fit as it is.
- [ ] **Prove Conjecture 6** (the upper bound for arbitrary shares), along the
      lines of the equal-share proof.
- [ ] **Illustration on real data**: compare the worst case with the gaps
      observed on the project's wind production series.

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
```

The other scripts are listed in [PULP_FICTION.md](PULP_FICTION.md); each
writes its outcomes to JSON under `results/` before generating a summary.
