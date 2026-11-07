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
* **Arbitrary shares, any depth: a conjectured closed form that held in
  1068 of 1068 random instances.** The worst gap is the largest value of four
  explicit families of laws (Conjecture 6 in
  [docs/exact_envelopes.md](docs/exact_envelopes.md)); every value is attained
  by an explicit law, and the certificate LP matched it every time.
* **Asymmetric imbalance penalties: the results survive and get stronger**
  ([notes](docs/asymmetric_penalties.md)). The ceiling stays valid and every
  symmetric worst case stays attainable, so pricing a shortfall differently
  from a surplus can only increase the overstatement. The last depth is
  solved for every penalty ratio kappa (Theorem A); for equal shares the
  windows shrink and vanish once kappa >= 2(m-1)/m, which leaves a two-piece
  formula (Theorem B). For arbitrary shares the best split into two blocks
  gives a lower bound at every depth (Theorem C). We conjectured that for
  kappa >= 2 it is always the answer (Conjecture C). Trying to prove it
  produced an exact counterexample instead, and a proved criterion for when
  the ceiling is exact (Proposition D).
* **Literature: no prior bound found.** A systematic search
  ([literature_review.md](docs/literature_review.md)) found the relaxation
  itself, the NP-hardness of core membership and results on when fuzzy and
  crisp cores coincide, but nothing that bounds how much a fractional audit
  can overstate.
* **Real data: the bounds are guarantees, not predictions.** On hourly wind
  production (three panels, 24 exact audits) the observed overstatement is at
  most 0.0013 of the pooled cost, while the worst case for the same shares and
  floor reaches 0.41 for a diverse portfolio
  ([wind_audit.md](results/illustration/wind_audit.md)).
* **Open.** A proof of the upper bound for arbitrary shares (Conjecture 6);
  general conditions for one of the four families; a proof that the seminorm
  relaxation is always attained by a demand law; the asymmetric windows for
  1 < kappa < 2(m-1)/m, where the relaxation may not be attained at all;
  the exact worst case for arbitrary shares under asymmetric penalties,
  where transitional laws matter at every ratio.

## How to read the branch

For a one-page summary of the state of the project, see
[PROGRESS.md](PROGRESS.md). Then start with
[docs/exact_envelopes.md](docs/exact_envelopes.md): statements and complete
proofs of the theorems. [docs/paper_plan.md](docs/paper_plan.md)
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
python scripts/check_general_formula.py
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

### 12. A formula for arbitrary shares

The active certificates in the unequal-share instances pointed at the same two
mechanisms as in the equal-share case, now with shares instead of counts. Split
the free producers into units I and fractional producers J. The C31 value
(1-r)a(F) is reached when A_J(1-r)/(1+r) <= a(I) <= A_J(1-r)/(2r), the exact
analogue of the intervals I_p; and when a(I) >= A_J(1-r)/(2r) the positive-cost
law gives A_J(1-r^2)/(2r). Both constructions work for any shares once the
units' coefficients are proportional to their shares, and the stability check
again comes down to the corners of a bilinear function (Theorem 5).

The first attempt used a wrong condition for the second family (a slip in
the algebra, (1+r) instead of 2r in the denominator) and overshot badly; with
the right condition the larger of the two values equals the exact worst gap in
67 of the 68 random instances. The one exception looks like the transitional
case again, which for arbitrary shares has no formula yet. So for arbitrary
shares at every depth we now have a proved lower bound that is almost always
the answer, an LP that certifies the answer, and one missing family.

### 13. Four families for arbitrary shares

The transitional family carried over to arbitrary shares with the same
recipe (unit coefficients proportional to shares), and its formula reduces
to V_p for equal shares. With it, the families matched the exact worst gap in
all 68 earlier instances. A fresh run of 400 found five more exceptions, all
on faces with only two free producers; there the missing piece was the third
regime of Theorem 2, where the unit's cap binds. Writing that regime for any
number of producers gave a fourth family, whose stability check again has
four corners. A final run of 1000 new random instances, up to six producers
and every depth: all 1000 laws valid in exact arithmetic, all 1000 values
equal to the certificate bound. One of them, with a producer holding 21/29 of
the shares, was solved only by the new family.

