# Zenodo Upload Notes for LSC 6.2.0

## Published Action

This package was published using Zenodo's **New version** workflow from the existing LSC 6.0 conceptual record:

https://zenodo.org/records/19780616

Published record:

https://zenodo.org/records/19878587

Version DOI:

https://doi.org/10.5281/zenodo.19878587

Do not create a detached standalone record unless a future workflow explicitly requires it.

## Why

This preserves research continuity for grant review:

```text
LSC 4.2 -> LSC 5.x -> LSC 6.0 -> LSC v1.2.0 reproducibility update -> LSC 6.2.0 preprint
```

## Suggested Title

LSC 6.2.0: A Phenomenological Framework for Neutrino Propagation and Detector-Frame Tensor Anisotropy

## Suggested Version

6.2.0-preprint

## Suggested Publication Type

Preprint

## Suggested Description

Use `metadata/zenodo.json`.

## arXiv Note

Include this sentence in the description:

```text
The work is prepared for arXiv submission and is currently awaiting category endorsement.
```

## Related Identifiers

Recommended:

- `isNewVersionOf`: https://doi.org/10.5281/zenodo.19780616
- `isSupplementedBy`: https://doi.org/10.5281/zenodo.19843361
- `isSupplementTo`: https://github.com/luciferprosun/LSC-6.0
- `isDerivedFrom`: https://doi.org/10.5281/zenodo.19602045

## Files to Upload

The published record includes:

- `paper/LSC_6_2_0_preprint.pdf`
- `source/LSC_6_2_0_arxiv_source.zip`
- `source/main.tex`
- `figures/LSC_6_2_0_model_map.png`
- `README.md`
- `CHANGELOG_LSC_6_2_0.md`
- `BUILD_LOG.md`
- `SOURCE_NOTES.txt`
- `metadata/zenodo.json`
- `metadata/CITATION.cff`
