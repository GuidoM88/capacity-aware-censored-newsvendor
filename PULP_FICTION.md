# pulp-fiction

This branch follows one question to the end: how badly can the fractional
coalition audit overstate savings once every producer is known to pay at
least a fraction r of its standalone cost? C39 answered it for three
producers with equal shares. Here we try to answer it in general.

The branch starts from `main` at `309977c` and only adds files, so merging
is mechanical. Work on `main` went on in parallel; keeping the two apart made
it easy to compare them before deciding what goes into the paper.

## Where things stand

* **Equal shares, any number of producers, any depth, any r: solved in
  closed form** ([Theorems 1 and 4](docs/exact_envelopes.md)). With
  m = n-k free producers at depth k, the elementary C31 ceiling (1-r)m/n is
  exact on a union of intervals; above (m-1)/(m+1) the value is
  (m-1)(1-r^2)/(2nr); in the "windows" between the intervals it is the larger
  of two explicit families, and a quadratic in r says which. Every value comes
  with an explicit finite demand law.
* **Arbitrary shares at the last nonterminal depth n-2: settled for every r**
  ([Theorem 2](docs/exact_envelopes.md)). For three producers this extends
  C39 to unequal shares. The C39 argument by itself is not sharp there: at
  w = (3/5, 1/4, 3/20) and r = 1/5 it gives 0.68, while the true worst gap is
  17/28 = 0.607.
* **Arbitrary shares, any depth: a two-LP method that determines the worst
  gap in every instance tried.** A certificate LP bounds every demand law; an
  LP over finite symmetric laws produces a law that meets it. On 68 random
  instances with up to six producers the bound equals the exact relaxation,
  and in all 38 where a law was built the law reaches it (Section 9 of the
  log). Before that, the laws had matched the relaxation in 29 of 29 cases,
  17 of them outside every theorem (Section 7).
* **Negative results kept on record.** Charging in proportion to standalone
  costs does not tame the gap beyond three producers. The windows are not a
  thin sliver: they cover 13 to 20 percent of the range of r for 4 to 30
  producers.
* **Open.** A closed form for unequal shares at depths 1 to n-3; a proof
  that the seminorm relaxation is always attained by a demand law; asymmetric
  imbalance penalties.

## How to read the branch

Start with [docs/exact_envelopes.md](docs/exact_envelopes.md): statements and
complete proofs of the theorems. [docs/paper_plan.md](docs/paper_plan.md)
proposes how to rebuild the manuscript around them. [docs/seminorm_envelope.md](docs/seminorm_envelope.md)
explains the oracle, the upper bounds and the numerical map that led there.
The `results/exclusion/*.md` files are generated from saved JSON by the
scripts listed at the end and should not be edited by hand.

```bash
python -m pip install -r requirements.txt
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
python scripts/check_exact_envelopes.py
python scripts/check_window_envelopes.py
python scripts/check_certificate_method.py
python scripts/summarize_c31_exactness.py
python scripts/plot_exact_envelopes.py
python scripts/check_strict_mixtures.py
python scripts/check_seminorm_envelope.py
python scripts/check_zonotope_realizability.py
python scripts/check_proportional_envelope.py
python scripts/check_realizability_conjecture.py
```

The first two scripts take under a minute each; the seminorm map and the
proportional map about eight minutes on four cores; the conjecture test about
fifteen.

## Log

### 1. Reading the November 5 draft

The proofs in the draft hold up: Lemma 1, Proposition 2, Theorem 3,
Proposition 4, Corollary 6, the example after Proposition 7 and
Proposition 8 all check out. One small gap in the statement of Theorem 3:
it should say that alpha and beta are fixed. With two equiprobable states
the cost is min(alpha, beta)|d'z|/2, so the supremum holds for every fixed
pair.

The weakness is significance, not correctness. The upper bound of the main
theorem is one line from nonnegative cost, and the matching family reuses
the two-state device of Chen and Zhang (2009). Along that family L goes to
zero, and measured against the cooperative surplus sum_j c_j - c(N) (which
is H-1 in unscaled units) the gap stays below 1/(2(2n-3)) and tends to
zero. The relaxation itself appears only in a section of the 2005
Burer-Dror manuscript that the journal version dropped, so the audience is
narrow. On presentation: the tone is defensive, the statistical comparison
of Section 6, Table 2 and Appendix B belong in a companion note, and the
draft never names its application, renewable producers pooling imbalance
penalties.

