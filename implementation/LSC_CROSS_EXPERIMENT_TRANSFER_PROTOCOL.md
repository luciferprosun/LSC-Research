# LSC Cross-Experiment Transfer Protocol

Status: Step 3 implementation artifact  

## 1. Purpose

Cross-experiment transfer tests whether a frozen model generalizes beyond one experiment.

## 2. Transfer Directions

| Fit Source | Prediction Target |
|---|---|
| BEST | GALLEX |
| BEST | SAGE |
| GALLEX/SAGE | BEST |
| 51Cr sources | 37Ar source |
| BEST/GALLEX/SAGE | future BEST-2 |
| BEST inner | BEST outer |
| BEST outer | BEST inner |

## 3. Transfer Conditions

Transfer is valid only if:

- mapping is frozen before fitting;
- geometry differences are documented;
- isotope/source differences are documented;
- covariance limitations are stated;
- M0-M6 are evaluated under the same transfer;
- no target-specific retuning is allowed.

## 4. Transfer Failure

Transfer fails if:

- model fits source experiment but misses target experiment;
- parameters require unrelated values per experiment;
- M4 transfers as well or better than M6;
- isotope transfer fails without explanation;
- covariance sensitivity changes conclusion.

## 5. Isotope Consistency Checks

Required:

- 51Cr-trained behavior tested against 37Ar where possible;
- source-line and cross-section uncertainties propagated;
- isotope-specific systematics tested under M2 and M4.

## 6. Geometry Consistency Checks

Required:

- source position mapping;
- detector zone mapping;
- geometry uncertainty propagation;
- separation of source geometry from detector artifact.

## 7. External Veto Dependencies

Transfer success is not sufficient if:

- KATRIN veto fails;
- IceCube/SME tensor constraint fails;
- solar or standard oscillation consistency fails;
- detector calibration literature supports a simpler explanation.

