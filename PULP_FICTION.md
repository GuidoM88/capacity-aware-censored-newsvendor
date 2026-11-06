# Branch `pulp-fiction`: handoff note

November 6, 2026. Work done by Claude (Claude Code) in a separate session,
in parallel with the work on `main`. The branch starts from `main` at
`309977c`. **No existing file is modified**; everything here is a new file,
so merging should not conflict with parallel work on `main`.

## 1. What was done, in order

1. Read the repository and the November 5 first-draft PDF (`paper/main.pdf`,
   identical to the copy in the repository).
2. Reviewed the draft for correctness, originality and presentation
   (Section 2 below).
3. Re-ran the existing checks at `309977c`. `scripts/check_three_player_rho.py`
   passes: 9 attaining, 10 strict and 8 off-family cases, 81 primal/dual
   and 27 MILP checks. The 40 unit tests pass after the README's editable
   install (`python -m pip install --no-deps -e .`). An earlier remark that
   the validation command in `AGENTS.md` fails was wrong: it failed only
   because the package was not installed in a fresh container.
4. Built a computational oracle for the structural envelope and mapped it
   (Section 3), with proofs of the bounds it is compared against.
5. Gave a recommendation for the next research step (Section 4).

## 2. Review of the first draft (summary)

The opinions here are a model review, not a guarantee of how referees will
judge the work.

* **Correctness.** Lemma 1, Proposition 2, Theorem 3, Proposition 4,
  Corollary 6, the example after Proposition 7, and Proposition 8 check out.
  Minor point: Theorem 3 should say that alpha and beta are fixed; with two
  equiprobable states the cost is min(alpha,beta)|d'z|/2, so the supremum
  holds for every fixed pair.
* **Why the draft is thin as a paper.** The upper bound follows in one line
  from nonnegative cost, and the matching family uses the two-state device
  of Chen and Zhang (2009). The extremal family has L tending to zero. Measured
  against the cooperative surplus sum_j c_j - c(N), which equals H-1 in
  unscaled units, its gap is below 1/(2(2n-3)) and tends to zero along the
  sequence that attains the supremum. The closest precedent of the
  relaxation is a section of the 2005 Burer-Dror manuscript that the journal
  version dropped, so its audience is narrow.
* **Presentation.** The tone is defensive; Section 6's statistical comparison,
  Table 2 and Appendix B do not belong in a theory note; `main.tex` never
  names the application (aggregated renewable producers with imbalance
  penalties).
* **Suggested improvements.** A stronger central theorem in a structural
  parameter (this branch explores which one); an introduction built on the
  application; references to add beyond the four already recorded in
  `docs/feedback_review.md`: Baeyens, Bitar, Khargonekar and Poolla (2013),
  *Coalitional aggregation of wind power*, IEEE Trans. Power Systems 28(4);
  Chakraborty, Baeyens and Khargonekar (2018), *Cost causation based
  allocations of costs for market integration of renewable energy*, IEEE
  Trans. Power Systems 33(1); Montrucchio, Norde, Ozen, Scarsini and Slikker
  (2012), *Cooperative newsvendor games: a review*, Handbook of Newsvendor
  Problems; Caprara and Letchford (2010), *New techniques for cost sharing
  in combinatorial optimization games*, Math. Programming 124. Also: move the
  statistics to a companion note, write explicit contribution and limitation
  paragraphs, promote Section 4.2 (physical versus canonical extension),
  and publish the paper's code separately from the censored-demand history.
* **Verdict.** In its November 5 form, not yet sufficient for a strong
  journal; a short note would need a stronger central result.

## 3. New on this branch

Full statements, proofs and scope: [docs/seminorm_envelope.md](docs/seminorm_envelope.md).
Saved map: [results/exclusion/seminorm_envelope.md](results/exclusion/seminorm_envelope.md).

* **Lemma 1 (gauge duality).** For a fixed membership, the smallest cost
  over all symmetric-loss seminorms obeying the depth-one game constraints
  is a max-min of small LPs. This gives an upper bound on the worst gap over
  demand laws. It reproduces C39 at ten ratios and C30's value at r=0.
* **Proposition 2.** Equal shares, any n: the C39 argument generalizes to a
  bound U_n(r) that equals the C31 ceiling for r<=(n-2)/n.
* **Numerical windows.** For n=4 and n=5 the relaxation is strictly below
  C31 in windows below (n-2)/n (5 of 16 cases), e.g. n=4, r=1/4: 0.553571
  against 0.5625. A configuration heuristic predicted the n=5 window from
  n=4. The windows are numerical observations, not certified.
* **Proposition 3 and a negative result.** For three players with unequal
  shares the C39 proof is not sharp (7 of 24 cases, e.g. 0.68 against
  0.607143). A fourth inequality, from the integral coordinate's standalone
  cap, gives a bound that the relaxation attains in all 24 cases.
* **Proposition 4 (proportional charges).** Three equal shares and equal
  standalone costs: the worst gap is zero for rho<=0.1547, peaks at 4/15 of
  L at rho=1/5, and equals (1-rho)/3, half of C31, above. The relaxation
  attains this bound at 13 of 13 ratios.

At the time of the first push, realizability by demand laws was not checked
for any new value; the update section below reports the later check.

## 4. Recommendation for the next step

* Do not switch to the fixed L/A question: A depends on declared capacities,
  whereas rho is intrinsic. With charges proportional to standalone costs
  and an optimal grand offer, rho equals the pooling ratio c(N)/sum_j c_j.
