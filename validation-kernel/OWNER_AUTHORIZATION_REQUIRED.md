# LSC 6.4.0 Owner Authorization Required

## Authorization state

- successor: **LSC 6.4.0**;
- decision package: **READY FOR OWNER REVIEW**;
- owner authorization recorded: **NO**;
- implementation authorized: **NO**;
- fitting, prediction, T1-T12, BEST-2 prediction, release, tag, push, and publication: **NOT AUTHORIZED**.

Authorization is valid only if all three decisions below are completed together. Selecting Response A or B also requires attaching the exact equations, domains, normalizations, and provenance requested by the canonical decision. A changed option invalidates the current implementation-contract hash and requires a new scientific-decision freeze.

## Decision 1

**Question:** Which response-function hypothesis defines the LSC 6.4.0 predictive closure?

**Recommended:** **A. Physically derived transferable functions**

**Alternatives:**

- **B. Finite preregistered phenomenological basis**
- **C. Observation-specific weighted moments**

**Consequence of recommendation:** one fixed, transferable, dimensionless scalar template `s(E,t;x)` and one signed amplitude `alpha_0` form the recommended trace-only response. The exact physical equation, normalization, domain, external constants, and provenance must be supplied with owner authorization. If historical gallium data determine the amplitude, they are permanently `MODEL_EXPOSED` and `RETROSPECTIVE_NON_BLIND` for this model.

**Required owner payload for A:**

- exact equation for `s(E,t;x)`;
- meaning and canonical units of every argument;
- dataset-independent normalization rule;
- valid domain and fail-closed out-of-domain policy;
- source/isotope transfer rule;
- provenance or named physical mechanism;
- theoretical value/range for `alpha_0`, or authorization for one preregistered retrospective determination.

**Owner selection:** PENDING

**Owner authorization required:** **YES**

## Decision 2

**Question:** Which tensor family and physical-axis hypothesis defines LSC 6.4.0?

**Recommended:** **C. Disable the anisotropic sector**

**Alternatives:**

- **A. Shared normalized uniaxial tensor with an a-priori axis**
- **B. Shared general 3-by-3 symmetric traceless tensor**

**Consequence of recommendation:** the active model is a restricted trace-only M5 configuration with `B_a=0`. It has no active physical axis and makes no directional or sidereal claim. This is recommended because the current evidence contains no independently justified LSC physical axis, while a general STF tensor is underidentified.

**If the owner instead selects A:** the authorization must name the physical hypothesis and provide a normalized ICRS vector, coordinate/epoch metadata, immutable source provenance, and a declaration that no outcome, residual, or sky scan selected it. A coordinate landmark alone is not a physical hypothesis.

**Current physical-axis status:** `NO_JUSTIFIED_AXIS_AVAILABLE`

**Owner selection:** PENDING

**Owner authorization required:** **YES**

## Decision 3

**Question:** Which cross-zone and cross-experiment sharing semantics define LSC 6.4.0?

**Recommended:** **A. One physical tensor and one response law shared across experiments/zones**

**Alternatives:**

- **B. Zone tensors derived deterministically from a frozen geometry law**
- **C. Independently fitted zone or experiment tensors**

**Consequence of recommendation:** the physical response equation and its frozen parameters transfer without refit. Source, isotope, geometry, detector, and exposure differences enter through authoritative integration inputs. Experiment-specific calibration remains a nuisance and cannot silently become experiment-specific LSC physics.

**Owner selection:** PENDING

**Owner authorization required:** **YES**

## Owner record

- owner name/identifier: PENDING
- authorization timestamp UTC: PENDING
- all three decisions accepted: NO
- required Response A/B equation payload attached: NO
- scientific-decision freeze regenerated after authorization: NO
- implementation authorization: NO

Until this record is completed and a new hash-bound authorized contract is generated, STEP 07C must fail closed.
