# Literature map

Updated **2026-10-26**. See the [originality audit](novelty_audit.md) for the
research decision. This is a working map, not an exhaustive review or a
certificate of novelty. Links point to primary sources; reading depth is explicit.

| Work | Relevant scope | Why it matters | Reading status |
| --- | --- | --- | --- |
| Hssaine and Sinclair, *The Data-Driven Censored Newsvendor Problem*, arXiv:2412.01763v3 | Scalar offline identification, minimax risk and finite-sample guarantees | Direct conceptual overlap; their bound on the optimal unconstrained quantile differs from our capacity-constrained comparator | Model, Proposition 3.3, Theorem 3.4 and proof sketch inspected; not every appendix proof reproduced |
| Kumar and Mouchtaki, *What is the Value of Censored Data?*, arXiv:2602.16842v2 | Scalar finite-sample regret under bounded demand | Stronger finite-sample prior art than our population example; vector coupling is not covered by a simple substitution | Definition 1, Theorems 1 and 4, and reduction argument inspected |
| Shi, Chen and Duenyas (2016) | Censored multiproduct learning with warehouse capacity and carry-over | Establishes that the combination of those three ingredients is not itself new | Author PDF model, Assumption 1, DDM and Theorem 2 inspected |
| Zheng, Chen, Hedenstierna and Yang (2026) | Offline multiproduct demand and substitution estimation | Relevant offline prior art with observation-coverage conditions | Publisher abstract and companion B.1 inspected; complete main text still inaccessible |
| Perakis and Roels, *Regret in the Newsvendor Model with Partial Information* (2008) | Distributional minimax regret with partial information | Section 6 explicitly points to capacity-constrained multiproduct results in Roels' thesis | Author-hosted article formulation and conclusion inspected; thesis chapter not obtained |
| Perakis and Roels, *Robust Controls for Network Revenue Management* (2010) | Robust capacity allocation with polyhedral uncertainty | Computational prior art for any proposed scalable regret algorithm | Primary abstract and repository-indexed section 4 inspected; full reduction comparison pending |

## Primary sources

1. Hssaine and Sinclair: https://arxiv.org/abs/2412.01763v3
2. Kumar and Mouchtaki: https://arxiv.org/abs/2602.16842v2
3. Shi, Chen and Duenyas: https://congshi-research.github.io/papers/nonparametric-multi-product.Final.pdf
4. Zheng et al.: https://doi.org/10.1177/10591478261424592
   - Companion: https://journals.sagepub.com/doi/suppl/10.1177/10591478261424592/suppl_file/sj-pdf-1-pao-10.1177_10591478261424592.pdf
   - Author preprint landing page: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4008913
5. Perakis and Roels (2008): https://www.anderson.ucla.edu/documents/areas/fac/dotm/bio/pdf_GR03.pdf
6. Roels (2006), thesis landing page: https://dspace.mit.edu/entities/publication/683dc5a1-2bc8-49c4-a19b-d6ab7e3273eb
7. Perakis and Roels (2010): https://doi.org/10.1287/msom.1080.0252

## Adjacent leads, not established equivalents

- Vairaktarakis (2000), *Robust multi-item newsboy models with a budget
  constraint*: https://www.sciencedirect.com/science/article/abs/pii/S0925527399001292
  (primary search-index record; full text not obtained). The
  [Roels author note](https://www.anderson.ucla.edu/documents/areas/fac/dotm/bio/pdf_GR01.pdf)
  distinguishes its realized-demand comparator from distribution-aware regret.
- Boonstra, van Eekelen and van Leeuwaarden, *Robust knapsack ordering for a
  partially-informed newsvendor with budget constraint*:
  https://arxiv.org/abs/2301.02662 (abstract inspected). Its objective is worst
  expected cost with range/mean/deviation information, not the present regret.
- Fu, Li and Zhang (2024), *Distributionally Robust Newsvendor Under Stochastic
  Dominance with a Feature-Based Application*:
  https://doi.org/10.1287/msom.2023.0159 (primary abstract inspected). Stochastic
  dominance ambiguity sets are relevant background; a common vocabulary does
  not establish that its absolute-cost results solve our regret problem.

## Candidate difference to investigate

The current question concerns identification and minimax regret from **fixed
offline censored observations**, with products coupled through a resource
constraint. Offline learning, capacity constraints, censored demand, robust
optimization, and multiplier-adjusted quantiles are individually established.
A useful contribution needs an explicit result that the nearest existing
theorems do not already imply.

The current audit derives an elementary general identification criterion and
rejects identification alone as the planned central contribution. The next
bounded question concerns computation of full-class regret; its novelty is
still unestablished.

For each proposed claim, compare the information model, admissible distributions,
decision set, comparator, and exact theorem conclusion. Search citing papers and
alternative terminology such as partial identification, limited observability,
resource allocation, and offline inventory learning. A failed keyword search is
not evidence that a result is new.

## Possible later data source

[FreshRetailNet-50K](https://arxiv.org/abs/2505.16319v5) provides stockout-annotated
retail sales. The title/version matters: earlier versions and related releases
use different naming. Inspect the selected release, schema and license before
adding a loader. No data is currently downloaded or used.

Stockout annotations do not reveal the lost demand. Controlled censoring on
otherwise observed series can support a semi-synthetic evaluation; an imputed
series must not be presented as independently observed ground truth. The static
population example does not establish validity for seasonal or dependent demand.
