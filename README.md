# LSC Research - Pre-BEST-2 Freeze Repository

## Status

This repository is the canonical LSC freeze-stage repository for the pre-BEST-2 era.

LSC is preserved here as an unvalidated, constrained phenomenological validation framework for studying Gallium/BEST-style neutrino anomaly structures against conventional baselines, detector/systematics competitors, sterile-neutrino comparisons, and external constraints.

This repository is frozen before BEST-2-era analysis to prevent post-hoc theory drift.

## Authorship

Freeze-stage authorship:

- LuciferSun
- flAmeBorn

Older collaborator or creator names may remain inside `historical_archive/` only as provenance-preserved historical metadata.

## Claim Boundary

This repository does not claim:

- confirmed new physics;
- discovery of a new particle;
- exclusion of sterile-neutrino explanations;
- exclusion of detector or systematics explanations;
- validation of a BEST-2 prediction;
- AI model agreement as scientific evidence.

Negative outcomes are valid outcomes. If detector/systematics models reproduce LSC-level structures with equal or better penalized performance, LSC is not distinguishable.

## Freeze Philosophy

The pre-BEST-2 freeze exists to preserve a testable, auditable state before future data appear. The active framework is limited to:

- canonical concepts separated during STEP 1;
- validation infrastructure specified during STEP 2;
- implementation and archival templates specified during STEP 3;
- final local release-preparation materials assembled during STEP 4;
- repository closure and freeze engineering performed during STEP 5.

No new equations, mechanisms, tensor structures, or discovery claims should be added inside this freeze-stage repository without explicit post-freeze classification and changelog entries.

## Validation Philosophy

The repository treats LSC as one model class in an M0-M6 comparison hierarchy:

| Model | Role |
|---|---|
| M0 | Null/no-anomaly comparator |
| M1 | Normalization-only comparator |
| M2 | Cross-section/systematics comparator |
| M3 | Sterile-neutrino comparator |
| M4 | Detector/systematics competitor |
| M5 | Hybrid or nuisance-extended comparator |
| M6 | LSC-specific phenomenological model |

The M4 detector/systematics baseline remains a primary competitor. Missing covariance-grade datasets block full likelihood validation.

## Repository Layout

| Path | Purpose |
|---|---|
| `canonical/` | Active canonical LSC core, active equation set, freeze boundary, historical lineage summary. |
| `validation/` | Validation protocol, M0-M6 hierarchy, M4 baseline, covariance policy, external veto checklist, preregistration policy, risk matrix. |
| `implementation/` | Data requirement matrix, M0-M6 templates, M4 schema, covariance placeholder templates, leave-one-out protocol, transfer protocol, BEST-2 preregistration form. |
| `freeze_release/` | Release notes draft, Zenodo metadata draft, request/freezing documents, final GitHub freeze checklist, pre-BEST-2 freeze statement. |
| `audits/` | External audits and Codex STEP 1-4 reports used as criticism and constraint layers. |
| `provenance/` | Source inventory, migration plan, duplicate report, manifests, checksums, pre-migration tree/hash records. |
| `docs/` | Human-readable repository guides and authority documents. |
| `data_requirements/` | Missing-data requests and data limitations needed for validation. |
| `historical_archive/` | Pre-STEP5 repository state, deprecated components, old speculative material, legacy PBH/curvature material, noncanonical history. |
| `tools/` | Helper scripts for manifest/checksum maintenance if needed. |

## Missing Data Blocking Full Validation

Full likelihood validation remains blocked by missing or incomplete:

- covariance matrices;
- extraction-level data;
- orientation/timestamp metadata;
- exposure-level data;
- calibration/systematics data;
- KATRIN, IceCube, SME/Lorentz, solar-neutrino, and standard oscillation constraint mappings.

Placeholder covariance structures are non-validation-grade.

## External Audits

External reviews from Claude, Gemini, DeepSeek, Kimi, and reconnaissance material are included as audit and criticism layers. They are not treated as evidence for LSC and are not used to expand the theory.

## Release and Zenodo Status

This repository is prepared for GitHub freeze-stage review. No Zenodo upload is performed here. A later Zenodo archival snapshot should occur only after human review of:

- claim language;
- licensing;
- authorship and affiliation metadata;
- citation metadata;
- checksums and manifest;
- external-source references.

## How to Review

Recommended review order:

1. `canonical/LSC_CANONICAL_CORE.md`
2. `canonical/LSC_FREEZE_BOUNDARY.md`
3. `validation/LSC_VALIDATION_PROTOCOL.md`
4. `validation/LSC_M4_DETECTOR_SYSTEMATICS_BASELINE.md`
5. `implementation/LSC_DATA_REQUIREMENT_MATRIX.md`
6. `freeze_release/FINAL_GITHUB_FREEZE_CHECKLIST.md`
7. `provenance/MANIFEST.csv` or root `MANIFEST.csv`
8. `CHECKSUMS.sha256`

## LSC Evidence Chain

The complete repository is bound by an append-only, file-level SHA-256
evidence chain and checked in CI. See
[the evidence protocol](evidence-chain/README.md) and
[research attribution boundary](RESEARCH_ATTRIBUTION.md). The chain supplements
the existing freeze manifests and DOI records; it does not change the MIT
license or turn chronology into scientific validation.
