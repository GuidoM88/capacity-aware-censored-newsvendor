# Guide for reading the proofs

November 7, 2026, branch `pulp-fiction`. For an expert reading
`paper_exact/main.pdf`, or the notes it summarizes. Every proof has the same
two halves: an **upper bound**, valid for every demand law, from
certificates (or from the elementary ceiling), and a **lower bound** from an
explicit finite law. The table says where each half comes from, what has
been checked by machine, and which steps rest on reasoning alone. Those
steps are the ones worth reading most carefully.

Machine checks: symbolic identities and sign factorizations in
`scripts/verify_symbolic.py` (groups A to M, 200 checks,
[report](../results/verification/symbolic_checks.md)); exact rational checks
of the constructions on every coalition (`results/exclusion/`,
`results/asymmetric/`); independent numerical LPs (certificate LP, exact
relaxation, explicit-law LP).

Numbering below is the paper's (one counter for all statements), with the
number used in the notes in brackets: Proposition 1 (ceilings), Lemma 2
(laws from generators), Lemma 3 (triangle certificates), Theorem 4 (equal
shares; notes Theorem 1), Theorem 5 (windows; notes Theorem 4), Corollary 6
(closed form; includes notes Theorem 3), Theorem 7 (last depth; notes
Theorem 2), Theorem 8 (families; notes Theorem 5), Conjecture 9 (notes
Conjecture 6), Proposition 10 (strict stability; notes Proposition 5),
Lemma 11 to Corollary 13 (asymmetric model), Theorem 14 (notes Theorem A),
Theorem 15 (notes Theorem B), the two-block bound (eq. blocks; notes
Theorem C), Proposition 16 (notes Proposition D).

## Steps that are not machine-checked

1. **Reduction to one face and one unit coordinate.** The excess is
   positively homogeneous, so a maximizer with positive excess can be scaled
   until its largest free coordinate is one (end of Section 3).
2. **Triangle certificates** (Lemma 3, and its asymmetric form in Section 7):
   subadditivity, the caps c(e_i) <= a_i/r and, for asymmetric loss,
   c(-e_i) <= kappa c(e_i). Short, but every upper bound depends on them.
3. **Laws from generators** (Lemma 2) and **three-point mixtures**
   (Proposition 12): the claim that the components share an optimal offer.
   For symmetric laws this is symmetry about the centre; for the three-point
   components it is the quantile condition P(V<0) <= tau, P(V>0) <= tau for
   tau <= 1/2.
4. **Gauge duality** (seminorm notes, Lemma 1, and its asymmetric version):
   used only by the numerical oracle, not by any theorem of the paper.
5. **Bilinearity arguments.** In every equal-share and two-block
   construction the stability slack of a coalition depends on two numbers
   only (how many units, or which share of the units, and which fractional
   share), and it is bilinear in them. The symbolic checks verify the
   bilinearity and the corner values. That the slack depends on those two
   numbers only must be read off the construction.
6. **Max-min computations by hand.** Theorems 7 and 14: the maximum over t of
   the minimum of four linear functions of t. Each regime boundary is a
   checked factorization, but the case split itself is reasoning.
7. **Theorem 5 (windows), upper bound.** Dual weights of a small LP on the
   sorted region. The weights and their feasibility are checked
   symbolically; that this LP is the right one (the certificates used, and
   that the sorted region is a simplex whose vertices are the top-set
   indicators) is reasoning.

## Result by result

| Result | Upper bound | Lower bound | Machine checks | Read carefully |
| --- | --- | --- | --- | --- |
| Proposition 1 (ceilings) | c >= 0; subadditivity along 1_F - z | two-state laws (r = 0) | group A | the weighted-average step |
| Theorem 4 (equal shares, intervals and high regime) | ceiling; separable bound (two certificates) | ceiling law on I_p; law H_1 | groups B, C, D; 1910 exact constructions | steps 1, 2, 5 |
| Theorem 5 (windows) | dual weights in two regimes, sign of Q(r) | families V_p and H_{p+1} | group E (incl. t_2 >= 0 by coefficient positivity); 324 window ratios | step 7 |
| Corollary 6 (closed form, four producers) | Theorems 4 and 5 | the same laws | group F for the three-producer window | sign checks of the absolute values |
| Theorem 7 (last depth, any shares) | four certificates, max-min over t | three single-generator laws | group G; 600 exact constructions | step 6 |
| Theorem 8 (families, any shares) | none (lower bound only) | families C31, H, G | group H; 1068 instances exact | step 5 |
| Conjecture 9 | certificate LP, numerically | four families | 1068 of 1068 instances | not a theorem |
| Proposition 10 (strict stability) | not needed | mixture with a strictly stable law | group I; 12 mixed laws | continuity in r |
| Lemma 11, Proposition 12, Corollary 13 (asymmetric model) | Corollary 13(a): as Proposition 1 | three-point mixtures | group K | step 3 |
| Theorem 14 (last depth, any kappa) | four asymmetric certificates | three segment laws | group K; 300 instances with explicit laws | steps 2, 6 |
| Theorem 15 (equal shares, any kappa) | two certificates and the ceiling | ceiling law on I_p^kappa, law H_p^kappa | group K; 5565 constructions, 1305 laws | step 5 and the window algebra |
| Two-block bound (eq. blocks) | none | three two-block families | group L; 600 laws | step 5 |
| Proposition 16 (ceiling criterion) | ceiling | the two-block bound | group M | the partial-sum argument |
| Conjecture C (notes only) | none | none | refuted by an exact counterexample | not a theorem |

## Suggested order

Lemmas 2 and 3 first (they carry everything), then Theorem 7 (the shortest
complete proof), then Theorem 4, Theorem 5 and Section 7. Corollary 6 follows
from Theorems 4 and 5 and can be skipped on a first reading.