So for arbitrary shares we now have a precise conjecture (Conjecture 6): the
worst gap is the largest value of four explicit families. Every value is
attained by a law, so what remains to prove is the upper bound. For equal
shares Theorem 4 did exactly that, which suggests the route.

### 14. A first draft of the new paper

With the results settled, we wrote an eight-page draft that follows the plan:
[paper_exact/main.pdf](paper_exact/main.pdf), source in `paper_exact/`. It
states the elementary ceilings, the two tools (laws from generators and
triangle certificates), the complete equal-share answer with the
four-producer curve, the last-depth theorem, the four families with the
conjecture and its evidence, and the mixture argument. Proofs are condensed
from the notes; the corner checks are stated with their values. It compiles
cleanly with pdflatex and bibtex. The original `paper/` folder is untouched.

### 15. Checking the proofs symbolically

Exact arithmetic at sample points tests the constructions, but a proof is
about all sizes at once. We therefore checked the algebra of every proof with
sympy (`scripts/verify_symbolic.py`): every identity (closed forms of the
generator coefficients, vanishing at the witness, tight caps, grand cost),
every corner value of the bilinear stability checks, the dual weights of
Theorem 4 in both regimes, and every inequality, each reduced to a
factorization whose sign is stated. The positivity needed for t_2 >= 0 is
checked by substituting the window bounds and verifying that all
coefficients of the resulting polynomial are nonnegative.

The first run found 7 failures out of 128, all in the checking script rather
than in the mathematics: a matrix compared with the scalar zero, a factor
(1+r) missing from one expected expression, and two absolute values removed
with the wrong sign in the three-producer plane law. After fixing them, and
adding explicit checks for the signs that had been implicit, all 134 checks
pass. One check turned out to be a small result of its own: V_p - H_{p+1}
factors as a(m+p+1)(r - r_L) Q(r) / (2rD), so the claim that the window value
is the larger of the two families is now an identity rather than an
observation. Some counts quoted earlier came from interactive runs that were
not saved; the notes now cite only saved results.

### 16. Asymmetric penalties

All results so far assumed that a surplus and a shortfall of the same size
cost the same. Real balancing markets rarely work that way, and it is the
first objection we would expect from a referee, so we redid the analysis
with a pinball loss whose two slopes differ by a factor kappa
([notes](docs/asymmetric_penalties.md)).

The first question was what survives without new work. The optimized cost
is still sublinear but no longer symmetric: c(-x) can be up to kappa times
c(x). Two things follow at once. The C31 ceiling survives, because its proof
only uses subadditivity along nonnegative differences. Every symmetric worst
case survives too: a mixture of three-point components, each having zero as
both a tau- and a (1-tau)-quantile, reproduces any sum of segments whose two
sides differ by at most a factor kappa, symmetric generators included. So
asymmetry can only make the audit's overstatement larger.

The real question was how much larger. The certificate argument carries over
with one change: lowering a coordinate is a shortfall direction and costs up
to kappa times the cap. With that, the last-depth computation behind
Theorem 2 can be redone by hand for every kappa. The three regimes survive,
with (1+r)/2 replaced by (r+kappa)/(1+kappa), and each has an explicit law;
two of them use the full ratio kappa on one segment (Theorem A). For equal
shares the same two certificates give the upper bound min{C31, H_1}, and the
symmetric ceiling and H_p laws generalize with the same bilinear-slack
argument (Theorem B). As kappa grows the ceiling intervals widen on both
sides and the windows close: the window between configurations p+1 and p is
nonempty iff kappa < (p+1)(m-p)/(pm), so all of them are gone by
kappa = 2(m-1)/m < 2. For practically relevant ratios the equal-share answer
is a two-piece formula.