References worth adding, beyond the four already in `docs/feedback_review.md`:
Baeyens, Bitar, Khargonekar and Poolla, *Coalitional aggregation of wind
power*, IEEE Trans. Power Systems 28(4), 2013; Chakraborty, Baeyens and
Khargonekar, *Cost causation based allocations of costs for market
integration of renewable energy*, IEEE Trans. Power Systems 33(1), 2018;
Montrucchio, Norde, Ozen, Scarsini and Slikker, *Cooperative newsvendor
games: a review*, in Handbook of Newsvendor Problems, 2012; Caprara and
Letchford, *New techniques for cost sharing in combinatorial optimization
games*, Math. Programming 124, 2010.

The conclusion was that the draft needs a stronger central result before it
is worth submitting anywhere demanding.

### 2. Why the standalone ratio and not L/A

Two ways of escaping the vanishing-L problem were on the table: fix L/A, or
parametrize by the standalone ratio rho. We chose rho. A depends on declared
capacities, which can be inflated without changing anything in the economic
problem, whereas rho is a property of the game. With charges proportional to
standalone costs and an optimal grand offer, rho is exactly the pooling ratio
c(N)/sum_j c_j.

### 3. Mapping before proving

C39 was proved by hand for one case. Before trying to generalize by hand we
wanted to see what the answer looks like. Under symmetric absolute loss the
optimized cost is a seminorm, and for a fixed membership the smallest
seminorm compatible with the game's constraints can be computed by small LPs
(gauge duality, Lemma 1 of the seminorm note). Maximizing over memberships
gives an upper bound on the worst gap for any n, shares and r.

What the map showed:

* it reproduces C39 at ten ratios and C30 at r = 0, which validated the tool;
* for three producers with unequal shares the C39 argument is loose in 7 of
  24 cases; adding the standalone cap of the integral producer as a fourth
  inequality closes the gap in all 24;
* for four and five producers with equal shares the bound sits strictly below
  C31 on windows of r, and equals it elsewhere below (n-2)/n. A simple
  heuristic in terms of "p unit and q fractional producers" predicted the
  five-producer window from the four-producer one.

### 4. Do real demand laws reach these values?

A relaxation can be loose, so the map alone proves nothing about demand
laws. The useful observation is that a finite centrally symmetric law has
cost c(x) = sum_k p_k |x_k'x|, a zonotope support function. Once the signs
of the generators on the finite set of test vectors are fixed, searching
these laws is a single LP. Each solution was turned into an explicit law on
the unit box and re-evaluated with the original audit code.

All 12 values tested were attained (6 to 14 atoms, zero integer excess,
rho = r up to a solver tolerance of 1e-6). In 8 of them the value equals a
proved upper bound, so it is the exact worst gap at that ratio. This
suggested the conjecture that the seminorm relaxation is always attained by
symmetric laws.

### 5. A dead end: proportional charges

For three producers with equal shares and equal standalone costs, charging in
proportion to standalone costs looked attractive: the worst gap vanishes when
pooling is strong (rho below 0.1547), peaks at 4/15 of L at rho = 1/5, and
is half the C31 ceiling above that. It does not survive at four producers.
There the relaxed gap is about 0.5 + rho for small rho, and an explicit law
attains 0.54 at rho = 0.04: with that much pooling the audit can still report
a saving of 54 percent of L although no coalition gains anything. With five
producers the gap equals C31 at five of nine sampled ratios. We dropped
this line.

### 6. From examples to theorems

The laws returned by the LP had a recognizable shape: one generator per
fractional producer, vanishing at the witness membership, plus one generator
per excluded producer. Writing that shape down with free parameters and
asking which constraints must be tight gave two families.

For equal shares the necessary conditions behind the heuristic of Section 3
turned out to be sufficient. On the configuration with p unit and q
fractional producers, all coalition constraints reduce to a bilinear
function of two counts, whose minimum sits at one of four corners. This
gives C31 exactly on the intervals
[max(0, (q-p)/(q+p)), q/(q+2p)], and a second family gives the exact value
above (m-1)/(m+1). Nothing in the argument uses k = 1, so it covers every
depth (Theorem 1).

For arbitrary shares at the last depth, the same idea with two free
producers gives three regimes per ordered pair, one for each way the lower
envelope of the four lines can peak (Theorem 2).

