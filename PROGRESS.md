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

In plain terms: with four producers each paying at least a quarter of their
standalone cost, the audit can still report a saving of 31/56, about 55%, of
the expected pooled cost while no coalition actually gains anything. With
generic shares the elementary ceiling (1-r)(n-k)/n turned out to be the exact
answer whenever r <= 0.4 in our samples, and never when r >= 0.7.

The figure [results/exclusion/exact_envelopes.png](results/exclusion/exact_envelopes.png)
shows the exact curves for 4, 5, 6 and 8 producers against the elementary
ceiling.

## How the results are checked

1. **Exact arithmetic on the constructions.** Every explicit law is checked
   with rational arithmetic on every coalition constraint: 1910 equal-share
   and 600 last-depth constructions, 324 window ratios and 1068 random
   arbitrary-share instances (all saved under `results/exclusion/`).
2. **Symbolic verification of the proofs.** The algebra of every proof
   (identities, corner values of the stability checks, dual weights, sign
   factorizations) is checked with sympy for general sizes: **134 of 134
   checks pass** ([report](results/verification/symbolic_checks.md)).
3. **Independent evaluation.** Samples of the explicit laws are re-evaluated
   with the project's original audit code, which computes the relaxation and
   the coalition excesses from scratch.
4. **Upper bounds by linear programming.** A certificate LP, valid for every
   demand law, matches the explicit laws in every instance computed.

What this does not replace: the reading of the proofs by an expert. The
convex-analysis lemmas are short arguments that are not machine-checked, and
the conjecture for arbitrary shares is supported by computation, not proved.

## Next steps

- [x] **Symbolic verification of all proof algebra** (done 7 November: 134
      checks; it also turned the claim "the window value is the larger of the
      two families" into an identity, V_p - H_{p+1} = a(m+p+1)(r - r_L)Q(r)/(2rD)).
- [ ] **Asymmetric imbalance penalties.** Real markets usually price surplus
      and shortfall differently; all results so far assume equal penalties.
      Extend the results, or at least determine what changes. This is the
      first objection a referee would raise.
- [ ] **Systematic literature review** to confirm novelty, in particular risk
      capital allocation with homogeneous risk measures and relaxations of
      core membership. The zonoid identity used in the constructions is
      classical and is credited as such.
- [ ] **Revise the paper draft** ([paper_exact/main.pdf](paper_exact/main.pdf),
      8 pages) and have the proofs read by an expert.
- [ ] **Prove Conjecture 6** (the upper bound for arbitrary shares), along the
      lines of the equal-share proof.
- [ ] **Illustration on real data**: compare the worst case with the gaps
      observed on the project's wind production series.

## Publication outlook

The equal-share theory and the last-depth theorem form a complete, proved
core with a non-obvious structure (intervals, windows, a switching
quadratic), which seems sufficient for a short paper in a journal such as
Operations Research Letters, TOP, Mathematical Methods of Operations Research
or the International Journal of Game Theory. Asymmetric penalties, a proof of
the conjecture and a data illustration would strengthen it considerably.
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

## Reproducing everything

```bash
python -m pip install -r requirements.txt -r requirements-verify.txt
python -m pip install --no-deps -e .
python -m unittest discover -s tests
python scripts/verify_symbolic.py
```

The other scripts are listed in [PULP_FICTION.md](PULP_FICTION.md); each
writes its outcomes to JSON under `results/` before generating a summary.
