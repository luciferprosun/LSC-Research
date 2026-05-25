# LSC Pre-BEST-2 Final Freeze Archive

## Archive Status

This directory is a local release-candidate archive for the LSC Pre-BEST-2 freeze package. It is prepared for human review, GitHub release preparation, Zenodo archival preparation, reproducibility preservation, provenance preservation, and future BEST-2-era validation continuity.

No publication, GitHub release, Git push, or Zenodo upload is performed by this archive assembly step.

## What LSC Is

LSC is treated here as a constrained phenomenological validation framework for studying whether structured deviations in Gallium/BEST-style neutrino source experiments can be tested against conventional baselines, detector/systematics competitors, and external constraints.

The archive preserves the frozen pre-BEST-2 state: canonical concepts, active equations as already classified, validation hierarchy, data requirements, preregistration discipline, and failure conditions.

## What LSC Is Not

This archive does not claim:

- confirmed new physics;
- discovery of a new particle;
- exclusion of sterile-neutrino explanations;
- exclusion of detector/systematics explanations;
- a validated BEST-2 prediction;
- a completed global likelihood analysis.

## Freeze Philosophy

The freeze exists to prevent post-hoc theory drift before BEST-2-era analysis. The framework is frozen around:

- the canonical core separated in STEP 1;
- the validation infrastructure specified in STEP 2;
- the implementation and archival engineering templates specified in STEP 3;
- explicit limits on claims, tuning, and retrospective reinterpretation.

Future changes require new data, a changelog, and clear classification as either validation, correction, supplement, or post-freeze extension. New mechanisms, new equations, new tensor structures, and new discovery claims are outside the freeze package.

## Validation Philosophy

LSC must be evaluated against the full M0-M6 hierarchy:

| Model | Role |
|---|---|
| M0 | Null/no-anomaly comparator |
| M1 | Normalization-only comparator |
| M2 | Cross-section/systematics comparator |
| M3 | Sterile-neutrino comparator |
| M4 | Detector/systematics competitor |
| M5 | Hybrid or nuisance-extended comparator |
| M6 | LSC-specific phenomenological model |

M4 is a primary competitor. If M4 reproduces the same structures as M6 with comparable or better penalized performance, LSC is not distinguishable.

## Known Limitations

- Full likelihood validation is blocked without covariance-grade datasets.
- Extraction-level, orientation, timestamp, exposure-level, and calibration metadata remain incomplete or unavailable.
- External constraints from KATRIN, IceCube, solar neutrino fits, standard oscillation fits, and SME/Lorentz-style searches require formal mapping.
- Tensor freedom, detector/systematics degeneracy, overfitting, and identifiability risks remain active.
- Placeholder covariance structures are non-validation-grade.

## Missing Datasets

The request-for-data package lists required access to:

- covariance matrices;
- extraction-level data;
- orientation/timestamp metadata;
- exposure-level data;
- source and calibration/systematics data;
- KATRIN/IceCube constraint mappings;
- solar-neutrino and standard oscillation constraint tables.

## External Constraints

Publication confidence requires explicit external-veto review against:

- KATRIN;
- IceCube;
- SME/Lorentz-style tensor bounds;
- solar neutrino consistency;
- standard oscillation fits;
- detector calibration/systematics literature.

## Why Freeze Before BEST-2

The framework is frozen before BEST-2 to preserve testability. BEST-2-era outcomes should confront a documented, preregistered structure rather than a theory adjusted after seeing new data.

## Archive Navigation

| Folder/File | Purpose |
|---|---|
| `LSC_FINAL_FREEZE_PACKAGE/canonical/` | STEP 1 canonical core, active equations, freeze boundary, deprecated components, lineage. |
| `LSC_FINAL_FREEZE_PACKAGE/validation/` | STEP 2 validation protocol, M4 baseline, covariance policy, veto checklist, preregistration policy, risk matrix. |
| `LSC_FINAL_FREEZE_PACKAGE/implementation/` | STEP 3 implementation templates, data matrices, schemas, preregistration form, archive structure plan. |
| `LSC_FINAL_FREEZE_PACKAGE/audits/` | External audit originals and extracted text. |
| `LSC_FINAL_FREEZE_PACKAGE/master_context/` | Master context package, source inventory, claims table, missing-data checklist. |
| `LSC_FINAL_FREEZE_PACKAGE/source_refs/` | Repository authority files and Zenodo metadata snapshots. |
| `LSC_ZENODO_METADATA_DRAFT.json` | Draft metadata for future Zenodo deposit. |
| `LSC_REQUEST_FOR_DATA_ACCESS.md` | Formal data-access request checklist. |
| `LSC_SOURCE_AND_PROVENANCE_MANIFEST.csv` | File-level provenance manifest. |
| `CHECKSUMS.sha256` | Integrity checksums for the package. |
| `FINAL_FREEZE_REVIEW_CHECKLIST.md` | Human-review checklist before publication. |

