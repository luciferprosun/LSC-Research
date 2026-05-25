---
title: "Kodeks 1015 - LSC Step 3 Review Package"
date: "2026-05-25"
toc: true
toc-depth: 3
geometry: margin=2cm
fontsize: 10pt
---

# Executive Summary

This report consolidates STEP 3 of the LSC Pre-BEST-2 Freeze Program for human review before STEP 4.

STEP 3 is implementation and archival engineering only. It does not extend LSC, create new physics, create new equations, create new tensor structures, create new particle claims, or create LSC 6.4.

The Step 3 output answers:

> What exact infrastructure, datasets, templates, procedures, and archival structures are required to execute the frozen framework without introducing post-hoc theory drift?

## Step 3 Output Status

| Area | Status |
|---|---|
| Dataset matrix | created |
| M0-M6 templates | created |
| M4 detector/systematics schema | created |
| Covariance placeholder policy | created |
| Sensitivity-analysis structure | created |
| LOO protocol | created |
| Cross-experiment transfer protocol | created |
| External veto data request checklist | created |
| BEST-2 preregistration form | created |
| Archive structure plan | created |
| GitHub push | not performed |
| Zenodo upload | not performed |

# Data Requirement Matrix

| Resource | Availability | Machine-readable | Covariance | Extraction-level | Orientation/timestamp | Exposure-level | Relevance | Class |
|---|---|---|---|---|---|---|---|---|
| BEST | summary local | partial | unavailable | unavailable | unavailable | unavailable | primary two-zone validation | ESSENTIAL |
| GALLEX | summary local | partial | unavailable | unavailable | unavailable | incomplete | transfer validation | IMPORTANT |
| SAGE | summary local | partial | unavailable | unavailable | unavailable | incomplete | transfer/isotope validation | IMPORTANT |
| BEST-2 | future/planned | unavailable | unavailable | unavailable | unavailable | unavailable | decisive preregistered validation | ESSENTIAL / CURRENTLY UNAVAILABLE |
| KATRIN | literature public | not integrated | not integrated | N/A | N/A | N/A | energy-response veto | ESSENTIAL |
| IceCube | literature public | not integrated | not integrated | N/A | N/A | N/A | anisotropy / SME-style veto | ESSENTIAL if tensor physical/celestial |
| Solar constraints | literature public | not integrated | not integrated | N/A | N/A | N/A | universal-response veto | IMPORTANT |
| SME/Lorentz literature | literature public | not integrated | not integrated | N/A | N/A | N/A | tensor-background veto | ESSENTIAL if tensor physical/celestial |
| Detector calibration/systematics literature | partial | not consolidated | unavailable | unavailable | unavailable | unavailable | M4 construction | ESSENTIAL |

## Required Future Fields

- source activity calibration;
- source position and source extension;
- zone geometry;
- extraction-by-extraction tables;
- counter efficiencies;
- background model;
- statistical covariance;
- systematic covariance;
- detector orientation;
- exposure timestamps;
- environmental logs;
- machine-readable baseline predictions.

# M0-M6 Specification Templates

| Model | Purpose | Allowed Freedoms | Forbidden Freedoms | Required Comparisons |
|---|---|---|---|---|
| M0 | published/null baseline | documented published inputs | hidden normalization tuning | all models vs M0 |
| M1 | scalar normalization only | one preregistered scale/nuisance term | zone/tensor behavior | M1 vs M5/M6 |
| M2 | cross-section/source systematics | literature-supported source/cross-section uncertainty | arbitrary post-hoc source shifts | M2 vs M5/M6 |
| M3 | sterile-neutrino benchmark | fixed literature benchmark or preregistered scan | omission from final comparison | M3 vs M5/M6 |
| M4 | detector-systematics benchmark | physically motivated detector/systematics terms | optional treatment | M4 vs M5/M6 |
| M5 | LSC trace-only | preregistered scalar template | directional/tensor terms | M5 vs M1/M2/M4/M6 |
| M6 | LSC trace + traceless anisotropy | frozen trace/traceless template only | post-hoc tensor orientation or added terms | M6 vs M0-M5 |

Allowed claims are restricted to exploratory or validation-grade statements depending on covariance/data completeness. Discovery, sterile-exclusion and confirmed-new-physics claims remain prohibited.

