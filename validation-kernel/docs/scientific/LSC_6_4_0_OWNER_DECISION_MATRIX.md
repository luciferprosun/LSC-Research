# LSC 6.4.0 Owner Scientific Decision Matrix

## Decision outcome

**Status:** `OWNER_AUTHORIZATION_REQUIRED`

**Recommended scientific configuration:** `R-A / T-C / S-A`

- response: physically derived, transferable scalar response with one fixed normalized shape and one signed scalar amplitude;
- tensor: anisotropic sector disabled;
- sharing: one universal physical response law, with experiment and zone variation entering only through authoritative integration inputs and nuisance terms;
- physical free-parameter count: **1**;
- physical-axis status: `NO_JUSTIFIED_AXIS_AVAILABLE`;
- successor version: **LSC 6.4.0**;
- owner authorization: **NO**.

This is the smallest currently defensible transferable successor. It is a restricted trace-only M5 configuration, not a full M6 model. It is recommended without using BEST, SAGE, GALLEX/GNO, or any other fit quality. A full uniaxial M6 option remains scientifically admissible only after the owner supplies a named, independently motivated physical axis and its machine-readable ICRS provenance.

## Evidence and decision boundary

The matrix is derived from the canonical A/B/C space in [OWNER_SCIENTIFIC_DECISIONS_REQUIRED.md](OWNER_SCIENTIFIC_DECISIONS_REQUIRED.md), the STEP 07A gauge and identifiability analysis, and the preserved E1-E12 symbolic backbone. It does not add a fourth owner decision. Exact response equations required by Response A remain an explicit owner payload; implementation may not invent them.

No parameter fit, prediction, T1-T12 execution, BEST-2 observation access, sky scan, residual-direction scan, publication, tag, or push was performed.

## Decision 1: response-function hypothesis

### Option A: Physically derived transferable functions

| Property | Assessment |
|---|---|
| Functional form | Explicit, named physical form for `S_a(E,t)` and, if anisotropy is active, `h_A,a(E,t)`. The current repository does not contain these equations; the owner must supply them before implementation. |
| Parameterization used by the recommendation | `S_a(E,t;x)=alpha_0 s(E,t;x)`, where `s` is a fixed, dimensionless, transferable template with a source-independent normalization rule and `alpha_0` is one signed amplitude. The exact `s` equation and normalization are pending owner authorization. |
| Number of free physical parameters | One in the recommended trace-only closure. A theory-fixed amplitude could reduce this to zero, but that is not assumed here. |
| Energy/time dependence | Exactly the dependence written in the owner-supplied equation; none may be inferred from data or hidden in code. |
| Source/isotope dependence | Only through explicitly declared physical arguments/constants and the authoritative E1 integration measure. No per-isotope fit is permitted by default. |
| Normalization | Must be fixed before amplitude determination, dataset-independent, dimensionless after gauge reduction, and recorded with the equation. |
| Cross-experiment transfer | Strong: the same equation and frozen amplitude are evaluated with each experiment's authoritative spectrum, geometry, exposure, and detector inputs. |
| Identifiability | Conditional but finite: one amplitude is identifiable only if the fixed template has nonzero, nondegenerate weighted response across the development design. |
| Falsifiability | Strongest option because a frozen function and amplitude produce out-of-sample transfer predictions without experiment-specific refitting. |
| Determination data | Prefer theory/calibration. If historical gallium data determine `alpha_0`, the exact rows, hashes, objective, covariance scenario, and bounds must be preregistered and become `MODEL_EXPOSED`. |
| Overfitting risk | Lowest of the non-null response options when the shape is fixed independently. |
| Extrapolation | Defined only over the owner-declared domain; out-of-domain evaluation must fail closed. |
| BEST-2 suitability | `PROSPECTIVE_SCHEMA_CAPABLE` after the exact function, amplitude, and model are frozen before observed BEST-2 data and authoritative as-built inputs are supplied. |

### Option B: Finite preregistered phenomenological basis

