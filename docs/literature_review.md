# Literature review

November 7, 2026, branch `pulp-fiction`. This replaces the short first pass
in [paper_plan.md](paper_plan.md). It does not replace a database search
(Scopus, Web of Science, MathSciNet) by someone with institutional access;
see the last section.

## Questions

1. Has anyone bounded, in the worst case over demand laws, how much a
   fractional (relaxed) coalition audit can overstate the largest saving of
   an actual coalition, as a function of a standalone-cost floor?
2. Are zonoid or zonotope constructions used for cost allocation or for
   cooperative games of the newsvendor type?
3. Is the asymmetric-penalty extension (pinball loss, quasi-symmetric costs)
   covered by existing work on deviation measures or quantile offers?
4. Are the bibliographic data of every reference correct?

## Method

Web searches on 7 November 2026 (the queries are listed below), reading
publisher pages, RePEc/IDEAS records, institutional repositories and
Project Euclid. Two limits: the network policy of the environment blocks
`api.crossref.org` and `arxiv.org`, so DOIs could not be checked
automatically and arXiv full texts could not be opened. Where only an
abstract or metadata was seen, the table says so. The fourteen entries
added on 5 and 6 November keep their notes on which parts of the full text
were inspected then.

| # | Query (abridged) | Outcome |
| --- | --- | --- |
| 1 | Chen Zhang stochastic programming duality inventory centralization games NP-hard | OR 57(4):840-851 (2009); membership in the core is NP-hard to decide even in a simple setting; strong duality gives a core element |
| 2 | fuzzy core vs core, homogeneous cost, fractional coalitions, Aubin | Aubin core and its relation to the crisp core for convex and homogeneous fuzzy games; nothing on the gap for cost games |
| 3 | Csóka Herings Kóczy stable allocations of risk | GEB 67(1):266-276 (2009): risk allocation games = totally balanced games |
| 4 | renewable portfolio nucleolus Benders, Freire Street Lima Barroso | IEEE TPS 30(6):3265-3275 (2015): exponentially many coalition constraints handled by MILP and Benders |
| 5 | Montrucchio Scarsini large newsvendor games | GEB 58(2):316-337 (2007); core a singleton for large games with nonatomic demand |
| 6 | Samet Zemel core and dual set of LP games | MOR 9(2), 1984, DOI 10.1287/moor.9.2.309 (pages 309-316 in our entry, from the full text read on Nov 5) |
| 7 | Tijs Branzei Ishihara Muto cores and stable sets for fuzzy games | Fuzzy Sets and Systems 146(2):285-296 (2004): for convex fuzzy games all cores coincide |
| 8 | Denault coherent allocation of risk capital | J. Risk 4(1):1-34 (2001): fuzzy games, Aumann-Shapley (gradient) allocation |
| 9 | Baeyens Bitar Khargonekar Poolla coalitional aggregation of wind power | IEEE TPS 28(4):3774-3784 (2013): balanced game, nonempty core; conference version: not convex, Shapley value may lie outside the core |
| 10 | core membership verification, fractional relaxation, worst case, standalone ratio (extended search) | nothing on the question; related: epsilon-fractional cores (hedonic games), LP estimation of the core, NP-completeness for production-inventory games |
| 11 | zonotope or zonoid, cooperative game, cost allocation, newsvendor | nothing connecting the two |
| 12 | Fischer risk capital allocation one-sided moments | Insurance Math. Econ. 32(1):135-146 (2003) |
| 13 | LP approach to estimate the core in cooperative games | arXiv:2510.01766 (Camacho, Gonçalves-Dosantos, Sánchez-Soriano, 2025): inner approximation of the core by sampled extreme points |
| 14 | robust newsvendor games with ambiguity in demand distributions | OR 68(4):1047-1062 (2020), Doan and Nguyen: core existence through worst-case distributions in Fréchet classes |
| 15 | quid pro quo allocations in production-inventory games | arXiv:2002.00953 (Guardiola, Meca, Puerto, 2020): core membership is NP-complete for PI-games |
| 16 | Rockafellar Uryasev Zabarankin generalized deviations | Finance Stoch. 10(1):51-74 (2006), DOI 10.1007/s00780-005-0165-8: deviation measures, CVaR deviation |
| 17-21 | verification of Chakraborty et al. 2018, Montrucchio et al. 2012, Caprara and Letchford 2010, Chen et al. 2019, Molchanov et al. | all confirmed; Chen et al. is MS 65(5):2142-2160; Molchanov et al. appeared in Bernoulli 20(3):1210-1233 (2014) |
| 22-24 | Koshevoy Mosler zonoid trimming; Pinson et al. 2007; Bitar et al. 2012 | Ann. Statist. 25(5):1998-2017 (1997); IEEE TPS 22(3):1148-1156 (2007); IEEE TPS 27(3):1225-1235 (2012) |
| 25 | fuzzy newsvendor or fuzzy inventory game, Aubin core | nothing; only crisp newsvendor games |

