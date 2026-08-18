# Missing Object Matrix

Status: Step 01 recovery gate

This matrix distinguishes an authentic symbolic specification from a complete machine-executable frozen object. A historical number is not promoted merely because its name or shape resembles an active LSC symbol.

| Object | Status | Best candidate found | Blocks evaluator? | Notes |
|---|---|---|---:|---|
| `theta` / full parameter vector | `MISSING` | Canonical core lists parameter *structures* only | YES | No complete numerical vector or authoritative serialization was found. |
| `lambda0` | `MISSING` | Symbolic `lambda0` in E2/E7 | YES | No numerical value. Toy `c0=0.808281` is post-data and has no source-defined mapping. |
| `lambdaA` | `MISSING` | Symbolic `lambdaA` in E2/E7 | YES | No numerical value. Toy `c1=0.012500` is post-data and has no source-defined mapping. |
| Scalar response `f0_a` | `MISSING` | Symbolic definition in E2/E8 | YES | The freeze boundary explicitly says the exact functional form is not frozen. |
| Anisotropic response `fA_a` | `MISSING` | Symbolic definition in E2/E8 | YES | The freeze boundary explicitly says the exact functional form is not frozen. |
| Active tensor components `A_a^{ij}` | `MISSING` | Symmetric/traceless constraints E3/E4 | YES | Historical `D` tensors use different conventions and are post-data; they cannot be substituted. |
| Tensor orientation | `MISSING` | E11 describes a future ICRS-to-lab transformation | YES for E3/E11/E12 | No authoritative direction, Euler angles, detector orientation, or equivalent frozen object. |
| Coordinate/reference frame | `MISSING` | Symbolic ICRS/lab names in E11 | YES for E11/E12 | Latitude, longitude, detector orientation, time convention, and frozen celestial direction are absent. |
| Complete unit schema | `MISSING` | Per-equation prose contains some units | YES | No vector-level unit contract covering all active parameters and inputs. |
| Parameter ordering | `MISSING` | None | YES | No authoritative ordered vector, schema, or checkpoint layout. |
| E1-E12 evaluator implementation | `MISSING` | Canonical Markdown equation set | YES | E1-E12 are document-only. The later `FrozenPredictionAdapter` reads external predictions and is not an evaluator. |
| Authentic frozen prediction table | `MISSING` | Historical fitted tables | YES for prediction-only execution | Existing tables were produced from observed BEST/GALLEX/SAGE values or are unrelated external data. |
| Frozen numerical configuration | `MISSING` | Historical 4.x/5.5/6.0 configurations | YES | No configuration binds active E1-E12 to exact values, ordering, frames, bounds, defaults, and normalizations. |
| Final parameter bounds/priors | `MISSING` | Validation templates | YES for a fit-ready contract | Explicitly classified as not frozen. No fitting is allowed in Step 01. |
| Numerical integration/default sequence | `MISSING` | Symbolic integrations E1/E5 | YES | Quadrature, normalization order, boundary handling, and defaults are not specified as an executable contract. |
| Frozen commit | `AUTHENTIC_FROZEN` | `6ffa07bdde533fcc2a550e36c762b8edd9236c47` | NO | Clean preserved `LSC-Research` object; post-BEST and pre-BEST-2. |
| Native frozen Git tag | `MISSING` | Zenodo version DOI and release metadata | NO for equations; YES for tag-level provenance | The preserved `LSC-Research` repository contains zero Git tags. A DOI is not a Git tag. |

## Conflict decisions

| Candidate pair | Decision | Reason |
|---|---|---|
| M6 toy `c0/c1` versus active `lambda0/lambdaA` | `UNVERIFIED_CONFLICT` in notes; registry class `UNVERIFIED` | Different symbols and a generator that fits observed data; no mapping exists. |
| LSC 5.5 `D=(1,-0.5,-0.5)` versus active `A_a^{ij}` | `UNVERIFIED_CONFLICT` in notes; registry class `UNVERIFIED` | Different scale, frame, zone indexing, tensor convention, and post-data provenance. |
| LSC 6.2 illustrative `delta≈0.05` versus active anisotropy amplitude | `HISTORICAL_POST_DATA` | The source calls it illustrative and not fitted or measured; it is not frozen as 6.3.0. |

## Gate result

The documentary freeze identity, symbolic E1-E12 set, parameter names, and methodological boundary are authentic. The complete numerical evaluator object is not recoverable from the available sources. This is a valid Step 01 result and must not be repaired by fitting later data.
