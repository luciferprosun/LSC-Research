LSC arXiv source package

Main file:
  main.tex

Included reproducibility files:
  data/gallium_source_summary.csv
  data/best_extraction_rates.csv
  data/data_notes.md
  scripts/validate_gallium_toy.py
  outputs/model_comparison.csv
  outputs/model_parameters.csv
  outputs/residuals.csv
  outputs/validation_summary.md

Build command:
  pdflatex main.tex
  bibtex main
  pdflatex main.tex
  pdflatex main.tex

Reproduce toy validation:
  python3 scripts/validate_gallium_toy.py

Notes:
  - This is a conservative methodology draft, not a discovery claim.
  - The toy validation now reports AICc and a leave-one-out stress metric in addition to chi2/AIC.
  - The bibliography output main.bbl should be included in the arXiv upload zip.
  - Do not upload temporary files such as .aux, .log, .out, .blg, or the generated PDF.
  - The private phone number is intentionally not included in the public manuscript.
  - SAGE and extraction-level values should be manually source-checked before a strong statistical claim.