## Map of the literature

**Newsvendor and inventory centralization games.** The core is nonempty
(Hartman, Dror and Shaked 2000; Müller, Scarsini and Shaked 2002), and strong
duality of stochastic programs produces a core allocation (Chen and Zhang
2009; Burer and Dror 2012). Large games with nonatomic demand have a single
core allocation (Montrucchio and Scarsini 2007). Later work asks for more
than the core: population monotonic schemes (Chen, Gao, Hu and Wang 2019),
or robustness to an ambiguous joint distribution, where worst-case
distributions decide whether the core is nonempty (Doan and Nguyen 2020).
The review by Montrucchio, Norde, Özen, Scarsini and Slikker (2012) covers
the classical results. All of these study the existence or construction of
good allocations. None takes an allocation as given and asks how reliable a
relaxed check of it is.

**Checking core membership.** Deciding whether a given allocation is in the
core is NP-hard for inventory centralization games (Chen and Zhang 2009) and
NP-complete for production-inventory games (Guardiola, Meca and Puerto 2020).
Combinatorial optimization games tie the core to integrality gaps of LP
relaxations (Deng, Ibaraki and Nagamochi 1999; Goemans and Skutella 2004;
Caprara and Letchford 2010). Computational work handles the exponentially
many coalition constraints by row generation or mixed continuous/binary
coalition models (Bonnans and André 2008; Freire, Street, Lima and Barroso
2015), or approximates the core from inside (Camacho et al. 2025). The
fixed-allocation fractional relaxation we analyze is stated in Burer and
Dror (2005, Section 5). We found no worst-case analysis of its overstatement.

**Fractional participation.** Aubin (1981) introduced games with fuzzy
coalitions. For convex fuzzy games the fuzzy and crisp cores coincide (Tijs,
Brânzei, Ishihara and Muto 2004). Shellshear (2009) characterizes core
stability through fuzzy games. For positively homogeneous costs the full
fractional check has a precise meaning: an efficient allocation passes it
only if it is a subgradient, on nonnegative memberships, of the homogeneous
cost extension at the grand coalition. In the differentiable case this is the
Aumann-Shapley or gradient allocation (Denault 2001; Fischer 2003). Samet and Zemel (1984) give conditions under which the
dual allocations of LP games exhaust the core. So the fractional audit tests
membership in a set that is usually much smaller than the core. Our results
quantify, in the worst case, how far the two answers can differ for an
allocation that is in the core.

**Risk allocation.** Risk allocation games with coherent risk measures are
exactly the totally balanced games (Csóka, Herings and Kóczy 2009). The
asymmetric pinball cost is a scaled CVaR-type deviation measure in the sense
of Rockafellar, Uryasev and Zabarankin (2006): c(x) = tau(E X - LCVaR_tau(X))
for X = x'Y.