* Before proving the three-player unequal-share case by hand:
  1. test realizability of the relaxed values with finite centrally
     symmetric laws (cases listed in `docs/seminorm_envelope.md`);
  2. certify one window, for example n=4 and r=1/4;
  3. choose the central question. The proportional-charge envelope as a
     function of the pooling ratio is interpretable and non-monotone already
     at n=3; the rho-floor envelope with arbitrary charges risks reproducing
     C31 for larger n.

  Status after the update below: step 1 is done at 12 points (all realized).
  The proportional-charge suggestion in step 3 is withdrawn (negative
  result for n>=4).

## Update: realizability and proportional charges

Added after the first push, same day.

* **Realizability check.** Costs of finite centrally symmetric demand laws
  are zonotope support functions, and minimizing c(z) over them under the
  game constraints is one LP once sign chambers are fixed. Each solution was
  turned into an explicit law on the unit box and re-evaluated with the
  original `ExclusionEnvelope` and `coalition_table` code. **All 12 tested
  relaxed values are attained** (6 to 14 atoms, zero integer excess,
  rho=r, up to a normalized solver tolerance of 1e-6). In 8 cases the value
  equals a proved bound, so it is the **exact worst gap at that ratio**: for
  example 0.607143 for w=(0.6,0.25,0.15) at r=0.2, and the U_4 formula at
  r=0.6. Conjecture: the seminorm relaxation is always realizable for
  symmetric loss; tested only at these 12 points.
* **Negative result.** The proportional-charge shape at n=3 (zero gap under
  strong pooling, half of C31 above rho=1/5) does not persist. For n=4 the
  relaxed gap is 0.5+r for small r, and an explicit law attains 0.54 at
  rho=0.04. For n=5 it equals C31 at five of nine sampled ratios. This
  withdraws the earlier suggestion to center a paper on proportional charges.
* New files: `scripts/check_zonotope_realizability.py`,
  `scripts/check_proportional_envelope.py`, their results in
  `results/exclusion/`, Section 6 of `docs/seminorm_envelope.md`, and one
  realizability test.

## 5. Proposed claim-register rows

`docs/claims.md` is edited on `main` in parallel, so it is not modified
here. The rows below can be added when merging, with IDs assigned then.

| ID | Statement | Evidence | Scientific status |
| --- | --- | --- | --- |
| PF1 | For a fixed membership, the smallest symmetric-loss seminorm cost compatible with the depth-one game constraints equals max_S min{abs(pi'z): pi in Pi_S}; the induced envelope bounds every demand law | Lemma 1 in seminorm_envelope.md; reproduces C39 at ten ratios and C30 at r=0 | Proved relaxation; realizability not addressed |
| PF2 | Equal shares, n>=3: (D1-B)/L <= U_n(r), equal to C31 for r<=(n-2)/n and (n-2)(1-r^2)/(2nr) above | Proposition 2 | Proved upper bound; C39 for n=3; sharpness for n>=4 not established |
| PF3 | For n=4,5 the relaxed envelope lies strictly below C31 in windows below (n-2)/n | 5 of 16 saved cases, e.g. n=4, r=1/4: 0.553571 against 0.5625 | Numerical observation from grid search and refinement; not certified; realizability unchecked |
| PF4 | Three players, positive shares: four-inequality bound; the C39 three-inequality argument is not sharp for unequal shares | Proposition 3; attained by the relaxation in 24 of 24 cases and by explicit laws at w=(0.6,0.25,0.15), r=0.2 and w=(0.7,0.2,0.1), r=0.3; three-inequality bound loose in 7 | Proved bound, exact at the two realized points; preserved negative result; general attainment open |
| PF5 | Proportional charges, three equal shares and equal standalone costs: (D1-B)/L <= P(r), zero for r<=0.1547, peak 4/15 at r=1/5, (1-r)/3 above | Proposition 4; attained by the relaxation at 13 of 13 ratios and by explicit laws at r=0.17 and 0.3 | Proved upper bound, exact at the two realized ratios; does not extend to n>=4 (PF8) |
| PF6 | Configuration heuristic for the windows | Section 4; closed intervals agree with 16 of 16 saved labels; the first half-open version mislabeled one endpoint | Heuristic only |
| PF7 | Every relaxed value tested is attained by an explicit finite centrally symmetric law; eight of these values equal a proved bound and are therefore exact worst gaps at their ratios | Section 6 of seminorm_envelope.md; 12 of 12 cases re-evaluated with ExclusionEnvelope and coalition_table | Verified at 12 points up to tolerance 1e-6; general realizability is a conjecture |
| PF8 | Proportional charges do not remove or halve the gap for n>=4 | proportional_envelope.md: n=4 relaxed gap 0.5+r for small r, explicit law attaining 0.54 at rho=0.04; n=5 equals C31 at 5 of 9 sampled ratios | Negative result; withdraws the proportional-charge center |

## 6. Files on this branch

* `src/censored_newsvendor/seminorm_envelope.py`: oracle, closed-form bounds and heuristic.
* `tests/test_seminorm_envelope.py`: 8 fast tests.
* `scripts/check_seminorm_envelope.py`: 77-case map, about 7.5 minutes on 4 cores.
* `results/exclusion/seminorm_envelope.json` and `.md`: saved outcomes and the generated summary.
* `docs/seminorm_envelope.md`: statements, proofs, scope and next steps.
* `scripts/check_zonotope_realizability.py` and `scripts/check_proportional_envelope.py` with results in `results/exclusion/`: realizability and proportional checks (update section).
* `PULP_FICTION.md`: this note.

## 7. Merging

```bash
git fetch origin
git checkout main
git merge origin/pulp-fiction
```

Then assign claim IDs to the rows above and, if wanted, link this work from
the README.
