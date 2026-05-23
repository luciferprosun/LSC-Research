# Version History

## LSC 4.2

Public archival line begins with LSC 4.2:

- DOI: https://doi.org/10.5281/zenodo.19602045
- Role: propagation-side formalism, effective Hamiltonian language, weak phase modulation, relativistic energy mapping.

Additional historical documentation and earlier theory notes are maintained at:

- https://www.facebook.com/ProximaCentauri333

## LSC 5.5

LSC 5.5 introduced the detector-response direction:

- tensor-style detector response,
- Gallium anomaly interpreted through reconstruction effects,
- archived locally in `archive/LSC55_FINAL_ARCHIVE_2026-04-25.zip`.

## LSC 6.0

LSC 6.0 is the clean phenomenological version:

- removes compact-object assumptions from the Gallium interpretation,
- separates propagation and detector response,
- treats the detector tensor as phenomenological,
- links to the previous LSC 4.2 public DOI,
- prepares the line for future arXiv-style development.

Public records:

- Working paper DOI: https://doi.org/10.5281/zenodo.19780616
- Concept DOI: https://doi.org/10.5281/zenodo.19780615
- Software DOI: https://doi.org/10.5281/zenodo.19785745

## LSC v1.2.0

LSC v1.2.0 is the computational and reproducibility update:

- adds reproducible Python scripts,
- adds generated diagnostic figures,
- adds Zenodo and citation metadata,
- documents arXiv submission status,
- keeps conservative scientific interpretation.

Public record:

- DOI: https://doi.org/10.5281/zenodo.19843361

## LSC 6.2.0

LSC 6.2.0 is the latest preprint-stage continuation of the LSC 6.0 framework.

Core update:

- introduces an explicit detector-frame rank-2 tensor `D_ij`,
- separates propagation-level true energy from detector-level reconstructed energy,
- defines `E_rec = E_true [1 + alpha_D D_ij p^i p^j]`,
- uses a traceless anisotropy form `D_ij = delta(n_i n_j - delta_ij/3)`,
- defines null recovery through `D_ij -> 0` and `delta_G -> 0`,
- maps the model to angular anisotropy, detector dependence, energy residuals, and sidereal modulation tests.

Validation targets:

- BEST / GALLEX / SAGE gallium source experiments,
- KATRIN beta-spectrum constraints,
- IceCube anisotropy and detector-systematic studies,
- standard three-flavor oscillation limits.

Status:

- Zenodo preprint DOI: https://doi.org/10.5281/zenodo.19878587
- Zenodo record: https://zenodo.org/records/19878587
- arXiv-ready package included under `releases/LSC_6.2.0_preprint/`
- arXiv category endorsement pending
- not presented as confirmed new physics
