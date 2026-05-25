---
title: "Kodeks STEP3 Implementation And Archival Engineering"
date: "2026-05-25"
toc: true
toc-depth: 3
geometry: margin=2cm
fontsize: 10pt
---

# Executive Summary

STEP 3 creates the implementation and archival engineering layer required before final freeze archival, Zenodo release preparation, BEST-2 preregistration and future validation execution.

No theory expansion was performed:

- no new physics;
- no new equations;
- no new tensor structures;
- no new mechanisms;
- no new particle claims;
- no LSC 6.4.

All structures are implementation artifacts for the already frozen Step 1 and Step 2 framework.

# Implementation Architecture

The Step 3 package defines:

- dataset requirement matrix;
- M0-M6 model specification templates;
- M4 detector/systematics implementation schema;
- covariance placeholder and sensitivity template;
- leave-one-out execution protocol;
- cross-experiment transfer protocol;
- external veto data-request checklist;
- BEST-2 preregistration form;
- archive structure plan.

# Dataset Matrix Summary

| Resource | Machine-readable Status | Covariance | Extraction Level | Orientation/Timestamp | Classification |
|---|---|---|---|---|---|
| BEST | partial local summary | unavailable | unavailable | unavailable | ESSENTIAL |
| GALLEX | partial local summary | unavailable | unavailable | unavailable | IMPORTANT |
| SAGE | partial local summary | unavailable | unavailable | unavailable | IMPORTANT |
| BEST-2 | future/unavailable | unavailable | unavailable | unavailable | ESSENTIAL / CURRENTLY UNAVAILABLE |
| KATRIN | literature public, not integrated | not integrated | not applicable | not applicable | ESSENTIAL veto |
| IceCube | literature public, not integrated | not integrated | not applicable | not applicable | ESSENTIAL if tensor physical/celestial |
| Solar constraints | literature public, not integrated | not integrated | not applicable | not applicable | IMPORTANT |
| SME/Lorentz literature | public, not integrated | not integrated | not applicable | not applicable | ESSENTIAL if tensor-background interpretation |

# M0-M6 Template Summary

| Model | Purpose | Validation Role |
|---|---|---|
| M0 | null/published baseline | reference expectation |
| M1 | scalar normalization only | test scale explanation |
| M2 | cross-section/source-systematics only | test nuclear/source explanation |
| M3 | sterile-neutrino benchmark | required physics competitor |
| M4 | detector-systematics benchmark | required primary mundane competitor |
| M5 | LSC trace-only | test scalar LSC response |
| M6 | LSC trace + traceless anisotropy | test full frozen LSC template |

M6 cannot be claimed preferred unless it beats M4, passes LOO, transfers across experiments, survives external vetoes and is not blocked by covariance limitations.

# M4 Implementation Structure

The M4 schema includes:

- calibration drift;
- source normalization uncertainty;
- detector geometry asymmetry;
- extraction efficiency asymmetry;
- environmental background drift;
- covariance incompleteness;
- timing artifacts;
- orientation artifacts;
- background subtraction uncertainty.

M4 implementation outputs must report:

- included components;
- missing components;
- nuisance parameter count;
- covariance assumptions;
- fit score;
- penalty-adjusted score;
- comparison against M5/M6;
- whether M4 reproduces M6-level structures.

# Covariance Placeholder Policy

All placeholder covariance results must be labeled:

```text
NON-VALIDATION-GRADE
```

Allowed placeholders:

- diagonal covariance from summary uncertainties;
- block-diagonal covariance by experiment;
- conservative correlated-error envelope;
- source-normalization correlation envelope;
- cross-section shared uncertainty envelope.

Forbidden:

- final validation claims from placeholder covariance;
- discovery/exclusion claims;
- suppression of missing-covariance caveats.

# Leave-One-Out Protocol

Required omissions:

- BEST inner;
- BEST outer;
- BEST ratio;
- GALLEX combined;
- GALLEX Cr1;
- GALLEX Cr2;
- SAGE 51Cr;
- SAGE 37Ar;
- BEST group;
- GALLEX group;
- SAGE group.

Stability classes:

- stable;
- weakly stable;
- unstable;
- non-identifiable;
- non-validation-grade.

# Cross-Experiment Transfer Protocol

Required transfer directions:

- BEST to GALLEX;
- BEST to SAGE;
- GALLEX/SAGE to BEST;
- 51Cr to 37Ar;
- BEST/GALLEX/SAGE to future BEST-2;
- BEST inner to outer;
- BEST outer to inner.

Transfer fails if:

- target prediction fails;
- parameters become unrelated across experiments;
- M4 transfers as well or better than M6;
- isotope transfer fails;
- covariance sensitivity changes the conclusion.

# External Veto Data Requests

| Veto | Required Data |
|---|---|
| KATRIN | energy-response constraints and beta-spectrum systematics |
| IceCube | anisotropy / Lorentz / SME-related bounds |
| SME/Lorentz literature | coefficient bounds and tensor mapping rules |
| Solar-neutrino fits | solar Gallium and global fit constraints |
| Standard oscillation constraints | three-flavor global fit constraints and sterile benchmarks |
| Detector calibration literature | source activity, cross-section, extraction, counter efficiency and background uncertainty |

# BEST-2 Preregistration Form

The preregistration form requires:

- frozen equations copied from Step 1;
- frozen parameter structure;
- frozen datasets;
- M0-M6 validation hierarchy;
- prohibited post-hoc actions;
- allowed statistical interpretations;
- failure conditions;
- publication discipline.

# Freeze Archive Plan

The final archive should contain:

```text
canonical/
validation/
implementation/
audits/original/
audits/extracted/
sources/
reports/PDFs/
provenance/
MANIFEST.csv
CHECKSUMS.sha256
README.md
```

Publishing is not performed in Step 3.

# Final Validation Check

No theory expansion occurred: yes.  
No new equations were introduced: yes.  
All structures remain freeze-compatible: yes.  
Implementation artifacts are separated from theory: yes.  
All placeholder structures are clearly labeled: yes.  

# Step 4 Recommendation

STEP 4 should build the final local freeze package:

1. Assemble canonical, validation and implementation folders.
2. Generate manifest and checksums.
3. Copy final PDFs and Markdown sources.
4. Preserve original and extracted audits.
5. Prepare GitHub/Zenodo release metadata without publishing.
6. Produce final local archive ZIP for human review.

