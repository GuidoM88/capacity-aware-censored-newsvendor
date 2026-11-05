Sharp overstatement of coalition savings in newsvendor relaxations
Guido Morgante — working draft, 5 November 2026

Upload overleaf.zip as a new Overleaf project. Select main.tex as the main
document and pdfLaTeX as the compiler. The tables and references are included;
Python, the numerical solver and the rest of the repository are not required.

For a local TeX Live build:
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
  bibtex main
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
Repeat the final command if LaTeX requests another cross-reference pass.

This is a complete first draft for mathematical and scientific review.
Compilation and numerical consistency do not establish independent correctness,
bibliographic priority or suitability for a particular publication venue.

The private research repository contains the protocols, full stored outcomes,
source-reading records and table generator:
https://github.com/GuidoM88/capacity-aware-censored-newsvendor