Three things went wrong along the way, and they are worth keeping. Adding
kappa to the certificate LP first broke two old tests: a new variable reused
the name of the coalition weight inside the same loop. With the name fixed,
everything at kappa = 1 is unchanged. Then a first sweep showed one case
(five producers, depth one, kappa = 1.5, r = 0.4) where the certificate
bound was 0.48 but the law found at the certificate's maximizer reached only
0.467. This was not a counterexample. The exact relaxation is also 0.48, and
an explicit law reaches 0.47999994 at the relaxation's own maximizer; the
certificate LP had simply returned a maximizer that no law attains. Lesson:
when comparing bounds, try more than one maximizer. Finally, inside the
windows that survive for 1 < kappa < 2(m-1)/m the gap does not close. The
certificate bound equals the exact relaxation, but the best explicit law we
found stays 4e-4 to 1.3e-3 below it (nine cases, four producers). We record
this as open; Section 6 of the notes gives the two possible explanations.

Checks: 300 random last-depth instances and 5565 equal-share constructions
verified in exact arithmetic, 1605 explicit laws evaluated directly under
the asymmetric loss, 288 certificate cross-checks, and 41 new symbolic checks
(175 in total, all passing).

### 17. Arbitrary shares with asymmetric penalties

The next step after Theorems A and B was to go back to arbitrary shares at
intermediate depths, where even the symmetric case rests on a conjecture
(Conjecture 6). The three explicit families of Theorem 5 (C31, H and G)
share one structure: a block of units at 1, a block of fractional producers
at a common level t, one generator per fractional producer, and
coefficients proportional to the shares. With asymmetric penalties each
generator becomes a segment, and the cost of a coalition depends only on two
numbers: the fraction of the units' share it contains and the fractional
share it contains. The stability slack is bilinear in these two numbers, so
four corner coalitions decide everything, and they reduce to the conditions
of the last-depth regimes. The result is Theorem C: the two-producer formula
of Theorem A, applied to the best split into two blocks, is a lower bound at
every depth and for every ratio.

Whether it is also the answer we tested on 600 random instances against the
certificate bound ([summary](results/asymmetric/general_shares.md)). For
kappa >= 2 it matched in all 299 instances. For kappa = 1 the fourth,
transitional family of Conjecture 6 was needed in 8 of 97 instances, as
expected. For 1 < kappa < 2, three instances out of 204 stayed open, with
differences of at most 1.8e-3. Hence Conjecture C: for kappa >= 2 the worst
gap is the two-block formula, and the transitional family disappears, just
as the windows do for equal shares.

The first run of this check crashed at the very end, because a numpy boolean
cannot be written to JSON, and nothing was saved. The values are now
converted explicitly and the run was repeated; the numbers above come from
the saved run.

The open cases raised one more question: could general finite laws, not
just sums of segments, reach the certificate bound? Under pinball loss the
cost of a finite law is linear in the atom positions once the order of the
atoms along each test vector is fixed, so the best law in an order cell is
an LP. A local search over such cells, started from the best segment law,
found no improvement in any of three cases
([probe](results/asymmetric/general_law_probe.md)). This is a hint, not a
proof: with asymmetric penalties the relaxation can apparently overstate the
true worst case inside these narrow regions, which never happened with
symmetric loss.

### 18. Trying to prove Conjecture C, and finding it false

The proof started well. Every certificate bound can be written as an
asymmetric weighted distance from z to the points nu 1_S. On a region where
the coordinates of z are sorted, the certificate LP becomes a finite
zero-sum game: one player mixes the top-set indicators, the other mixes
certificates. Two-block laws are exactly the mixtures of two columns, so
the conjecture said that two columns are always enough when kappa >= 2. One
case is easy for every kappa, the symmetric one included: if some subset of
a largest face has a share inside the ceiling window, the ceiling is exact.
This is now Proposition D, and it explains the pattern seen with Theorem 5
(ceiling exact for r <= 0.4, never for r >= 0.7), because the window shrinks
as r grows. For the hard case we grouped the producers into the units, the
producer at which the cumulative share jumps over the window, and the rest.
Six certificates then depend only on three aggregate numbers, and the bound
becomes an LP in three variables.

