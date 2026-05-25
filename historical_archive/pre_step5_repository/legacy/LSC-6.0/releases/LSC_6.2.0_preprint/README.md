# LSC 6.2.0 Preprint Package

Title:

**LSC 6.2.0: A Phenomenological Framework for Neutrino Propagation and Detector-Frame Tensor Anisotropy**

## Status

This is the latest preprint-stage version of the LSC research line.

The package has been published on Zenodo as a new version under the LSC concept DOI and is prepared for arXiv submission. The arXiv submission process is currently waiting for category endorsement, so the Zenodo record should be used as the stable citable preprint record while endorsement is pending.

Published Zenodo record:

https://zenodo.org/records/19878587

Version DOI:

https://doi.org/10.5281/zenodo.19878587

arXiv endorsement request:

https://arxiv.org/auth/endorse?x=7KLAMS

## Recommended Zenodo Strategy

Published continuity option:

This package was published as a **new version of the existing LSC 6.0 conceptual record**, not as a detached new project.

Base record:

- LSC 6.0 record: https://zenodo.org/records/19780616
- DOI: https://doi.org/10.5281/zenodo.19780616
- Concept DOI: https://doi.org/10.5281/zenodo.19780615

Reason:

- LSC 6.2.0 is explicitly a continuation of the LSC 6.0 phenomenological framework.
- The new work extends the model rather than replacing the public archive.
- Grant reviewers can see one continuous research line: LSC 4.2 -> LSC 5.x -> LSC 6.0 -> LSC v1.2.0 reproducibility update -> LSC 6.2.0 preprint.
- Zenodo versioning preserves continuity while assigning the 6.2.0 preprint its own version DOI: https://doi.org/10.5281/zenodo.19878587.

## Scientific Framing

LSC 6.2.0 is not presented as confirmed new physics.

It is a phenomenological ansatz intended for independent review, numerical fitting and falsification. The main update is a detector-frame tensor anisotropy model that separates propagation effects from detector-level energy reconstruction.

## Conceptual Changes Since LSC 6.0

- Keeps the conservative LSC 6.0 propagation/reconstruction framing.
- Adds an explicit rank-2 detector-frame tensor `D_ij`.
- Separates true propagation energy from reconstructed detector energy.
- Defines the detector response:

```text
E_rec = E_true [1 + alpha_D D_ij p^i p^j]
```

- Uses a traceless anisotropy parameterization:

```text
D_ij = delta (n_i n_j - delta_ij / 3)
```

- Defines null recovery:

```text
D_ij -> 0
delta_G -> 0
```

- Maps the model to test classes:
  - angular anisotropy,
  - detector dependence,
  - energy-dependent residuals,
  - sidereal modulation.

- Identifies validation targets:
  - BEST / GALLEX / SAGE gallium source data,
  - KATRIN beta-spectrum constraints,
  - IceCube anisotropy and detector-systematic studies,
  - standard three-flavor oscillation limits.

## Files

```text
paper/
  LSC_6_2_0_preprint.pdf

source/
  main.tex
  LSC_6_2_0_arxiv_source.zip

figures/
  LSC_6_2_0_model_map.png
  LSC_6_2_0_social_preview.png

metadata/
  zenodo.json
  CITATION.cff
  ZENODO_UPLOAD_NOTES.md

BUILD_LOG.md
SOURCE_NOTES.txt
CHANGELOG_LSC_6_2_0.md
README.md
```

## Recommended Public Wording

Short version:

> LSC 6.2.0 is the latest preprint-stage continuation of the LSC 6.0 phenomenological framework. It introduces detector-frame tensor anisotropy as a testable reconstruction-level ansatz. The work is not presented as confirmed new physics and is awaiting arXiv endorsement for formal submission.

Grant-facing version:

> LSC 6.2.0 extends the public LSC 6.0 record into an arXiv-ready preprint with explicit mathematical separation between propagation effects and detector-frame reconstruction anisotropy. The package provides a citable continuity point for grant review while the formal arXiv submission awaits category endorsement.