# Full M4 Detector/Systematics Implementation Schema

M4 is the full detector/systematics competitor. It must be implemented before M6 preference can be claimed.

```yaml
model_id: M4
model_name: detector_systematics_baseline
validation_grade: NON-VALIDATION-GRADE until covariance and metadata are complete
components:
  calibration_drift: {}
  source_normalization_uncertainty: {}
  detector_geometry_asymmetry: {}
  extraction_efficiency_asymmetry: {}
  environmental_background_drift: {}
  covariance_incompleteness: {}
  timing_artifacts: {}
  orientation_artifacts: {}
  background_subtraction_uncertainty: {}
outputs:
  predicted_ratios: []
  nuisance_parameters: []
  covariance_assumptions: []
  comparison_scores: []
```

## M4 Component Table

| Component | Required Inputs | Sensitivity Hooks |
|---|---|---|
| calibration drift | calibration run, timestamp, calibration value, uncertainty | drift scan, time split |
| source normalization | source activity, uncertainty, method, isotope | source scale scan, isotope split |
| geometry asymmetry | geometry file, source position, zone boundaries, dead volume map | geometry perturbation, source shift |
| extraction efficiency | extraction ID, zone ID, efficiency, uncertainty | zone efficiency scan, run-by-run test |
| environmental drift | timestamp, temperature, pressure, radon, electronics state | environmental regression, day/night split |
| covariance incompleteness | covariance matrix, source, missing-correlation policy | diagonal vs correlated, conservative envelope |
| timing artifacts | exposure start/end, extraction time, counting time | time scramble, exposure phase split |
| orientation artifacts | azimuth, tilt, latitude, longitude, source orientation | lab vs celestial test, orientation scramble |
| background subtraction | background rate, uncertainty, model, run ID | background scale scan, background-only validation |

# Covariance Placeholder Policy

All placeholder covariance outputs must be labeled:

```text
NON-VALIDATION-GRADE
```

Allowed placeholders:

- diagonal covariance from published summary uncertainties;
- block-diagonal covariance by experiment;
- conservative correlated-error envelope;
- source-normalization correlation envelope;
- cross-section shared uncertainty envelope.

Forbidden:

- treating placeholders as final covariance;
- using placeholders for discovery, exclusion or strong preference claims;
- suppressing missing-covariance caveats.

# Sensitivity-Analysis Structure

Every exploratory run must compare:

| Sensitivity Variant | Purpose |
|---|---|
| diagonal errors | baseline placeholder |
| high-correlation envelope | conservative correlation stress test |
| low-correlation envelope | lower-bound correlation stress test |
| source-normalization shared shift | M2/M4 source mimicry |
| cross-section shared shift | M2 cross-section mimicry |
| zone-correlated extraction shift | M4 extraction asymmetry mimicry |

Each output must list missing covariance fields, affected model comparisons, blocked claims, sensitivity to placeholder choice and validation grade.

# Leave-One-Out Execution Protocol

## Required Omissions

| Omission | Prediction Target |
|---|---|
| BEST inner | BEST inner |
| BEST outer | BEST outer |
| BEST ratio | BEST ratio |
| GALLEX combined | GALLEX combined |
| GALLEX Cr1 | GALLEX Cr1 |
| GALLEX Cr2 | GALLEX Cr2 |
| SAGE 51Cr | SAGE 51Cr |
| SAGE 37Ar | SAGE 37Ar |
| BEST group | BEST group |
| GALLEX group | GALLEX group |
| SAGE group | SAGE group |

## Execution Flow

```text
load frozen model
load dataset and covariance status
select omission target
fit/evaluate on remaining data
predict omitted target
record residual and uncertainty
record parameter changes
repeat for M0-M6
compare penalty-adjusted performance
classify stability
```

## Stability Classes

- stable;
- weakly stable;
- unstable;
- non-identifiable;
- non-validation-grade.

# Cross-Experiment Transfer Protocol

| Fit Source | Prediction Target |
|---|---|
| BEST | GALLEX |
| BEST | SAGE |
| GALLEX/SAGE | BEST |
| 51Cr sources | 37Ar source |
| BEST/GALLEX/SAGE | future BEST-2 |
| BEST inner | BEST outer |
| BEST outer | BEST inner |