Testing that LP on a grid first produced a false alarm: we had compared it
only with the top sets of one ordering, while the jump producer alone was
inside the window. With every union of the three blocks allowed, the excess
shrank but did not vanish. The full certificate LP confirmed it on a
concrete face, and a local search then found an explicit law: four
producers with shares (1, 24, 24, 1)/50, depth one, r = 33/50, kappa = 10.
The law reaches 0.266393 against 0.249614 for the best two-block law. It has
three levels: the small producer at 1 and the two large ones at 0.41 and
0.10, a transitional law. To trust it we added a safety margin, rationalized
the law and checked every coalition in exact arithmetic. The first attempt
missed one cap by 4.5e-8 through rounding, so the margin was raised and the
check repeated, after which every constraint holds exactly. Its pinball
costs, evaluated directly, equal the segment costs. The certificate bound for
this instance is 0.2787, so its true worst case is still unknown within that
range ([conjecture_c.md](results/asymmetric/conjecture_c.md)).

So the 299 of 299 was a correct observation and a wrong conclusion: the
counterexample needs a shape that random sampling rarely produces. In a
targeted sample with one small share, two-block laws were beaten in 2 of
200 instances, both at kappa = 2, and in none at kappa = 3 or 10. Conjecture C
is withdrawn; Theorem C and Proposition D stand.

### 19. The literature, properly this time

The first pass of November 6 was a handful of searches. This time we wrote
down the questions first (has anyone bounded the overstatement? are zonoids
used in cost allocation? is the asymmetric extension known?), logged every
query, and checked the bibliographic data of every reference
([literature_review.md](docs/literature_review.md)). The answer to the main
question is still no. The closest work states the fractional relaxation
(Burer and Dror 2005), proves that core membership is NP-hard (Chen and
Zhang 2009) or NP-complete (Guardiola, Meca and Puerto 2020), or shows when
fuzzy and crisp cores coincide (convex fuzzy games). One observation from the
reading changed how the introduction argues. For homogeneous costs an
allocation passes the full fractional check only if it is a subgradient of
the cost extension, the gradient allocation of risk capital allocation. So
the audit tests membership in a much smaller set than the core, and our
results measure how wrong that can be.

Three entries were out of date (two working papers now published, one
missing volume), and ten verified references were added. The environment
blocks Crossref and arXiv, so DOIs were checked through publisher and RePEc
pages, and seven items were seen only as abstracts; they are flagged in the
review. A database search by someone with institutional access remains the
last step before submission.

### 20. What an audit finds on real wind data

Every result so far is a worst case. A referee will ask what happens on
actual production, so we audited real data
([wind_audit.md](results/illustration/wind_audit.md)). There are three
panels of four producers, using the public data the main branch already
verifies by checksum. The first is four nearby WIND Toolkit sites in Texas,
the second the four turbines of the ENGIE La Haute Borne farm, and the third
four distant WIND Toolkit sites in Texas, Iowa, Wyoming and New York. We
added the third panel when the first two turned out to be uninformative: on
them pooling saves almost nothing (r between 0.95 and 0.99). The distant
sites were chosen by a fixed rule from the toolkit's site metadata (the
onshore 16 MW site with the highest capacity factor in each state), and their
checksums are recorded in `configs/illustration_wind_sites.json`. For every
year, two penalty ratios and two allocations (proportional to standalone
costs, and the gradient allocation) we computed the integer and fractional
excesses exactly, with one LP per face over all hours.

The answer is clear. The observed overstatement never exceeds 0.0013 of the
pooled cost. It is exactly zero for the gradient allocation, as the
subgradient remark of Section 19 predicts, and zero for both allocations on
the distant sites, where the worst case for the same shares and floor is as
large as 0.41. Real production is far from the extremal laws, so the bounds
are guarantees, not predictions. When r is close to one they certify the
audit with no knowledge of the joint law. When r is low they say such a
certificate is impossible from r alone. That is a weaker selling point than
"audits are badly wrong in practice", but it is the honest one, and the paper
now says so.

Two practical notes. The first version built the LP with dense matrices
(two blocks of 8760 by 8760, about 1.2 GB) and stalled; with sparse
matrices one LP over a year takes about three seconds. Also, the first run
was stopped and restarted to include the third panel, so the saved results
come from a single complete run.

