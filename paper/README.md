# Working theoretical manuscript

**Sharp overstatement of coalition savings in newsvendor relaxations**

This is a complete first draft in English, with the central theorem and proof,
the exact finite-family calculation, root and canonical-extension comparisons,
the standalone-cost condition, numerical tables, and an iid validation appendix.
It is not a submission or an independently reviewed publication.

The November 6 [mathematical addendum](../docs/exclusion_robustness.md) strengthens
the construction to continuous true laws with positive definite covariance
and supplies a separate fixed-scale example. Its
[checks](../results/exclusion/robustness.md) are complete. The current PDF and
Overleaf ZIP retain the November 5 draft; the addendum is to be integrated in
the next revision. Review the addendum alongside this draft.

## Open in Overleaf

Upload `overleaf.zip` as a new project and select `main.tex` as the main document.
Use pdfLaTeX. The archive includes the generated tables and citation subset;
Python and the rest of this repository are not needed to compile it.
The compiled reading copy is `main.pdf`.

## Build from this repository

Generate the tables and citation subset from the stored results:

```bash
python paper/build_tables.py
```

Then compile in this directory with a normal TeX Live installation:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Repeat the final command if LaTeX requests another cross-reference pass.

`build_manifest.json` records hashes of the data, source and generated tables.
`references.bib` contains only the entries cited in the manuscript; reading-depth
notes remain in the repository's root bibliography and
[source comparison](../docs/exclusion_prior_art.md).
Rebuilding the tables does not run a new experiment.
[The assembly record](assembly_report.md) lists the checks performed on this draft.

## Scope of the first draft

The main result is the exact worst-case depth/share formula for a fixed positive
allocation. The relaxation, two-state cost device and statistical principles
are credited to their precedents. The failed broad statistical precision screen
is reported alongside the conditional success and matched alternatives.

The manuscript keeps separate:

- the error of the fixed-allocation relaxation and the quality of an optimized allocation;
- bounded physical production and its Gaussian norm-cost representation;
- expected cost L and maximum declared loss A;
- a mathematical proof, numerical consistency and bibliographic priority.

The next scientific review should assess the proof and the significance of
this narrow quantitative contribution. Merely assembling or compiling the draft
does not settle either independent correctness or publication readiness.