| Property | Assessment |
|---|---|
| Functional form | `S_a=sum_i c_i phi_i(E,t)` and, if active, `h_A,a=sum_j d_j psi_j(E,t)` with every basis element, order, domain, normalization, and coefficient bound fixed before fitting. |
| Number of free physical parameters | `p0` scalar coefficients plus `pA` anisotropic coefficients, before tensor shape degrees. Both must be declared finite integers before any data access. |
| Energy/time dependence | Restricted to the frozen basis. |
| Source/isotope dependence | Universal unless a dependence is explicitly part of the preregistered basis; per-isotope coefficients increase the model and exposure burden. |
| Normalization | Each basis vector must have a fixed, dataset-independent normalization and linearly independent design image. |
| Cross-experiment transfer | Conditional: coefficients transfer without refit only when basis domains and required inputs cover the target experiment. |
| Identifiability | Must be established by design-matrix rank and profile diagnostics before fitting. |
| Falsifiability | Moderate if the basis is small and frozen; declines rapidly with basis size. |
| Determination data | One frozen historical development set; all used data become `RETROSPECTIVE_NON_BLIND` for this model. |
| Overfitting risk | Higher than A and increasing with `p0+pA`. |
| Extrapolation | Basis-dependent and potentially unstable outside the development support. |
| BEST-2 suitability | Conditional on a pre-BEST-2 coefficient freeze and demonstrated domain coverage. |

### Option C: Observation-specific weighted moments

| Property | Assessment |
|---|---|
| Functional form | One `beta0_a=<S_a>` and, if active, one `betaA_a=<n^T B_a n>` for each fixed observation contract. |
| Number of free physical parameters | `b` moments for scalar-only or `2b` moments with anisotropy, where `b` is the number of fixed design bins. |
| Energy/time dependence | Not recoverable; compressed into design-specific moments. |
| Source/isotope dependence | Implicitly observation-specific. |
| Normalization | Fixed by the normalized E8 measure for that observation only. |
| Cross-experiment transfer | None unless a new physical mapping is added. |
| Identifiability | Local moments can be estimated, but the underlying response and tensor are not identifiable. |
| Falsifiability | Weak outside the frozen observation design. |
| Determination data | The same observation contracts whose moments are defined. |
| Overfitting risk | High when moments proliferate with observations. |
| Extrapolation | Undefined for new spectra, geometries, or exposure schedules. |
| BEST-2 suitability | `NOT_PROSPECTIVELY_SPECIFIED` without a new transfer law. |

**Recommendation: Option A.** It introduces the fewest transferable response assumptions, preserves the E1-E12 detector-response structure, permits a one-parameter closure, and has the clearest prospective falsification path. The recommendation is not executable until the owner supplies the exact physical response equation and provenance.

## Decision 2: tensor family and physical axis

The STEP 07A constraints remain fixed: dimension 3, rank 2, symmetric, traceless, five components before scale fixing, and Frobenius norm one on the nonzero branch.

### Option A: Shared normalized uniaxial tensor with an a-priori axis

The canonical tensor is

\[
T(u)=\sqrt{\frac{3}{2}}\left(uu^T-\frac{I}{3}\right),
\qquad \|u\|_2=1,
\qquad \|T\|_F=1.
\]

| Property | Assessment |
|---|---|
| Independent tensor DOF | Zero fitted tensor DOF when `u` is fixed a priori; otherwise two physical orientation DOF that may not be selected from residuals. |
| Physical interpretation | One quadrupolar preferred axis. |
| Required axis | Named physical ICRS axis fixed before validation. `u` and `-u` are the same tensor. |
| Sign degeneracy | Tensor sign is carried by the signed anisotropic amplitude; no sky-sign ambiguity remains. |
| Identifiability | Best finite full-M6 option if the axis and response shapes are externally fixed. |
| Falsifiability/transfer | Strong: one tensor and frozen response transfer to every experiment. |
| Experiment inputs | Precise time, surveyed orientation, site coordinates, source/geometry directions, and versioned Earth-orientation transforms for directional evaluation. |
| T12 | Model-side capable only after the axis is justified; experiment-side T12 remains blocked by timing/orientation/geometry prerequisites. |
| BEST-2 | Prospectively usable only with predeclared axis, frozen model, and authoritative as-built inputs. |

### Option B: Shared general 3-by-3 symmetric traceless tensor

| Property | Assessment |
|---|---|
| Independent tensor DOF | Four continuous shape/orientation DOF after Frobenius gauge, plus a signed anisotropic response amplitude. |
| Physical interpretation | General quadrupolar anisotropy without a privileged eigenvalue pattern. |
| Required axis | No single axis, but the full physical orientation/eigenframe must be specified or determined. |
| Sign degeneracy | Removed representation-wise by the canonical sign rule; physical signed response remains. |
| Identifiability | Not identifiable from the current BEST two-coordinate summary; richer directional design is required. |
| Falsifiability/transfer | Potentially broad but weak until the tensor is independently determined and frozen. |
| Experiment inputs | Same directional timing/orientation/geometry inputs as A, with sufficient design rank to constrain the tensor. |
| T12/BEST-2 | Conditional and not currently executable; no existing aggregate can establish the full tensor. |