### 21. A full re-reading, and one idea ruled out

We re-read the paper from start to finish as a referee would. Two passages
needed correcting. In the proof of the last-depth theorem the fourth bound
was attributed to a triangle inequality through the cap of the unit
producer; it actually comes from the certificate with the pair at level t
(the four bounds themselves were right). In the equal-share proof the letter
kappa counted excluded members, which clashes with the penalty ratio of the
asymmetric section. Every number quoted in the paper was traced to a saved
result, and the toy pipeline of the main branch still reproduces its saved
numbers exactly.

For the open asymmetric regions, the idea was to sharpen the relaxation with
an inequality that every pinball cost satisfies. Hlawka's inequality was the
obvious candidate: every sum of segments satisfies it. It fails for general
laws, already with symmetric penalties, and we verified a violation exactly
for each ratio ([hlawka.md](results/asymmetric/hlawka.md)). So that door is
closed; an inequality would have to use the structure of sections of
zonoids more specifically.

### What we would do next

The list is kept up to date in [PROGRESS.md](PROGRESS.md).

1. Transitional laws for arbitrary shares under asymmetric penalties: an
   explicit family playing the role of V, and the exact worst case of the
   counterexample (between 0.2664 and 0.2787).
2. The remaining asymmetric regions: either an asymmetric analogue of V_p,
   or a proof that no demand law reaches the relaxation there.
3. Revise the draft in `paper_exact/`: a careful read of every proof, an
   example section with numbers a practitioner can use, and the literature
   check of the plan.
4. Prove Conjecture 6: an upper-bound argument for arbitrary shares, along
   the lines of Theorem 4 (few active certificates, explicit dual weights),
   and general conditions for the transitional family.
5. Check the literature on zonotopes and zonoids in cooperative games before
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
| PF13 | Families H_p and V_p of explicit laws inside the windows | exact_envelopes.md Section 5 | Proved; algebra checked symbolically (results/verification), exact checks at 324 saved ratios |
| PF14 | A certificate LP bounds the equal-share worst gap for every law; it equals the best explicit law at all 324 tested window ratios | exact_envelopes.md Section 5; window_envelopes.md | Upper bound proved; equality now also follows from PF17 |
| PF15 | Theorem 3: for three free producers and 1/5 <= r <= 1/3 the worst gap is 2(2-r+3r^2)/(n(1+3r)); the four-producer depth-one curve is complete | exact_envelopes.md Section 5 | Proved |
| PF16 | For arbitrary shares, a certificate LP bounds the worst gap for every law; in 68 of 68 random instances (n = 4..6, depths 1..3) it equals the exact relaxation, and in 38 of 38 an explicit law reaches it | exact_envelopes.md Section 6; certificate_method.md | Upper bound proved; equality computational |
| PF20 | Conjecture 6: for arbitrary shares and any depth the worst gap is the maximum over the four families C31, H, G, V | exact_envelopes.md Section 6; general_formula.md (1000 of 1000) and certificate_method.md (68 of 68) | Lower bound proved (V checked per instance); upper bound computational |
| PF19 | Theorem 5: for arbitrary shares and any depth, two explicit families give the lower bound max over partitions of (1-r)a(F) or A_J(1-r^2)/(2r) under stated conditions | exact_envelopes.md Section 6; algebra checked symbolically; exact checks on the 1068 saved instances | Proved lower bound; equals the exact worst gap in 67 of 68 random instances |
| PF18 | Proposition 5: for r < 1 the suprema of Theorems 1, 2 and 4 (and the values attained in the two-LP computations) are unchanged under strict stability and positive definite covariance | exact_envelopes.md Section 7; strict_mixtures.md (12 mixed laws) | Proved |
| PF17 | Theorem 4: inside each equal-share window the worst gap is V_p(r) if Q(r) >= 0 and H_{p+1}(r) if Q(r) <= 0, with explicit laws; with Theorem 1 the equal-share case is solved for every n, depth and r | exact_envelopes.md Section 5; window_envelopes.md; 129,888 exact window checks | Proved |

