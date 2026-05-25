# LSC Covariance And Data Policy

Status: Step 2 validation infrastructure  

## 1. Purpose

This policy defines which data are essential, which assumptions are allowed, and which statistical shortcuts are forbidden before BEST-2-era validation.

## 2. Data Classification

| Class | Meaning |
|---|---|
| ESSENTIAL | Required for likelihood-level validation or core falsification |
| IMPORTANT | Strongly needed for reliable interpretation |
| OPTIONAL | Useful but not required for the main validation decision |
| CURRENTLY UNAVAILABLE | Not present in the current public/local package |

## 3. Required Covariance Structures

| Data Object | Class | Required Content | Current Status |
|---|---|---|---|
| BEST statistical covariance | ESSENTIAL | inner/outer/runs statistical correlations | CURRENTLY UNAVAILABLE |
| BEST systematic covariance | ESSENTIAL | source, extraction, efficiency, background correlations | CURRENTLY UNAVAILABLE |
| GALLEX covariance | IMPORTANT | source-run and detector-response correlations | CURRENTLY UNAVAILABLE |
| SAGE covariance | IMPORTANT | source-run, isotope and counter correlations | CURRENTLY UNAVAILABLE |
| Cross-experiment covariance | IMPORTANT | shared cross-section/source-line uncertainty treatment | CURRENTLY UNAVAILABLE |
| External veto covariance | IMPORTANT | KATRIN/IceCube/solar uncertainty mapping | CURRENTLY UNAVAILABLE |

## 4. Extraction-Level Data Requirements

| Requirement | Class | Purpose |
|---|---|---|
| BEST extraction-by-extraction table | ESSENTIAL | full likelihood and time/zone validation |
| BEST counter efficiencies | ESSENTIAL | detector/systematics separation |
| BEST source activity calibration details | ESSENTIAL | source normalization nuisance |
| BEST background-only periods | IMPORTANT | background subtraction validation |
| GALLEX exposure-level table | IMPORTANT | cross-experiment transfer |
| SAGE run-by-run source exposure | IMPORTANT | isotope and source validation |

## 5. Metadata Requirements

| Metadata | Class | Purpose |
|---|---|---|
| exposure timestamps | ESSENTIAL for anisotropy | sidereal/time tests |
| detector orientation / azimuth | ESSENTIAL for anisotropy | lab vs celestial separation |
| source position and extension | ESSENTIAL | geometry weighting |
| environmental logs | IMPORTANT | drift and background checks |
| detector geometry files | IMPORTANT | M4 geometry asymmetry |
| machine-readable public baseline predictions | IMPORTANT | reproducibility |

## 6. Allowed Placeholder Assumptions

Allowed only if clearly labeled exploratory:

- diagonal covariance approximation;
- block-diagonal covariance approximation;
- conservative envelope for unknown correlated systematics;
- summary-level rate ratios;
- approximate geometry from public reports;
- placeholder sterile baseline with explicit limitation.

These cannot support strong validation claims.

## 7. Forbidden Statistical Shortcuts

Forbidden:

- presenting diagonal-error chi-squared as final likelihood validation;
- ignoring correlated systematics;
- suppressing covariance limitations;
- using only anchor points;
- silently dropping outlier experiments;
- combining experiments with incompatible uncertainty conventions without disclosure;
- fitting tensor anisotropy without metadata;
- claiming precision from rounded summary tables.

## 8. Missing-Data Handling

Every validation report must include:

- list of missing data;
- effect of each missing input;
- whether the result is exploratory or validation-grade;
- sensitivity to placeholder assumptions;
- explicit statement of what claim is blocked.

## 9. Machine-Readable Dataset Requirements

Each dataset should eventually provide:

- source lines and intensities;
- source activity and uncertainty;
- detector geometry;
- exposure times;
- extraction runs;
- observed rates/counts;
- statistical uncertainties;
- systematic covariance;
- detector efficiency model;
- background model;
- metadata for orientation and environment.