**Energy applications.** Coalitions of wind producers have a nonempty core
(Baeyens, Bitar, Khargonekar and Poolla 2013), and cost-causation
allocations have been applied to wind producers in the Iberian market
(Chakraborty, Baeyens and Khargonekar 2018). Optimal offers of a single
producer under penalties for deviations are studied by Pinson, Chevallier
and Kariniotakis (2007) and Bitar et al. (2012); that the optimal offer is
a quantile of production when the two penalties are linear is the
newsvendor critical-fractile argument. We could only read the abstracts of
the last two papers, so the paper should not attribute that statement to
them specifically.

**Zonoids.** The first absolute moments E|<u, X>| of a random vector form
the support function of a zonoid. This is classical (Koshevoy and Mosler
1997; Molchanov, Schmutz and Stucki 2014) and must be credited. We found no
use of zonoids or zonotopes in cooperative cost allocation.

## Novelty, contribution by contribution

| Contribution | Closest prior work | What is different | Assessment |
| --- | --- | --- | --- |
| Worst-case overstatement of the fractional audit under a standalone floor (Theorems 1-5, Proposition 5) | Burer and Dror (2005) state the relaxation; fuzzy-game results say when fuzzy and crisp cores coincide (convex games) | a quantitative, distribution-free worst case, with exact constants and explicit attaining laws | no prior found |
| Windows and the switching quadratic (Theorem 4) | none | structure specific to the problem | no prior found |
| Explicit worst-case laws from zonotopes | the zonoid identity (Koshevoy and Mosler; Molchanov et al.) | its use to build extremal demand laws for an allocation problem | identity classical, use new as far as we found |
| Certificate LP upper bounds | triangle inequalities for seminorms, LP duality | the specific certificates and their exactness in the tested instances | technique standard, application new |
| Asymmetric penalties (Theorems A-C, Proposition D) | deviation measures (Rockafellar et al. 2006), quantile offers in wind trading | worst-case audit gap for quasi-symmetric costs; windows close at 2(m-1)/m | no prior found |
| Ceiling criterion (Proposition D) | none | an elementary consequence of Theorem C and the ceiling | new but simple; present as a proposition |

"No prior found" is a statement about this search, not a claim of priority.
The paper should say "we are not aware of" rather than "the first".

## Corrections made to the bibliography

* Montrucchio and Scarsini: the journal version (GEB 58(2):316-337, 2007,
  DOI 10.1016/j.geb.2006.04.003) replaces the 2006 working paper; the key is
  unchanged.
* Molchanov, Schmutz and Stucki: Bernoulli 20(3):1210-1233 (2014),
  DOI 10.3150/13-BEJ519, replaces the arXiv preprint.
* Chen, Gao, Hu and Wang: volume 65, issue 5, pages 2142-2160 added.
* Denault: volume 4, issue 1, pages 1-34 added.
* Caprara and Letchford: issue 1-2 added. Koshevoy and Mosler: DOI added.
* New entries: Csóka et al. 2009, Tijs et al. 2004, Freire et al. 2015,
  Doan and Nguyen 2020, Guardiola et al. 2020, Camacho et al. 2025,
  Rockafellar et al. 2006, Fischer 2003, Pinson et al. 2007, Bitar et al. 2012.

## Still to do before submission

* A database search (Scopus or Web of Science, MathSciNet) on "fuzzy core",
  "fractional coalitions", "core membership" and "newsvendor game", by
  someone with access. Forward citations of Burer and Dror (2005) and of
  Chen and Zhang (2009) are the most likely place for overlooked prior work.
* Full-text checks of the items seen only as abstracts: Tijs et al. 2004,
  Doan and Nguyen 2020, Guardiola et al. 2020, Camacho et al. 2025, Pinson
  et al. 2007, Bitar et al. 2012, Fischer 2003.
* Allowing `api.crossref.org` and `arxiv.org` in the environment would let
  the DOI checks run automatically.
