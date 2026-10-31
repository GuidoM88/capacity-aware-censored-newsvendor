# Capacity-Aware Censored Newsvendor

Research code for **identifiability and minimax regret under censored demand and shared capacity**.

**Current investigation, 2026-10-31.** We audit the cost of leaving a coalition
after producers submit a forecast-based offer. Excluding at least one whole producer
closes the original four-producer relaxation gap. The new note proves exactness for
exchangeable production and equal shares, and constructs a persistent gap at any
fixed exclusion depth in the heterogeneous model.
[Proofs and research decision](docs/exclusion.md) · [Reproducible comparison](results/exclusion/summary.md)

Historical sales reveal `min(demand, stock)`, not necessarily demand. This project
asks when a resource constraint makes the optimal allocation identifiable even
though the unobserved demand tails remain unknown.

**Research decision, 2026-10-28:** the [three-direction comparison](docs/research_directions.md)
prioritizes a bounded investigation of **finite-data certificates for coalition
stability after forecast reconciliation**. The [first certificate note](docs/coalition_certificate.md)
now proves a baseline and identifies its fractional-coalition relaxation. A
prespecified 100-case diagnostic and independent LP/MILP checks distinguish
sampling uncertainty from structural conservatism. These results narrow the
next research target; scientific novelty is not yet established.

Retain the censored-newsvendor work as a reproducible foundation. The earlier
[computational assessment](docs/computational_prior_art.md) is a provisional
project-priority judgment, not a proof of full duplication or unpublishability.
The comparison now states the precise next hypothesis and the baselines it must
exceed before a larger implementation.

The [working derivation](docs/sparse_scenarios.md) reduces full-class regret to
`n+1` endpoint worlds for one shared resource, and to rank-bounded upper-tail
subsets for a packing polytope. Its proof, exact finite-atomic LP and independent
checks remain available as supporting material. Finite-sample guarantees and
practical forecasting contributions are not yet established.

## Initial example

Two marginal demand models are observationally indistinguishable when historical
stock is 40:

- A: uniform demand on `[0, 100]`.
- B: a mixture of `0.4 × Uniform(0, 40)` and `0.6 × Uniform(40, 160)`.

Both have CDF `F(x) = x / 100` below 40 and censored sales with an atom of mass
0.6 at 40. Two products yield four latent scenarios: AA, AB, BA, BB.
Underage costs are 4, overage costs are 1, and the resource weights are 1.

| Total capacity | Oracle allocation under AB | Oracle allocation under BA |
| ---: | ---: | ---: |
| 60 | (30, 30) | (30, 30) |
| 80 | (40, 40) | (40, 40) |
| 120 | (53.333333, 66.666667) | (66.666667, 53.333333) |

The [mathematical note](docs/formulation.md) proves that the optimal action is
identified from this population sales law exactly when capacity is at most 80,
within the stated class of nonnegative finite-mean demand distributions.
The numerical example is a check of that argument, not its proof.

![Population allocation and regret across capacities](results/toy/capacity_sweep.png)

The committed [reference results](results/toy/summary.md) cover 131 capacities
from 0 to 260. At capacity 120 the finite-scenario minimax reference has worst
regret `5/3`, while sales-as-demand has worst regret 70 over the four supplied
worlds. The fixed A-tail policy also attains `5/3` there; this single instance
does not distinguish those two policies. Information assumptions are listed below.

The separate [full-class analysis](docs/population_reduction.md) gives minimax
regret **60** at capacity 120 when every compatible demand tail is allowed.
The value `5/3` above concerns only the supplied A/B family. The population note
proves a general common-action characterization and an exact endpoint reduction;
the original A/B experiment and its saved results are unchanged.

## Reproduce

