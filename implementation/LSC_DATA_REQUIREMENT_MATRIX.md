# LSC Data Requirement Matrix

Status: Step 3 implementation artifact  
Scope: dataset infrastructure preparation only  
No theory extension: yes  

## 1. Classification Key

| Class | Meaning |
|---|---|
| ESSENTIAL | Required for likelihood-grade validation, core falsification, or required veto |
| IMPORTANT | Needed for robust interpretation but not always a hard blocker |
| OPTIONAL | Useful for completeness, plotting, or secondary review |
| CURRENTLY UNAVAILABLE | Not available in the current local/public package |

## 2. Machine-Readable Matrix

| Resource | Availability status | Machine-readable status | Covariance availability | Extraction-level availability | Orientation/timestamp availability | Exposure-level availability | Relevance | Classification |
|---|---|---|---|---|---|---|---|---|
| BEST | summary values present in local package | partial JSON/CSV summary | unavailable | unavailable | unavailable | unavailable | primary two-zone Gallium validation target | ESSENTIAL |
| GALLEX | summary values present | partial JSON/CSV summary | unavailable | unavailable | unavailable | incomplete | cross-experiment transfer | IMPORTANT |
| SAGE | summary values present | partial JSON/CSV summary | unavailable | unavailable | unavailable | incomplete | cross-experiment and isotope transfer | IMPORTANT |
| BEST-2 | future/planned | unavailable | unavailable | unavailable | unavailable | unavailable | future decisive preregistered validation | ESSENTIAL / CURRENTLY UNAVAILABLE |
| KATRIN | public literature exists | not integrated locally as constraints | not integrated | not applicable | not applicable | not applicable | external energy-response veto | ESSENTIAL |
| IceCube | public constraint literature exists | not integrated locally as tensor bounds | not integrated | not applicable | not applicable | not applicable | anisotropy / SME-style veto | ESSENTIAL if tensor is physical/celestial |
| solar-neutrino constraints | public literature exists | not integrated locally | not integrated | not applicable | not applicable | not applicable | consistency veto for universal response | IMPORTANT |
| SME/Lorentz constraint literature | public literature exists | not integrated locally | not integrated | not applicable | not applicable | not applicable | tensor-background veto | ESSENTIAL if tensor interpretation exceeds detector-local response |
| detector calibration/systematics literature | partially referenced | not consolidated | unavailable | unavailable | unavailable | unavailable | M4 baseline construction | ESSENTIAL |

## 3. Required Future Data Fields

### BEST / BEST-2

- source activity calibration;
- source position and source extension;
- zone geometry;
- extraction-by-extraction table;
- counter efficiencies;
- background model;
- statistical covariance;
- systematic covariance;
- detector orientation;
- exposure timestamps;
- environmental logs;
- machine-readable baseline predictions.

### GALLEX

- source run metadata;
- exact source coordinates;
- exposure-level rates;
- detector response/covariance;
- uncertainty convention;
- source activity details.

### SAGE

- run-by-run source exposure;
- isotope-specific source metadata;
- counter-level likelihood inputs;
- 37Ar impurity table;
- covariance/systematics table.

### External Vetoes

- KATRIN energy-response constraints;
- IceCube anisotropy/Lorentz/SME bounds;
- solar-neutrino consistency tables;
- standard oscillation fit constraints;
- calibration/cross-section uncertainty literature.

## 4. Implementation Rule

Until ESSENTIAL missing data are available, outputs must be labeled:

```text
NON-VALIDATION-GRADE / EXPLORATORY ONLY
```

