# Plan for the revised paper

November 6, 2026, branch `pulp-fiction`. This is a proposal for rebuilding the
manuscript around the exact results of [exact_envelopes.md](exact_envelopes.md).
Nothing in `paper/` has been changed on this branch.

## What changed since the first draft

The November 5 draft had one theorem: the fractional audit can overstate the
best coalition saving by as much as the trivial ceiling allows. Its upper
bound was one line, its extremal family needed the expected cost L to vanish,
and the standalone-ratio refinement (C31) was an elementary inequality whose
sharpness was unknown. Reviewers would likely have called it thin.

The question is now answered in full for equal shares and at the deepest
exclusion level for arbitrary shares, with explicit worst-case demand laws and
a computational method that has matched upper and lower bounds in every
instance tried. That is a different paper: the main object is the exact
worst-case error of the audit as a function of how much of their standalone
cost the producers are charged.

## Working title

*How much can a fractional audit overstate coalition savings? Exact bounds
for pooled newsvendor costs under a standalone-cost floor*

## Draft abstract

Producers that pool their imbalance risk, such as wind farms bidding jointly,
share the expected cost of the pooled offer and must check that no group of
them would do better on its own. Checking every coalition is hard, so the
check is often relaxed to fractional memberships. We ask how far that
relaxation can overstate the largest saving available to an actual
coalition, when every producer is known to pay at least a fraction r of its
standalone cost and k producers are excluded from the search. For equal
shares we give the exact worst case for every number of producers, every
depth k and every r. It equals the elementary ceiling (1-r)(n-k)/n on a union
of intervals and is strictly smaller elsewhere, with closed forms in all
regimes. For arbitrary shares we give the exact worst case at the deepest
nonterminal level. Every bound is attained by an explicit finite demand law.
The constructions rest on the fact that the costs of symmetric demand laws are
zonotope support functions, and the upper bounds on triangle-inequality
certificates. For arbitrary shares and depths, a pair of linear programs
built from the same two ingredients determines the worst case in every
instance we computed.

## Contributions

1. Exact worst-case audit error for equal shares, every n, depth and r
   (Theorems 1 and 4), with the regimes stated explicitly: where the
   elementary (1-r) ceiling is exact, where it is not, and by how much.
2. Exact worst case for arbitrary positive shares at depth n-2 (Theorem 2),
   which for three producers extends C39 and shows that the C39 argument
   alone is not sharp with unequal shares.
3. Explicit worst-case demand laws: finite, centrally symmetric, with at most
   2n atoms, mapped into the unit box with an optimal grand offer.
4. A two-LP method for arbitrary shares: a certificate LP that bounds every
   law and a zonotope LP that produces a law; they agreed in all 68 random
   instances computed (38 with an explicit law), and in 29 earlier cases.
5. The observation behind 3 and 4: for symmetric absolute loss, the worst case
   over demand laws coincided with the worst case over all seminorms in every
   case computed (the realizability conjecture).

## Proposed structure

1. **Introduction.** Pooling of imbalance risk by renewable producers; the
   audit problem; why coalition checks are relaxed (hardness, Chen and Zhang
   2009); the question and the answer in one paragraph with the figure.
   Related work: cooperative newsvendor games (Hartman, Dror and Shaked 2000;
   Muller, Scarsini and Shaked 2002; Montrucchio et al. 2012), wind
   aggregation (Baeyens et al. 2013; Chakraborty et al. 2018), integrality
   gaps and approximate cores (Deng, Ibaraki and Nagamochi 1999; Goemans and
   Skutella 2004; Caprara and Letchford 2010), fractional participation
   (Aubin 1981; Denault 2001), the 2005 Burer-Dror manuscript.
2. **Model.** Physical fractional cost, exclusion hierarchy, standalone ratio.
   C30 and C31 as the elementary ceilings, proved in a few lines.
3. **Two tools.** Costs of symmetric laws are zonotope support functions
   (Lemma 5 of the seminorm note) and laws can be read off generators;
   triangle certificates give upper bounds (Lemma 1 there, in dual form).
4. **Equal shares.** Theorem 1 (intervals and the high regime), Theorem 4
   (windows), the complete four-producer curve as a worked example, the
   window lengths, the figure.
5. **Arbitrary shares at the deepest level.** Theorem 2 and its three regimes.
6. **Arbitrary shares at any depth.** The two-LP method and the computational
   results; the realizability conjecture stated as such.
7. **What the exact curves say.** When the audit can be trusted: the ceiling
   (1-r)(n-k)/n is the answer on most of the range, the improvements are
   real but modest, and the audit can still report large spurious savings
   even when every producer pays a substantial part of its standalone cost.
8. **Open questions.** Closed forms for arbitrary shares at intermediate
   depths, a proof of realizability, asymmetric penalties.

Appendix: proofs of the constructions (corner checks), the certificate LP,
and the reproducibility map (scripts and saved results).

## Material from the first draft

Keep: the model, C30 (as a remark), the root correspondence with Burer and
Dror, the physical versus canonical extension example (it explains why the
gap exists). Move to a companion note: the statistical certificates, the
precision comparison of Section 6 and Appendix A, and Table 2. Drop:
Appendix B and the defensive phrasing.

## Likely objections and how the new results answer them

* *"The bounds are elementary."* The upper bounds are short, but exactness is
  not: it needs the explicit laws, the window families and the dual
  certificates, and the answer has a structure (intervals, windows, a
  switching quadratic) that the elementary bound does not predict.
* *"The extremal examples are degenerate."* At fixed r the worst-case laws
  have L bounded away from zero relative to their scale, and Proposition 5
  shows that requiring positive definite covariance and strict stability of
  every coalition does not change any of the suprema.
* *"Who uses this relaxation?"* The paper should present it as the natural
  tractable certificate for core membership in pooled newsvendor games, cite
  where partial or fractional memberships appear (Burer and Dror 2005;
  Bonnans and Andre 2008), and show that the exact answer tells a practitioner
  how much to discount a fractional audit.
* *"Equal shares are special."* Theorem 2 and the two-LP results cover
  unequal shares; the paper should say plainly that a closed form at
  intermediate depths is open.

## Venue

A short theory paper of this kind fits Operations Research Letters, TOP,
Mathematical Methods of Operations Research or the International Journal of
Game Theory. A stronger outlet would need either a proof of the realizability
conjecture or a closed form for arbitrary shares at depth one.

## Before submission

1. Literature check on zonotopes and zonoids in cooperative games and in
   newsvendor pooling, to place contributions 3 to 5.
2. Independent reading of the proofs of Theorems 1 to 4 (the corner checks
   and the dual weights in particular).
3. Rewrite of the manuscript along the structure above, with the figure in
   `results/exclusion/exact_envelopes.png`.