### Option C: Disable the anisotropic sector

| Property | Assessment |
|---|---|
| Independent tensor DOF | Zero; `B_a=0` and no physical axis exists in the active model. |
| Physical interpretation | Trace-only detector response, restricted M5 branch. |
| Identifiability | Best of the three current options. |
| Falsifiability/transfer | Scalar transfer remains falsifiable; directional claims are prohibited. |
| Experiment inputs | No physical orientation or sidereal timing required for the active response. |
| T12 | Not an active model claim; T12 remains blocked/inapplicable to this restricted branch. |
| BEST-2 | Scalar prospective prediction is possible after the response function and amplitude are frozen. |

### Physical-axis audit

Scientifically admissible axes are limited to:

1. `AXIS_THEORETICALLY_DEFINED`: derived from the named LSC mechanism before any outcome inspection;
2. `AXIS_EXTERNALLY_DEFINED`: a versioned external physical direction tied to that mechanism, expressed as a normalized ICRS vector with epoch/provenance.

A coordinate pole, detector axis, Galactic centre, ecliptic direction, CMB dipole, or any other convenient catalogue direction is not admissible merely because it is available. The preserved sources contain no independently motivated physical LSC axis, and no sky or residual scan was performed.

**Current axis status: `NO_JUSTIFIED_AXIS_AVAILABLE`.**

**Recommendation: Option C.** Option A is the preferred full-M6 design only after an independently justified axis exists. In its absence, recommending A would let implementation choose physics. Option C is therefore the only currently complete, identifiable recommendation. It openly narrows 6.4.0 to trace-only M5 and forbids directional claims.

## Decision 3: cross-zone and cross-experiment sharing semantics

### Option A: One physical tensor and one response law shared

| Property | Assessment |
|---|---|
| Universal | Response equation, fixed shape, frozen physical coefficients; tensor too if a future anisotropic branch is authorized. |
| Source/isotope dependent | Only declared physical inputs and source-line/cross-section terms in the authoritative integration measure. |
| Detector/experiment dependent | Baseline efficiency, surveyed geometry, exposure, source activity, and nuisance objects; none becomes a new LSC physical coefficient. |
| Transfer rule | Freeze once, evaluate new experiment inputs without refitting. |
| Identifiability/falsifiability | Strongest; lowest parameter count and clearest cross-experiment failure condition. |

### Option B: Zone tensors derived from a frozen geometry law

| Property | Assessment |
|---|---|
| Universal | One explicit geometry-to-tensor mapping and any global response coefficients. |
| Geometry dependent | `T_a` may vary only as the deterministic result of authoritative surveyed geometry. |
| Additional content | The mapping is a new physical law, not a coordinate transform unless it is provably passive. |
| Transfer rule | Possible only when the same mapping applies without refit to every target geometry. |
| Identifiability/falsifiability | Conditional on independent justification and complete geometry. |

### Option C: Independently fitted zone or experiment tensors

| Property | Assessment |
|---|---|
| Universal | Little or none in the anisotropic sector. |
| Experiment dependent | Physical tensors are independently fitted, adding at least four normalized shape/orientation DOF per active tensor plus amplitudes. |
| Transfer rule | Absent or ambiguous. |
| Identifiability/falsifiability | Severe underidentification; risks absorbing detector systematics as LSC physics. |
| Prospective use | Cannot provide a unique new-experiment prediction without a new fit. |

**Recommendation: Option A.** It enforces the smallest physical parameter set and a decisive transfer rule: after freeze, no physical response or tensor coefficient may be refitted between experiments. Experiment-specific calibration remains a nuisance in the likelihood layer.

## Combined Response × Tensor × Sharing assessment

Notation:

- `p0>=1` and `pA>=1` are preregistered scalar and anisotropic basis coefficient counts;
- `b` is the number of fixed observation moments;
- `m` is the number of independently parameterized experiment/zone groups;
- counts exclude empirical nuisance parameters and authoritative dataset inputs;
- “blocked” means scientifically incomplete, not falsified.

