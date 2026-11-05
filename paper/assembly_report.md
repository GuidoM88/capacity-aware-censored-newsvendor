# Manuscript assembly record

2026-11-05. Scope: assemble the existing theoretical argument and stored evidence
into a complete English working manuscript. No new sampling or LP experiment
was performed during assembly.

## Deliverables

- `main.tex`: complete argument, proofs, limitations and statistical appendix.
- `main.pdf`: compiled 10-page reading copy, including 12 cited references.
- `overleaf.zip`: self-contained source, bibliography, two generated tables and
  compilation instructions.
- `build_tables.py` and `build_manifest.json`: regeneration and SHA-256 records
  linking the manuscript tables to saved outcomes and sources.

## Completed checks

1. Rebuilt both tables from the saved JSON records. Checked the 18 deterministic
   laws, all 84 depth values against their stored LP values, 18 root comparisons,
   the recorded count of 1,968 norm-cost identity points, and the standalone
   subgroup and detection counts used by the manuscript.
2. Recovered the original `results/exclusion/prior_art_checks.json` after the
   environment returned. Its three source hashes match the current script and
   implementation files. This preserves the original run; it does not claim
   that those LPs were rerun during assembly.
3. Compiled with pdfLaTeX and BibTeX until there were no LaTeX warnings,
   unresolved citations or references, or overfull/underfull box reports.
   The PDF has 31 unique resolved labels and embedded scalable fonts.
4. Rendered and visually inspected every page, including the equations, both
   numerical tables and bibliography. Checked extracted text and page count.
5. Extracted the Overleaf ZIP into an empty directory and compiled it there
   using only its contents. That build also completed without LaTeX warnings
   or unresolved references. Every archived source matches its repository copy.
6. Preserved all pre-existing numerical results and production code. Updated
   the research status, outline, claim cross-reference and historical recovery
   record to point to the assembled manuscript.

## Scientific scope unchanged

The central result is C30: the exact supremum of the fixed-allocation exclusion
gap relative to expected grand-offer cost. The finite-family calculation,
strict integer stability and forecast realization are proved in the draft.
The root relaxation is credited to its predecessor; the Gaussian embedding
is distinguished from bounded physical production. The vanishing ratio of
expected to maximum declared loss is explicit.

The conditional detection success and broad precision failure are both retained.
The tests are implementation evidence, not proof or priority verification.
Internal review and successful compilation do not establish independent
correctness, novelty, significance or submission readiness. C7 remains open.