Checks: 1910 equal-share constructions (n = 3 to 10, all depths) and 600
random rational instances of Theorem 2 pass an exact rational check of every
constraint, and 111 of the laws reproduce their value in the original audit
code.

One earlier guess had to be corrected here. We had expected the windows to
become negligible as n grows. They shrink only like n^(-1/2): their total
length is 0.13 for n = 4, close to 0.2 around n = 10, still 0.16 at n = 30.
So the window values are a real part of the answer, not a footnote.

### 7. Testing the realizability conjecture

The theorems only use the explicit families, so they say nothing about
whether the relaxation is attained elsewhere. We therefore picked 17 cases
that no theorem covers: four producers with random unequal shares at depth
one, the four- and five-producer equal-share windows, and five producers at
depth two with equal and unequal shares. For each, the relaxation was
maximized, the zonotope LP was solved at the maximizer (with sparse matrices,
since five producers already give about 7200 sign chambers), and the
resulting law was re-evaluated with the original audit code.

All 17 were attained, by laws with 6 to 26 atoms. Together with the 12 cases
of Section 4 that makes 29 out of 29. This is evidence, not a proof; but it
means that, in everything we have computed, the worst case over demand laws
and the worst case over seminorms coincide, and the second is a finite LP.
Details: [results/exclusion/realizability_conjecture.md](results/exclusion/realizability_conjecture.md).

### 8. Inside the windows

Since the windows are not negligible, we went after them next. Two things
turned out to be enough to pin them down numerically and, in the smallest
case, to prove the answer.

First, two more families of laws. One continues the C31 plateau of a
configuration beyond its interval by letting the witness carry positive cost
(family H_p; for p = 1 it is the high regime). The other has one producer in
transition between "unit" and "fractional" (family V_p). Both were read off
from LP solutions and then written in closed form; every constraint of both
has been checked in exact arithmetic at hundreds of ratios.

Second, an upper bound valid for every law: for a sorted witness, each
coalition of the s largest coordinates, scaled by one of the coordinates,
gives a triangle-inequality certificate that is linear on the sorted region.
The best bound from all of them is one LP. At all 324 window ratios tested
(n up to 12, depths 1 to 3) this bound equals the best explicit law, so the
worst gap is determined there.

For three free producers the LP collapses to three certificates whose
multipliers can be written down, and the window value
2(2 - r + 3r^2)/(n(1+3r)) is proved (Theorem 3). In plain terms: with four
producers and every producer paying at least a quarter of its standalone
cost, the audit can overstate the largest available saving by up to
31/56 = 55.4 percent of the expected cost, against 56.25 percent for the C31
ceiling.

What is not done: a general proof that the LP optimum is always the larger of
the two families inside each window, and a written algebraic check of the
transitional family for general sizes. Details:
[docs/exact_envelopes.md](docs/exact_envelopes.md), Section 5, and
[results/exclusion/window_envelopes.md](results/exclusion/window_envelopes.md).

### 9. Unequal shares: the same certificates, without symmetry

With unequal shares there is no sorting argument, but the certificates do not
need one: for a fixed face, a fixed producer carrying the largest coordinate
and a fixed order of the others, every certificate "coalition S scaled by one
coordinate" is linear, so each order gives one LP. Enumerating orders is
cheap up to six or seven producers.

We first checked the six four-producer cases of Section 7: the bound equals
the value of the law found there, to 1e-7. Then 68 new random instances
(four to six producers, depths 1 to 3): in every one the bound equals the
exact relaxation at the maximizer, and in all 38 where we also built a law
the law reaches it. The same LP reproduces Theorems 1 to 3 where they apply.
So, as far as we have looked, the worst gap with arbitrary shares is the
value of a finite LP, attained by an explicit finite law. What is missing is
a proof that this always happens.

Looking at which certificates are active gave a simple practical picture. In
45 of the 68 instances the exact worst gap is just the elementary C31
ceiling, and the dividing line is r: every instance with r <= 0.4 is at C31,
none with r >= 0.7 is, and there the exact value can be much lower (0.187
against 0.26 in one case). With generic shares, then, the elementary bound is
the right answer when producers pay a small or moderate part of their
standalone cost, and the exact theory matters when they pay most of it
([summary](results/exclusion/c31_exactness.md)).

