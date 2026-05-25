# LSC Covariance Placeholder And Sensitivity Template

Status: Step 3 implementation artifact  

## 1. Core Label

All placeholder covariance outputs must be labeled:

```text
NON-VALIDATION-GRADE
```

## 2. Placeholder Policy

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

## 3. Machine-Readable Placeholder Template

```yaml
covariance_policy:
  validation_grade: NON-VALIDATION-GRADE
  covariance_type: diagonal | block_diagonal | conservative_envelope
  source:
    - published_summary_uncertainties
  missing:
    - full_systematic_covariance
    - extraction_level_correlations
  allowed_claims:
    - exploratory_sensitivity
  prohibited_claims:
    - likelihood_grade_validation
    - discovery
    - exclusion
```

## 4. Sensitivity Analysis Structure

Every exploratory run must compare:

- diagonal errors;
- high-correlation envelope;
- low-correlation envelope;
- source-normalization shared shift;
- cross-section shared shift;
- zone-correlated extraction shift.

## 5. Missing-Data Propagation

Every result table must include:

- missing covariance fields;
- affected model comparisons;
- blocked claims;
- sensitivity to placeholder choice;
- validation grade.

## 6. Statistical Caveat Policy

Required statement for placeholder covariance:

```text
This result is NON-VALIDATION-GRADE because full statistical and systematic covariance is unavailable. It is suitable only for exploratory sensitivity analysis.
```

