# Research protocol

This protocol addresses failure modes of AI-assisted research. Its purpose is to
make correctness, information assumptions and evidential limits inspectable.

## Evidence motivating the protocol

- [Luo, Kasirzadeh and Shah, PNAS (2026)](https://doi.org/10.1073/pnas.2610214123)
  examine benchmark choice, leakage, metric use and post hoc selection in two
  autonomous research systems. Their audit benefits from code and execution
  records beyond the manuscript. The constructed audit dataset includes induced
  failures; its detection accuracy is not the error rate of published AI papers.
- [Evaluating Sakana's AI Scientist](https://arxiv.org/abs/2502.14297)
  reports failures of novelty assessment, implementation and result reporting in
  a specific older system using GPT-4o. Those rates are not measurements of Astra.
- [An Astra graph-theory campaign](https://github.com/graph-theory-AI/Graph-Theory-LLM-Proofs/blob/main/verification_astra/SUMMARY.md)
  includes results flagged as publishable that a later model-based audit labels
  already known or incomplete. This is exploratory evidence, not a representative
  benchmark or independent human validation. A model review cannot certify novelty.
- [OpenAI's mathematical results](https://openai.com/index/ten-advances-in-mathematics/)
  demonstrate a reported contribution from an internal Astra version, alongside
  human manuscript preparation and formal verification. They do not establish a
  general success rate for autonomous publication.

## Controls used in this repository

1. **Separate truth from novelty.** Every central statement belongs in the claim
   register with assumptions and evidence. A correct KKT consequence remains an
   elementary result until a substantive contribution is established against
   the closest full papers.
2. **Compare equal information.** Document exactly what every method sees. The
   original A/B reference knows four complete candidate worlds; its gains cannot
   be attributed to learning hidden tails from sales. The later endpoint audit
   derives its scenarios from the population sales law and explicit ambiguity
   assumptions. Those are different information models and must be labeled.
3. **Prespecify evaluative experiments.** Before a future empirical comparison,
   record the dataset, splits, costs, capacities, metrics, baselines and decision
   rule. Exploration may change these choices, but then requires a fresh final
   holdout. Keep exploratory and confirmatory results distinguishable.
4. **Make negative results visible.** Retain all runs, failures and negative or
   negligible gains. Do not choose seeds, capacity ranges or datasets solely to
   improve the final table. State the entire tested grid and any exclusions.
5. **Link claims to execution.** Generate result tables from stored outcomes;
   retain configuration and source hashes. A passing test is reported only after
   observing its completed execution. No manually invented numerical results.
6. **Use independent checks.** Here, exact costs are compared with quadrature,
   multiplier solutions with a separate constrained optimizer, and scenario
   minimax with analytical and grid references. These tests do not validate an
   unseen forecasting pipeline or the full ambiguity class.
7. **Challenge mathematical assumptions.** Check boundary atoms, zero/slack
   capacity, heterogeneous costs and weights, and alternative tail completions.
   A finite grid is a counterexample search, not a proof. A formal proof checker,
   if introduced later, must verify the intended statement and assumptions.

## Stop or redirect criteria

- The proposed central theorem is already known or follows immediately from an
  existing result with a change of notation.
- An apparent algorithmic gain disappears under equal information, equal
  computational budgets, or independent evaluation.
- The only supporting cases are the constructed motivating instances.

In those cases, preserve the reproducible result and reconsider the research
question before expanding the implementation or drafting publication claims.
