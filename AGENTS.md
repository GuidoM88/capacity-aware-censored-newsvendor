# Repository guidance

Keep code and research documentation in English. Read `docs/claims.md` before
changing scientific claims and `docs/research_protocol.md` when designing or
interpreting experiments. Do not treat numerical examples or model self-review
as proofs of general validity, novelty, or publishability.

The local tests and toy experiment use disposable synthetic inputs and no
external services. Run affected checks and fix implementation failures without
requesting approval for each iteration. Preserve all relevant negative results.

Validation commands:

```bash
python -m unittest discover -s tests -v
python -m censored_newsvendor.experiment --output results/toy
```

Generate result summaries from saved outcomes. Update the claim register when
evidence changes, and keep finite-scenario assumptions separate from guarantees
over all compatible demand tails.
