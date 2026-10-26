# Literature map

Initial search checked on **2026-10-25**. This is a working map, not an exhaustive
review or a certificate of novelty. Links point to primary sources. Review depth
is stated to avoid treating an abstract as a full-paper comparison.

| Work | Relevant scope | Why it matters | Reading status |
| --- | --- | --- | --- |
| Hssaine and Sinclair, *The Data-Driven Censored Newsvendor Problem*, arXiv:2412.01763v3 (2026 revision) | Offline censored data; one order quantity; identification, minimax regret, finite-sample guarantees | Closest conceptual starting point. Generalizing its results requires more than adding a capacity multiplier. | Abstract and selected full-text sections inspected; proof-by-proof reproduction pending |
| Kumar and Mouchtaki, *What is the Value of Censored Data? An Exact Analysis for the Data-driven Newsvendor*, arXiv:2602.16842v2 (2026) | Exact finite-sample worst-case regret characterizations for a policy class with bounded demand | Check whether its reductions already yield the proposed extension or a stronger baseline. | Abstract and selected full-text sections inspected; detailed reduction audit pending |
| Shi, Chen and Duenyas, *Nonparametric Data-Driven Algorithms for Multiproduct Inventory Systems with Censored Demand* (2016) | Adaptive multiproduct inventory control with shared warehouse capacity | Censoring, multiple products and capacity are already studied jointly. Our initial question fixes the historical data instead of learning through subsequent actions. | Author PDF introduction and model inspected; complete comparison pending |
| Zheng, Chen, Hedenstierna and Yang, *Offline Learning and Optimization for Multi-Product Inventory Management With Stockout-Based Substitution* (2026) | Offline multiproduct estimation and optimization with substitution | Directly relevant offline prior art; its full assumptions and special cases must be checked before claiming a gap. | Publisher abstract only; full text still required |

## Primary sources

1. Hssaine and Sinclair: https://arxiv.org/abs/2412.01763v3
2. Kumar and Mouchtaki: https://arxiv.org/abs/2602.16842v2
3. Shi, Chen and Duenyas: https://congshi-research.github.io/papers/nonparametric-multi-product.Final.pdf
4. Zheng et al.: https://doi.org/10.1177/10591478261424592

## Candidate difference to investigate

The current question concerns identification and minimax regret from **fixed
offline censored observations**, with products coupled through a resource
constraint. Offline learning, capacity constraints, censored demand, robust
optimization, and multiplier-adjusted quantiles are individually established.
A useful contribution needs an explicit result that the nearest existing
theorems do not already imply.

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