Python 3.11 or later is required; the initial run uses Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
python -m censored_newsvendor.experiment --output results/toy
```

On Windows, activate with `.venv\Scripts\activate` instead. For a quick run:

```bash
python -m censored_newsvendor.experiment --max-capacity 120 --step 20 --no-plot --output results/local/quick
```

The experiment writes all outcomes to CSV, a JSON manifest with parameters,
dependency versions and source hashes, a Markdown summary, and a figure.
No external dataset, GPU, API key, or random seed is needed for this deterministic
population experiment. `requirements.txt` pins direct dependencies; it is not a
complete transitive environment lock.

## Methods and information available

| Method | Information supplied | Role |
| --- | --- | --- |
| Oracle | True demand marginals | Unattainable reference for regret |
| Sales as demand | Exact censored sales law | Naive population baseline |
| Assume A tail | A imposed for both products | Sensitivity to a fixed tail assumption |
| Finite-scenario minimax regret | The four complete scenarios AA/AB/BA/BB | Reference under an explicitly supplied finite family |

The finite-scenario method has additional tail information. Its advantage over
sales-as-demand is **not evidence of a learned method outperforming a baseline
under equal information**. It does not optimize over every tail compatible with
censored sales. All methods are evaluated on true population expected loss, and
each scenario's oracle obeys the same capacity constraint.

The oracle solver finds the common resource multiplier and applies the adjusted
quantiles. The finite-scenario reference solves a convex epigraph problem.
Tests compare analytical losses with independent numerical integration, check
closed-form allocations, and compare solvers with independent optimization/grid
references. These checks validate this implementation within its supported scope.

## Research documents

- [Whole-producer exclusions, exactness and worst-case construction](docs/exclusion.md)

- [Baseline certificate, proofs and fractional-coalition obstruction](docs/coalition_certificate.md)
- [Prespecified certificate diagnostic protocol](docs/coalition_certificate_protocol.md)
- [Generated certificate comparison](results/certificates/summary.md)
- [Current direction selection, closest papers and checked diagnostic](docs/research_directions.md)
- [Formulation, elementary certificate, and exact toy threshold](docs/formulation.md)
- [Closest literature and unresolved overlap](docs/literature.md)
- [Originality audit and research decision](docs/novelty_audit.md)
- [General population reductions and full-class toy regret](docs/population_reduction.md)
- [Sparse-tail theorem, proof and exact LP](docs/sparse_scenarios.md)
- [Computational prior art and publication decision](docs/computational_prior_art.md)
- [Claim register](docs/claims.md)
- [Research protocol and failure controls](docs/research_protocol.md)
- [Next milestones](docs/roadmap.md)
- [Bibliography](references.bib)

Independent checks for the population reductions:

```bash
python scripts/check_population_reduction.py
python scripts/check_sparse_scenarios.py
```

This writes the [audit check report](results/audit/population_reduction.json).
It uses separate linear programs and numerical integration rather than the
production allocation and finite-scenario solvers. Its finite checks supplement
the proofs; they do not establish originality or a general theorem by themselves.
The sparse-scenario script separately compares full enumeration, the selected
worlds and a compact LP; its [generated report](results/audit/sparse_scenarios.md)
also preserves a counterexample to ignoring individual order caps.

The separate coalition-information diagnostic is reproduced with:

```bash
python scripts/check_coalition_information.py
```

Its [saved results](results/audit/coalition_information.json) check identical
individual and aggregate distributions, a blocking coalition, and the exact
common least-core tolerance `1/3`, using rational arithmetic and an independent LP.
The subsequent certificate diagnostic is reproduced with:

```bash
python scripts/check_coalition_certificate.py
```

To reproduce the subsequent exclusion comparison using the saved baseline outcomes:

```bash
python scripts/check_exclusion.py
python scripts/check_exclusion_obstruction.py
```

It compares the moment certificate with an enumeration-based confidence bound
under identical validation samples. Population LP/MILP references separately
measure structural slack and use the true finite law. The
[complete outcomes](results/certificates/results.json) preserve all 100 cases,
rules, input distributions and sampled-state counts. The mathematical confidence
guarantees assume bounded iid observations independent of the frozen rule.

The initial scope is a single-period, separable expected-loss problem. Demand
substitution, lead times, inventory carry-over, contextual forecasting, and time
dependence are not represented in the current implementation. Independence across
products is not needed for the separable expected-cost objective; the example can
use independent products to construct identical joint observation laws.
