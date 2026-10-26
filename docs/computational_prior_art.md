# Computational prior-art follow-up

Date: **2026-10-26**. Scope: the [sparse-tail derivation](sparse_scenarios.md),
following the earlier [identification audit](novelty_audit.md).

## Primary-source comparison

**Perakis and Roels, Robust Controls for Network Revenue Management (2010).**
The [MIT-hosted online companion](https://mitsloan.mit.edu/shared/ods/documents/?PublicationDocumentID=2281)
was inspected at proofs of Propositions 1, 2(a) and 5, especially pp. 3--4
and 10--11. Proposition 2(a) reduces a single-resource worst-regret problem to
convex maximization with individual upper bounds and then to knapsack.
Proposition 5 gives a single-resource nested-control LP using ordered low/high
demand scenarios. Thus both vertex arguments and small regret-scenario families
are established tools. Our inference: these passages do not immediately supply
the fixed-prefix, distribution-aware theorem, but they substantially narrow any
plausible methodological novelty claim. The main article and remaining proofs
have not been fully audited.

**An, Mikhaylov and Jung (2021).** The publisher's
[abstract, introduction and section excerpts](https://www.sciencedirect.com/science/article/pii/S0969699720305615)
describe an LP for evaluating worst regret under interval demand information and
a genetic algorithm for booking-limit optimization. Their comparator uses
realized-demand hindsight. This is additional evidence that an LP formulation
alone is not a novel research direction. Full propositions were not accessible;
no equivalence to our population ambiguity model is asserted.

**Roels (2006).** The [MIT thesis record](https://dspace.mit.edu/entities/publication/683dc5a1-2bc8-49c4-a19b-d6ab7e3273eb)
identifies the thesis and downloadable PDF. Retrieval attempts through MIT and
an indexed CiteSeer copy did not yield the relevant full chapter. The earlier
Perakis--Roels article explicitly points there for multiproduct capacity results.
This remains a specific unresolved comparison, not evidence that the work omits
our result.

## What still has to be mapped

| Element | Current derivation | Required comparison |
| --- | --- | --- |
| Information | Exact fixed censored-sales law; unrestricted compatible tails | Can an existing ambiguity model represent this law exactly, including atoms? |
| Comparator | Distribution-aware expected-cost optimum under the same constraints | Distinguish realized-demand hindsight and online competitive regret |
| Constraint geometry | Continuous packing polytope; all order caps included in `A` | Check whether known results already imply the rank bound |
| Endpoint family | At most `rank(A)` upper tails, uniformly for every decision | Compare selected families and tie cases, not just their cardinality |
| Algorithm | Exact finite-atomic LPs for fixed rank | Separate known convex epigraph machinery from any additional structural result |

Searches used both engines, exact titles, author publication links, and phrases
including `newsvendor regret n+1`, `regret censored rank inventory`, and
`minimax regret newsvendor scenarios capacity`. Failed keyword searches do not
support an absence claim. Broad inventory surveys were discovery leads only;
technical comparisons above use primary sources.

## Working decision

Retain the sparse-tail theorem and reproducible checks as a **candidate
structural result**. Do not start a manuscript asserting originality, claim to
have solved a previously hard problem, or treat a different comparator's
hardness result as our own. Resolve the thesis comparison and seek independent
mathematical scrutiny before deciding whether to pursue publication on this
static model. Statistical estimation and practical forecasting are still
separate, unfinished questions.