The picture for equal shares is summarized in
[results/exclusion/exact_envelopes.png](results/exclusion/exact_envelopes.png):
the exact curve against the C31 ceiling for 4, 5, 6 and 8 producers, with the
windows shaded. It also makes plain that the improvements over C31 are real
but modest in size; the paper should say so.

### 10. Closing the windows

The certificate LP had told us the window values; we wanted a proof for all
sizes. Reading the LP duals at a few window ratios showed that only a handful
of certificates are ever active: nonnegative cost, the p+1 largest
coordinates, and the whole face scaled either by the transitional coordinate
or by one. They depend on the witness only through three sums (the p largest
coordinates, the transitional one, and the rest), so the whole problem
collapses to a three-variable LP whose duals can be written down.

In the transitional regime the weights are explicit, and the weight on
"nonnegative cost" is proportional to Q(r) = mr^2 + 2(p-1)r + 2 + 2p - m;
in the positive-cost regime the feasibility condition for the weights
rearranges to Q(r) <= 0. So the two regimes meet exactly where Q vanishes
(for seven producers at depth one, at r = 1/sqrt(3), where both families
equal 0.32991). On the construction side, the transitional law turned out to
have tidy parameters (gamma = M(p+1)(1-r)/(2p) and so on), every free
producer sits exactly at its standalone cap, and stability reduces to eight
corner checks, all nonnegative on the window.

That gives Theorem 4, and with Theorem 1 a closed form for equal shares at
every size, depth and ratio. Before writing it up we checked the switching
rule and the admissibility of the witnesses at 129,888 window ratios in exact
arithmetic (up to 301 producers) and the closed form against the explicit
laws at 9,360 ratios: no exceptions. The figure was regenerated from the
closed form; the plotted values did not change.

### 11. Removing the degeneracy

A referee could object that the worst-case laws are degenerate: some
coalitions are exactly indifferent and the covariance is singular. The C39
note had handled this for its own family by mixing in a small amount of a
well-behaved law. The same works for every law here, with one fixed
ingredient: a symmetric law whose atoms are scaled differences e_i - e_j plus
a small common component. It makes every proper coalition strictly stable on
its own and has positive definite covariance, and since costs of symmetric
laws mix linearly, a small dose of it carries both properties over to any
mixture. Taking the worst-case law at a slightly shifted ratio keeps the
standalone caps exact. The suprema are unchanged for every r < 1
(Proposition 5); they are approached rather than attained. Twelve mixed laws,
evaluated with the original audit code, behave as the proof says.

### What we would do next

1. Rewrite the paper along [docs/paper_plan.md](docs/paper_plan.md): the
   exact equal-share curve and Theorem 2 as the core, the two-LP method as
   the computational counterpart, the first draft's statistics moved to a
   companion note.
2. Look for structure in the unequal-share optimizers at depth one: which
   certificates are active, and whether a few regimes per producer pair, as
   in Theorem 2, describe them.
3. Check the literature on zonotopes and zonoids in cooperative games before
   claiming contributions 3 to 5 of the plan.

## Proposed claim-register rows

`docs/claims.md` is edited on `main`, so the rows are collected here and can
be numbered at merge time.