| ID | Response | Tensor | Sharing | Physical parameter count | Identifiability | Transferability / required inputs | Prospective eligibility | Adjudication |
|---|---|---|---|---:|---|---|---|---|
| R-A/T-A/S-A | A | A | A | 2 | Conditional on fixed scalar/anisotropic shapes and justified axis | Strong; needs directional time/orientation/geometry | Conditional | `BLOCKED_AXIS_MISSING` |
| R-A/T-A/S-B | A | A | B | 2 plus one fixed geometry law | Conditional; law must do more than passive coordinates | Needs complete surveyed geometry and independent law | Conditional | `BLOCKED_NEW_GEOMETRY_LAW` |
| R-A/T-A/S-C | A | A | C | Undefined under canonical options | Shared a-priori tensor conflicts with independently fitted tensors | No unique transfer | No | `SCIENTIFICALLY_INADMISSIBLE` |
| R-A/T-B/S-A | A | B | A | 6 | General tensor underidentified by current summaries | Transfer only after independent tensor freeze | Conditional | `NOT_CURRENTLY_IDENTIFIABLE` |
| R-A/T-B/S-B | A | B | B | 6 plus one fixed geometry law | Underidentified and law-dependent | Requires rich directional design and geometry | Conditional | `NOT_CURRENTLY_IDENTIFIABLE` |
| R-A/T-B/S-C | A | B | C | at least `1+5m` | Severe per-group underidentification | Weak; new fit per group | No | `DOMINATED_MODEL_VARIANT` |
| R-A/T-C/S-A | A | C | A | **1** | Conditional finite one-amplitude model | Strong scalar transfer; no directional inputs | **Yes after freeze** | **`RECOMMENDED`** |
| R-A/T-C/S-B | A | C | B | 1 | Tensor geometry law is inactive and adds no prediction | Same scalar transfer as S-A | Yes after freeze | `DOMINATED_MODEL_VARIANT` |
| R-A/T-C/S-C | A | C | C | 1 | Independent-tensor rule is inactive | Same scalar transfer only if no hidden per-experiment physics | Yes after freeze | `DOMINATED_MODEL_VARIANT` |
| R-B/T-A/S-A | B | A | A | `p0+pA` | Requires full design-rank audit and justified axis | Transferable within frozen basis domain | Conditional | `CONDITIONALLY_ADMISSIBLE_NON_BLIND` |
| R-B/T-A/S-B | B | A | B | `p0+pA` plus one fixed geometry law | Basis and law both require independent rank/support | Geometry-complete targets only | Conditional | `CONDITIONALLY_ADMISSIBLE_NON_BLIND` |
| R-B/T-A/S-C | B | A | C | Undefined under canonical options | Shared axis conflicts with independent fitted tensors | No unique transfer | No | `SCIENTIFICALLY_INADMISSIBLE` |
| R-B/T-B/S-A | B | B | A | `p0+pA+4` | High-rank and currently underidentified | Requires rich directional training and target inputs | Conditional | `NOT_CURRENTLY_IDENTIFIABLE` |
| R-B/T-B/S-B | B | B | B | `p0+pA+4` plus one fixed geometry law | Higher-rank and law-dependent | Geometry-complete targets only | Conditional | `NOT_CURRENTLY_IDENTIFIABLE` |
| R-B/T-B/S-C | B | B | C | at least `p0+m(pA+4)` | Severe per-group underidentification | Requires refit per group | No | `DOMINATED_MODEL_VARIANT` |
| R-B/T-C/S-A | B | C | A | `p0` | Conditional on preregistered basis rank | Transfers without refit inside basis domain | Conditional | `CONDITIONALLY_ADMISSIBLE_NON_BLIND` |
| R-B/T-C/S-B | B | C | B | `p0` | Geometry-tensor rule is inactive | Same as S-A with extra assumption | Conditional | `DOMINATED_MODEL_VARIANT` |
| R-B/T-C/S-C | B | C | C | `p0` | Independent-tensor rule is inactive | Transfer only if basis coefficients stay shared | Conditional | `DOMINATED_MODEL_VARIANT` |
| R-C/T-A/S-A | C | A | A | `2b` observable moments; tensor not separately identifiable | Tensor information is absorbed into moments | Fixed-design only | No | `NOT_PROSPECTIVELY_SPECIFIED` |
| R-C/T-A/S-B | C | A | B | `2b` plus one geometry law | Law cannot be tested separately from moments | Fixed-design only | No | `DOMINATED_MODEL_VARIANT` |
| R-C/T-A/S-C | C | A | C | at least `2b` plus independent tensor objects | Nonidentifiable redundancy | None | No | `SCIENTIFICALLY_INADMISSIBLE` |
| R-C/T-B/S-A | C | B | A | `2b+4` formal, rank-deficient | General tensor cannot be recovered from contracted moments | Fixed-design only | No | `NOT_CURRENTLY_IDENTIFIABLE` |
| R-C/T-B/S-B | C | B | B | `2b+4` plus one geometry law | More assumptions without new observable rank | Fixed-design only | No | `DOMINATED_MODEL_VARIANT` |
| R-C/T-B/S-C | C | B | C | at least `2b+4m` | Maximally underidentified | None | No | `DOMINATED_MODEL_VARIANT` |
| R-C/T-C/S-A | C | C | A | `b` | Moments identifiable only for the frozen design | No new-experiment mapping | No | `RESTRICTED_METHOD_PROFILE_ONLY` |
| R-C/T-C/S-B | C | C | B | `b` | Geometry-tensor rule is inactive | Same fixed-design profile | No | `DOMINATED_MODEL_VARIANT` |
| R-C/T-C/S-C | C | C | C | `b` | Independent-tensor rule is inactive | Same fixed-design profile | No | `DOMINATED_MODEL_VARIANT` |