Transfer is valid only if mapping is frozen before fitting, geometry differences are documented, isotope/source differences are documented, covariance limitations are stated, M0-M6 are evaluated under the same transfer and no target-specific retuning is allowed.

# External Veto Data Request Checklist

| Veto | Exact Data Required | Why It Matters | Constrains |
|---|---|---|---|
| KATRIN | energy-response constraints, beta-spectrum systematics | tests universal energy-response distortions | trace response |
| IceCube | anisotropy/Lorentz/SME-related bounds | tests physical/celestial tensor interpretations | traceless/tensor response |
| SME/Lorentz literature | coefficient bounds, mapping rules | prevents hidden Lorentz conflict | tensor-background interpretation |
| solar-neutrino fits | solar Gallium and global constraints | tests universal response consistency | scalar/trace response |
| standard oscillation constraints | three-flavor fits and sterile benchmarks | maintains compatibility with known oscillations | survival/transition behavior |
| detector calibration literature | source activity, cross-section, extraction, counter efficiency, background uncertainty | powers M2 and M4 | trace and detector/systematics mimicry |

# BEST-2 Preregistration Form

The preregistration form requires:

- project identity;
- frozen equations copied verbatim from Step 1;
- frozen parameter structure;
- frozen datasets;
- frozen M0-M6 hierarchy;
- prohibited post-hoc actions;
- allowed statistical interpretations;
- failure conditions;
- publication discipline.

Prohibited post-hoc actions:

- adding mechanisms;
- adding equations;
- adding tensor structures;
- changing tensor orientation after data inspection;
- suppressing covariance limitations;
- dropping M4;
- dropping M3;
- changing success/failure criteria;
- using AI consensus as evidence.

# Freeze Archive Structure Plan

```text
LSC_FREEZE_PACKAGE/
  README.md
  MANIFEST.csv
  CHECKSUMS.sha256
  canonical/
  validation/
  implementation/
  audits/
    original/
    extracted/
  sources/
    source_inventory.csv
    zenodo_metadata/
  reports/
    PDFs/
  provenance/
```

The archive must preserve:

- Step 1 canonicalization decisions;
- Step 2 validation rules;
- Step 3 implementation templates;
- original audits;
- extracted audit text;
- Zenodo metadata;
- source repository references;
- checksum manifest.

# Remaining Blockers

- final freeze package not assembled;
- final manifest and checksums not generated for the freeze package;
- release notes not drafted;
- Zenodo metadata draft not prepared;
- human review not completed;
- no approval for GitHub or Zenodo publication.

# Remaining Missing Data

- BEST full covariance;
- BEST extraction-by-extraction table;
- BEST counter efficiencies;
- BEST orientation/timestamp metadata;
- GALLEX exposure-level data;
- SAGE run-by-run source data;
- KATRIN machine-readable constraints;
- IceCube/SME tensor-bound mappings;
- solar-neutrino fit tables;
- detector calibration/systematics literature in machine-readable form.

# Remaining External Constraints

- KATRIN energy-response veto;
- IceCube anisotropy/tensor bounds;
- SME/Lorentz-style tensor constraints;
- solar-neutrino consistency;
- standard oscillation global fits;
- detector calibration and gallium cross-section constraints.

# Final Freeze Readiness Assessment

| Readiness Area | Status |
|---|---|
| canonical core | ready from Step 1 |
| validation infrastructure | ready from Step 2 |
| implementation templates | ready from Step 3 |
| final local archive package | not yet assembled |
| manifest/checksums | not yet generated for final package |
| release metadata | not yet drafted |
| human review | pending |
| publication | prohibited until reviewed |

Freeze readiness status:

```text
READY FOR STEP 4 LOCAL PACKAGE ASSEMBLY
NOT READY FOR PUBLIC RELEASE
```

# Final Recommendations Before STEP 4

STEP 4 should:

1. Assemble final local freeze package.
2. Copy canonical, validation and implementation documents into final structure.
3. Copy original and extracted audits.
4. Copy master PDFs and source inventory.
5. Generate `MANIFEST.csv`.
6. Generate `CHECKSUMS.sha256`.
7. Draft GitHub release notes without publishing.
8. Draft Zenodo metadata without uploading.
9. Create final local ZIP for human review.
10. Verify all placeholders remain `NON-VALIDATION-GRADE`.