| ID | Statement | Evidence | Scientific status |
| --- | --- | --- | --- |
| PF1 | For a fixed membership, the smallest symmetric-loss seminorm cost compatible with the game constraints equals max_S min{abs(pi'z): pi in Pi_S}; the induced envelope bounds every demand law | Lemma 1 in seminorm_envelope.md; reproduces C39 at ten ratios and C30 at r=0 | Proved relaxation |
| PF2 | Equal shares: (D_k-B)/L <= (m-1)(1-r^2)/(2nr) for r >= (m-1)/(m+1), m = n-k | Proposition 2 of seminorm_envelope.md, any depth | Proved; exact by PF9 |
| PF4 | Three producers, positive shares: four-inequality bound; the C39 argument alone is not sharp for unequal shares | Proposition 3; loose in 7 of 24 mapped cases | Proved; exact by PF10; negative result preserved |
| PF5 | Proportional charges, three equal shares and equal standalone costs: worst relaxed gap zero for rho <= 0.1547, peak 4/15 at rho = 1/5, (1-rho)/3 above | Proposition 4; explicit laws at rho = 0.17 and 0.3 | Proved bound, exact at the realized ratios; does not extend (PF8) |
| PF7 | Every relaxed value tested so far is attained by an explicit finite symmetric law | seminorm_envelope.md Section 6 and the conjecture tests | Verified at the listed points up to 1e-6; general statement conjectural |
| PF8 | Proportional charges do not remove or halve the gap for n >= 4 | proportional_envelope.md | Negative result |
| PF9 | Theorem 1: equal shares, any n and depth k, exact worst gap on the intervals I_p and for r >= (m-1)/(m+1), with explicit laws | exact_envelopes.md; 1910 exact checks, independent re-evaluation | Proved |
| PF10 | Theorem 2: arbitrary positive shares at depth n-2, exact worst gap for every r, three regimes per ordered pair, explicit laws | exact_envelopes.md; 600 exact checks, independent re-evaluation | Proved |
| PF11 | For equal shares at depth one, the windows not covered by Theorem 1 have total length 0.13 to 0.20 for 4 <= n <= 30, decaying like n^(-1/2) | exact_envelopes.md, windows table | Exact computation of the intervals |
| PF12 | The seminorm relaxation was attained by an explicit finite symmetric law in 17 of 17 cases outside every theorem (n = 4, 5; depths 1, 2; equal and unequal shares) | realizability_conjecture.md | Evidence for the realizability conjecture; not a proof |
| PF13 | Families H_p and V_p of explicit laws inside the windows | exact_envelopes.md Section 5 | Proved (both families verified algebraically; exact checks at 441 + 324 ratios) |
| PF14 | A certificate LP bounds the equal-share worst gap for every law; it equals the best explicit law at all 324 tested window ratios | exact_envelopes.md Section 5; window_envelopes.md | Upper bound proved; equality now also follows from PF17 |
| PF15 | Theorem 3: for three free producers and 1/5 <= r <= 1/3 the worst gap is 2(2-r+3r^2)/(n(1+3r)); the four-producer depth-one curve is complete | exact_envelopes.md Section 5 | Proved |
| PF16 | For arbitrary shares, a certificate LP bounds the worst gap for every law; in 68 of 68 random instances (n = 4..6, depths 1..3) it equals the exact relaxation, and in 38 of 38 an explicit law reaches it | exact_envelopes.md Section 6; certificate_method.md | Upper bound proved; equality computational |
| PF18 | Proposition 5: for r < 1 the suprema of Theorems 1, 2 and 4 (and the values attained in the two-LP computations) are unchanged under strict stability and positive definite covariance | exact_envelopes.md Section 7; strict_mixtures.md (12 mixed laws) | Proved |
| PF17 | Theorem 4: inside each equal-share window the worst gap is V_p(r) if Q(r) >= 0 and H_{p+1}(r) if Q(r) <= 0, with explicit laws; with Theorem 1 the equal-share case is solved for every n, depth and r | exact_envelopes.md Section 5; window_envelopes.md; 129,888 exact window checks | Proved |

PF3 and PF6 of the earlier version (numerical windows, configuration
heuristic) are superseded by PF9 and PF11.

## Files

* `src/censored_newsvendor/exact_envelopes.py`: the explicit laws, closed forms, windows and exact verification.
* `src/censored_newsvendor/seminorm_envelope.py`: the seminorm oracle, the zonotope LP and the proved bounds.
* `src/censored_newsvendor/certificates.py`: the certificate LP for arbitrary shares and depths.
* `results/exclusion/exact_envelopes.png` (with the plotted values in `exact_envelopes_curve.csv`): the exact equal-share curves.
* `docs/exact_envelopes.md`: Theorems 1 and 2 with proofs.
* `docs/seminorm_envelope.md`: the oracle, upper bounds, numerical map and realizability check.
* `docs/paper_plan.md`: proposed structure, abstract and contributions for the revised paper.
* `scripts/check_*envelope*.py` (including `check_window_envelopes.py`), `scripts/check_zonotope_realizability.py`, `scripts/check_realizability_conjecture.py`: generators of the summaries in `results/exclusion/`.
* `tests/test_exact_envelopes.py`, `tests/test_seminorm_envelope.py`, `tests/test_certificates.py`: fast tests.

## Merging

```bash
git fetch origin
git checkout main
git merge origin/pulp-fiction
```

Then number the claim rows above and, if wanted, link the two notes from
the README.
