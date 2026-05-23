# LSC Framework v1.2.0

This is an incremental release of the LSC framework focused on computational modeling, reproducibility, and preprint preparation.

The release documents:

- current model state,
- computational extension,
- numerical evaluation of the LSC potential,
- resonance-condition diagnostic figures,
- arXiv submission status,
- Zenodo-ready metadata.

Project website:

https://luciferprosun.github.io/akasha-chronicles

## Contents

```text
paper/
  LSC_v1.2.0.pdf
  LSC_v1.2.0.tex
updates/
  CHANGELOG.md
  RELEASE_NOTES.md
code/
  simulation.py
  plot_results.py
figures/
  lsc_potential.png
  resonance_plot.png
metadata/
  zenodo_metadata.json
  CITATION.cff
README.md
```

## Run Simulation

From the release root:

```bash
python3 code/simulation.py
```

This writes numerical output to:

```text
code/simulation_output.json
```

## Reproduce Plots

From the release root:

```bash
python3 code/plot_results.py
```

This regenerates:

```text
figures/lsc_potential.png
figures/resonance_plot.png
```

## Compile Paper

From the `paper/` directory:

```bash
pdflatex LSC_v1.2.0.tex
pdflatex LSC_v1.2.0.tex
```

## arXiv Status

arXiv submission is in progress. The submission is currently awaiting endorsement for category access.

Direct endorsement link:

https://arxiv.org/auth/endorse?x=7KLAMS

## Scientific Status

This release is a phenomenological and computational research package. It is not presented as confirmed new physics. The purpose is reproducibility, independent review, and falsifiability.
