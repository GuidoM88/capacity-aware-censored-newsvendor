# pulp-fiction

This branch follows one question to the end: how badly can the fractional
coalition audit overstate savings once every producer is known to pay at
least a fraction r of its standalone cost? C39 answered it for three
producers with equal shares. Here we try to answer it in general.

The branch starts from `main` at `309977c` and only adds files, so merging
is mechanical. Work on `main` went on in parallel; keeping the two apart made
it easy to compare them before deciding what goes into the paper.

## Where things stand

* **Equal shares, any number of producers, any depth: settled except on
  explicit "windows" of r** ([Theorem 1](docs/exact_envelopes.md)). The
  elementary C31 ceiling (1-r)m/n is exact on a union of intervals, and for
  r >= (m-1)/(m+1) the exact value is (m-1)(1-r^2)/(2nr); m = n-k is the
  number of free producers at depth k. Every value comes with an explicit
  finite demand law.
* **Arbitrary shares at the last nonterminal depth n-2: settled for every r**
  ([Theorem 2](docs/exact_envelopes.md)). For three producers this extends
  C39 to unequal shares. The C39 argument by itself is not sharp there: at
  w = (3/5, 1/4, 3/20) and r = 1/5 it gives 0.68, while the true worst gap is
  17/28 = 0.607.
* **A method that certifies values numerically.** An LP over all seminorms
  gives an upper bound for a fixed membership; an LP over finite symmetric
  laws produces a law that attains it. When the two meet, the value is exact.
  So far they have met in every case tried (Section 7 of the log).
* **Negative results kept on record.** Charging in proportion to standalone
  costs does not tame the gap beyond three producers. The windows are not a
  thin sliver: they cover 13 to 20 percent of the range of r for 4 to 30
  producers.
* **Open.** The exact values inside the windows; unequal shares at depths
  1 to n-3; asymmetric imbalance penalties.

## How to read the branch

Start with [docs/exact_envelopes.md](docs/exact_envelopes.md): statements and
complete proofs of the two theorems. [docs/seminorm_envelope.md](docs/seminorm_envelope.md)
explains the oracle, the upper bounds and the numerical map that led there.
The `results/exclusion/*.md` files are generated from saved JSON by the
scripts listed at the end and should not be edited by hand.

```bash
python -m pip install -r requirements.txt
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
python scripts/check_exact_envelopes.py
python scripts/check_seminorm_envelope.py
python scripts/check_zonotope_realizability.py
python scripts/check_proportional_envelope.py
python scripts/check_realizability_conjecture.py
```

The first two scripts take about a minute and seven minutes on four cores;
the realizability scripts a few minutes each.

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

*In progress.*

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
| PF11 | For equal shares at depth one, the windows where the value is open have total length 0.13 to 0.20 for 4 <= n <= 30, decaying like n^(-1/2) | exact_envelopes.md, windows table | Exact computation of the intervals; window values open |

PF3 and PF6 of the earlier version (numerical windows, configuration
heuristic) are superseded by PF9 and PF11.

## Files

* `src/censored_newsvendor/exact_envelopes.py`: the explicit laws, closed forms, windows and exact verification.
* `src/censored_newsvendor/seminorm_envelope.py`: the seminorm oracle, the zonotope LP and the proved bounds.
* `docs/exact_envelopes.md`: Theorems 1 and 2 with proofs.
* `docs/seminorm_envelope.md`: the oracle, upper bounds, numerical map and realizability check.
* `scripts/check_*envelope*.py`, `scripts/check_zonotope_realizability.py`, `scripts/check_realizability_conjecture.py`: generators of the summaries in `results/exclusion/`.
* `tests/test_exact_envelopes.py`, `tests/test_seminorm_envelope.py`: fast tests.

## Merging

```bash
git fetch origin
git checkout main
git merge origin/pulp-fiction
```

Then number the claim rows above and, if wanted, link the two notes from
the README.