| PF21 | With asymmetric penalties of ratio kappa the cost is sublinear with c(-x) <= kappa c(x); every sum of kappa-segments is the cost of a finite three-point mixture; hence the C31 ceiling remains an upper bound and every symmetric lower bound remains attained | asymmetric_penalties.md Sections 1-2; symbolic group K | Proved |
| PF22 | Theorem A: arbitrary shares at depth n-2, exact worst gap for every kappa, three regimes per ordered pair, explicit laws; kappa = 1 gives Theorem 2 | asymmetric_penalties.md Section 4; 300 of 300 random instances (construction, law, certificate) | Proved |
| PF23 | Theorem B: equal shares, any depth, worst gap min{(1-r)m/n, H_1} outside windows that are nonempty iff kappa < (p+1)(m-p)/(pm); none for kappa >= 2(m-1)/m | asymmetric_penalties.md Section 5; 5565 exact constructions, 1305 laws, 288 certificate cross-checks | Proved |
| PF24 | Inside the remaining windows (1 < kappa < 2(m-1)/m), and in 3 of 204 arbitrary-share instances with 1 < kappa < 2, the certificate bound equals the exact relaxation but the best explicit law found stays up to 1.8e-3 below it; a local search over general finite laws did not improve on segment laws in 3 of these cases | asymmetric_penalties.md Sections 6-7; asymmetric_checks.md part D; general_shares.md; general_law_probe.md | Open; evidence of a gap between relaxation and demand laws |
| PF25 | Theorem C: for arbitrary shares, every depth and every kappa, the worst gap is at least the maximum over excluded sets and splits into units and fractional producers of Psi_kappa(a(I), A_J) | asymmetric_penalties.md Section 7; symbolic group L; 600 of 600 laws verified exactly | Proved |
| PF26 | Conjecture C: for kappa >= 2 the bound of PF25 is the worst gap | general_shares.md: 299 of 299 random instances; conjecture_c.md: exact counterexample at kappa = 10 (0.266393 against 0.249614), 2 of 200 failures in a sample with one small share | Refuted; negative result kept |
| PF27 | Proposition D: for every kappa >= 1, if a subset of a largest face has share in [(1-r)/(1+kappa), kappa(1-r)/(r+kappa)] a(F), the worst gap equals the elementary ceiling; in particular when every producer's share is at most the window width | asymmetric_penalties.md Section 7; symbolic group M | Proved |

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
* `paper_exact/`: the eight-page draft built from the plan (`main.tex`, `references.bib`, the figure and the compiled `main.pdf`).
* `scripts/check_*envelope*.py` (including `check_window_envelopes.py`), `scripts/check_zonotope_realizability.py`, `scripts/check_realizability_conjecture.py`: generators of the summaries in `results/exclusion/`.
* `tests/test_exact_envelopes.py`, `tests/test_seminorm_envelope.py`, `tests/test_certificates.py`, `tests/test_symbolic.py`: fast tests.
* `scripts/verify_symbolic.py`, `requirements-verify.txt` and `results/verification/`: symbolic verification of the proofs.
* `PROGRESS.md`: one-page progress report with the current next steps.
* `docs/literature_review.md` and `docs/proof_guide.md`: the systematic literature review and the guide for the expert reading.
* `scripts/illustrate_wind_audit.py`, `scripts/table_wind_audit.py`, `configs/illustration_wind_sites.json`, `results/illustration/` and `tests/test_illustration.py`: the illustration on wind data.
* `src/censored_newsvendor/asymmetric.py`, `docs/asymmetric_penalties.md`, `scripts/check_asymmetric_penalties.py`, `scripts/check_asymmetric_general.py`, `scripts/probe_general_laws.py`, `scripts/refute_conjecture_c.py`, `results/asymmetric/` and `tests/test_asymmetric.py`: asymmetric imbalance penalties.

## Merging

```bash
git fetch origin
git checkout main
git merge origin/pulp-fiction
```

Then number the claim rows above and, if wanted, link the two notes from
the README.
