# LSC Leave-One-Out Execution Protocol

Status: Step 3 implementation artifact  

## 1. Purpose

Leave-one-out testing prevents anchor-fit overclaiming and tests parameter stability.

## 2. Required Inputs

- dataset table;
- model specification M0-M6;
- covariance or placeholder covariance label;
- parameter bounds;
- nuisance parameter policy;
- penalty method.

## 3. Required Omission Runs

| Omission | Prediction Target |
|---|---|
| omit BEST inner | BEST inner |
| omit BEST outer | BEST outer |
| omit BEST ratio | BEST ratio |
| omit GALLEX combined | GALLEX combined |
| omit GALLEX Cr1 | GALLEX Cr1 |
| omit GALLEX Cr2 | GALLEX Cr2 |
| omit SAGE 51Cr | SAGE 51Cr |
| omit SAGE 37Ar | SAGE 37Ar |
| omit BEST group | BEST group |
| omit GALLEX group | GALLEX group |
| omit SAGE group | SAGE group |

## 4. Execution Steps

1. Load frozen model template.
2. Load dataset and covariance status.
3. Select one omission target.
4. Fit or evaluate on remaining data only.
5. Predict omitted target.
6. Record residual and uncertainty.
7. Record parameter changes.
8. Repeat for M0-M6.
9. Compare penalty-adjusted performance.
10. Classify stability.

## 5. Stability Classification

| Class | Meaning |
|---|---|
| stable | predictions remain within preregistered tolerance and parameters remain bounded |
| weakly stable | predictions degrade but model remains interpretable |
| unstable | parameters swing or predictions fail significantly |
| non-identifiable | fit cannot distinguish model components |
| non-validation-grade | covariance/data limitations block validation claim |

## 6. Failure Handling

If LOO fails:

- do not claim validation;
- report instability;
- compare whether M4/M1/M2 are more stable;
- reduce model complexity only in a future preregistered version;
- do not add post-hoc mechanisms.

