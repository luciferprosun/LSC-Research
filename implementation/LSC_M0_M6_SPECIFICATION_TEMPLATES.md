# LSC M0-M6 Specification Templates

Status: Step 3 implementation artifact  
Purpose: formal model-template definitions for future validation execution  

## Shared Rules

All models must report:

- datasets used;
- parameters and nuisance parameters;
- allowed freedoms;
- forbidden freedoms;
- penalty method;
- covariance status;
- comparison targets;
- allowed claims;
- prohibited claims.

No template may introduce new theory.

## M0 - Null / Published Baseline

| Field | Specification |
|---|---|
| purpose | published or standard baseline expectation |
| parameters | none beyond published baseline inputs |
| allowed freedoms | documented experimental uncertainties only |
| forbidden freedoms | hidden normalization tuning |
| required penalties | none or fixed-baseline accounting |
| required datasets | BEST/GALLEX/SAGE baseline expectations |
| comparisons | all models vs M0 |
| allowed claims | residual exists relative to baseline |
| prohibited claims | LSC support by residual alone |

## M1 - Scalar Normalization Only

| Field | Specification |
|---|---|
| purpose | test global scale / normalization explanation |
| parameters | scalar normalization nuisance |
| allowed freedoms | one preregistered scale parameter or documented source-specific scale |
| forbidden freedoms | zone-specific tensor-like behavior |
| required penalties | scalar parameter penalty |
| required datasets | rate ratios and covariance |
| comparisons | M1 vs M5/M6 |
| allowed claims | trace may be normalization-like |
| prohibited claims | directional structure |

## M2 - Cross-Section / Source-Systematics Only

| Field | Specification |
|---|---|
| purpose | test nuclear/source explanation |
| parameters | source activity, cross-section and isotope nuisance terms |
| allowed freedoms | literature-supported uncertainties |
| forbidden freedoms | arbitrary post-hoc source shifts |
| required penalties | nuisance and uncertainty penalties |
| required datasets | source lines, source activity, cross-section uncertainties |
| comparisons | M2 vs M5/M6 |
| allowed claims | source/cross-section can explain trace if supported |
| prohibited claims | LSC preference without outperforming M2 |

## M3 - Sterile-Neutrino Benchmark

| Field | Specification |
|---|---|
| purpose | required physics competitor |
| parameters | sterile benchmark parameters as preregistered |
| allowed freedoms | standard benchmark scan or fixed literature benchmark |
| forbidden freedoms | omitting M3 from final comparison |
| required penalties | complexity/scan penalty |
| required datasets | L/E mapping, geometry, rates, covariance |
| comparisons | M3 vs M5/M6 |
| allowed claims | LSC compares to sterile baseline |
| prohibited claims | sterile excluded unless full analysis supports it |

## M4 - Detector-Systematics Benchmark

| Field | Specification |
|---|---|
| purpose | required mundane competitor |
| parameters | calibration, source, extraction, geometry, background, environment, covariance and orientation artifacts |
| allowed freedoms | physically motivated detector/systematics terms |
| forbidden freedoms | treating M4 as optional |
| required penalties | nuisance and complexity penalties |
| required datasets | calibration, extraction, background, geometry, covariance metadata |
| comparisons | M4 vs M5/M6 |
| allowed claims | detector/systematics can mimic LSC if it fits |
| prohibited claims | LSC preference before M4 is evaluated |

## M5 - LSC Trace-Only

| Field | Specification |
|---|---|
| purpose | test scalar trace response |
| parameters | frozen trace response amplitude and nuisance terms |
| allowed freedoms | preregistered scalar template only |
| forbidden freedoms | directional/tensor terms |
| required penalties | trace parameter penalty |
| required datasets | rate ratios, covariance, baseline expectations |
| comparisons | M5 vs M1/M2/M4/M6 |
| allowed claims | trace template improves fit if validated |
| prohibited claims | anisotropy or sidereal signal |

## M6 - LSC Trace + Traceless Anisotropy

| Field | Specification |
|---|---|
| purpose | full frozen LSC detector-response test |
| parameters | trace amplitude, anisotropic amplitude, frozen tensor/orientation structure, nuisance terms |
| allowed freedoms | only preregistered trace/traceless template |
| forbidden freedoms | post-hoc tensor orientation or added terms |
| required penalties | full complexity penalty |
| required datasets | covariance, orientation/timestamps, geometry, exposure data |
| comparisons | M6 vs M0-M5 |
| allowed claims | candidate support only if all validation criteria pass |
| prohibited claims | discovery, sterile exclusion, or validation without M4/covariance/vetoes |