All 27 combinations are retained for audit. Dominated variants remain in the decision record; none was eliminated based on fit quality.

## Recommended LSC 6.4.0 scientific configuration

| Field | Frozen recommendation pending owner authorization |
|---|---|
| Response hypothesis | Response A: exact physically derived transferable scalar template |
| Canonical response | `S_a(E,t;x)=alpha_0 s(E,t;x)` |
| Tensor hypothesis | Tensor C: anisotropic sector disabled, `B_a=0` |
| Axis hypothesis | Not applicable to active model; audit status `NO_JUSTIFIED_AXIS_AVAILABLE` |
| Sharing | Sharing A: one universal law and frozen amplitude |
| Physical free parameters | One signed scalar amplitude `alpha_0` |
| Parameters requiring determination | `alpha_0` unless fixed by theory; exact template equation and normalization are owner-supplied structural content |
| Fixed conventions | Gauge-invariant response, E8 baseline normalization, Binding A, count/rate declaration, explicit units and domains |
| Historical data | If used to determine `alpha_0`: `MODEL_EXPOSED` / `RETROSPECTIVE_NON_BLIND` |
| Cross-experiment refit | Prohibited |
| Directional claims | Prohibited for this trace-only branch |
| BEST-2 | `FUTURE_ONLY`, `FUTURE_BLIND`, `PROSPECTIVE_SCHEMA_CAPABLE` after complete pre-data freeze and authoritative inputs |

## E1-E12 relationship

The **symbolic backbone is preserved; predictive closure is newly specified in 6.4.0**.

| Equation | Relationship to recommended configuration |
|---|---|
| E1 | Algebraically unchanged baseline expectation and authoritative measure. |
| E2 | Backbone retained; new 6.4.0 closure uses `S_a=alpha_0 s` and the anisotropic term is inactive. |
| E3-E4 | Preserved historically but inactive under Tensor C; no tensor value or axis is manufactured. |
| E5 | Algebraically unchanged integration of the scalar-closed response. |
| E6 | Unchanged observed ratio definition. |
| E7 | Unchanged derived residual role under Binding A. |
| E8 | Normalized scalar functional retained; anisotropic functional inactive. |
| E9 | Unchanged derived BEST double ratio; not an independent third coordinate. |
| E10 | Unchanged ratio-space comparison; no validation authorized in STEP 07B. |
| E11-E12 | Preserved historically but inactive; no directional claim or execution authorized. |

## Prospective transfer rule

After a valid owner authorization, exact response equation, parameter-determination manifest, and candidate freeze:

1. the same `s` equation and frozen `alpha_0` must be used for every experiment;
2. source, isotope, geometry, exposure, detector, and timing inputs enter only through their authoritative dataset contracts;
3. nuisance parameters may be profiled under the frozen statistical policy, but no LSC physical parameter may be refitted;
4. unsupported response domains fail closed;
5. a new experiment is a falsifying transfer test if its authoritative inputs are sufficient and the frozen prediction fails the preregistered criterion.

This rule makes the recommendation prospectively specified in principle without granting prediction authorization now.
