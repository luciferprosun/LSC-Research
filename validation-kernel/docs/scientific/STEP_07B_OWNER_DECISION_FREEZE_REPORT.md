# STEP 07B RESULT

Project: **LSC Validation Kernel**

Status: **PASS**

Decision-package verdict: **`LSC_6_4_0_OWNER_DECISION_PACKAGE_READY`**

## Executive result

The canonical STEP 07A decision space has been reduced to one evidence-based recommendation without fitting or prediction:

**`R-A / T-C / S-A` = physically derived transferable scalar response / anisotropy disabled / one universal cross-experiment response law.**

This is a restricted trace-only M5 configuration with one conditionally identifiable physical amplitude. It is not presented as a full M6 successor. No independently justified LSC physical axis exists in the preserved evidence, so a uniaxial tensor cannot currently be recommended as completed physics. The exact scalar response equation remains an owner-supplied scientific payload.

The package is ready for owner authorization, but implementation is not authorized. The implementation contract deliberately records `owner_authorized=false` and fails closed until all three decisions and the exact response equation are supplied and re-hashed.

## A. Response-function decision

### Option A: Physically derived transferable functions

Uses explicit `S_a(E,t)` and, if applicable, `h_A,a(E,t)` derived from a named mechanism. It has the lowest overfitting risk, clearest transfer rule, and strongest prospective falsifiability. Under the recommended trace-only closure, a fixed normalized `s(E,t;x)` carries one signed amplitude `alpha_0`. The exact equation, domain, normalization, constants, and provenance are not present locally and must be supplied by the owner.

### Option B: Finite preregistered phenomenological basis

Uses a finite, frozen basis with `p0` scalar and `pA` anisotropic coefficients. It is reproducible only if basis order, normalization, bounds, one development set, objective, and covariance policy are frozen before fitting. It is retrospective/non-blind when historical gallium data determine coefficients and carries greater identifiability and overfitting risk.

### Option C: Observation-specific weighted moments

Uses only `beta0_a` and `betaA_a` for fixed observation contracts. These moments can describe one design but do not determine transferable energy/time functions or tensor content. A new experiment would require a new mapping, so this option is not a complete prospective successor.

**Recommended:** **A. Physically derived transferable functions**

**Reason:** fewest transferable assumptions, one-amplitude finite closure, strongest no-refit transfer, clearest falsification, and lowest overfitting risk. No historical fit quality was inspected or used. Exact owner equations remain mandatory before implementation.

## B. Tensor/axis decision

### Option A: Shared normalized uniaxial tensor with an a-priori axis

The Frobenius-normalized tensor

\[
T(u)=\sqrt{3/2}(uu^T-I/3)
\]

is the minimum finite full-M6 tensor if `u` is physically justified and frozen a priori. It leaves one signed anisotropic amplitude after response-shape freeze and can transfer across experiments. It requires an independently motivated, machine-readable ICRS axis; `u` and `-u` are equivalent.

### Option B: Shared general 3-by-3 symmetric traceless tensor

Retains four continuous shape/orientation degrees after Frobenius gauge plus the signed anisotropic response. It is not identifiable from current BEST summary coordinates and requires a richer directional design before it can become a frozen predictive object.

### Option C: Disable the anisotropic sector

Sets `B_a=0` as an explicit 6.4.0 physical branch decision. It has zero tensor parameters, needs no preferred axis, is the most identifiable option, and prohibits directional/sidereal claims. It yields a restricted trace-only M5 model rather than a full M6 successor.

**Recommended:** **C. Disable the anisotropic sector**

**Physical-axis status:** **`NO_JUSTIFIED_AXIS_AVAILABLE`**

**Reason:** the repository contains no independent LSC axis hypothesis. No sky, residual, or best-fit direction scan was performed. Option A remains the preferred full-M6 alternative only if the owner supplies a theory-defined or externally defined axis with ICRS coordinates and provenance. Until then, selecting it would allow implementation to choose physics.

## C. Sharing-semantics decision

### Option A: One physical tensor and one response law shared

Freezes one response equation and physical parameter set for all zones and experiments. Source, isotope, geometry, detector, exposure, and timing variation enters only through authoritative integration inputs. Calibration factors stay in `eta` as nuisance parameters.

### Option B: Zone tensors derived from a frozen geometry law

Allows deterministic zone variation only through one universal, independently justified geometry-to-tensor mapping. If the mapping is merely a passive coordinate transform, it is equivalent to A; if it changes physical tensors, it is new model content requiring complete geometry.

### Option C: Independently fitted zone or experiment tensors

Introduces at least four normalized tensor shape/orientation degrees per active tensor plus amplitudes, destroys a unique transfer rule, and can absorb detector systematics as LSC physics. It is severely underidentified.

**Recommended:** **A. One physical tensor and one response law shared across experiments/zones**

**Reason:** smallest parameter count, strongest transfer, and clearest falsification. No physical parameter may be refitted between experiments; experiment-specific nuisance parameters cannot be promoted to LSC physics.

## D. Recommended combined LSC 6.4.0 configuration

| Field | Recommendation |
|---|---|
| Configuration | `R-A / T-C / S-A` |
| Scalar response | `S_a(E,t;x)=alpha_0 s(E,t;x)` with exact `s` supplied by owner |
| Anisotropic response | inactive, `B_a=0` |
| Axis | none in the active model |
| Sharing | universal physical law and frozen physical amplitude |
| Model profile | restricted trace-only M5 |
| E1-E12 statement | symbolic backbone preserved; predictive closure newly specified in 6.4.0 |
| Directional claims | prohibited |
| Empirical refit between experiments | prohibited |

All 27 Response × Tensor × Sharing combinations were assessed in [LSC_6_4_0_OWNER_DECISION_MATRIX.md](LSC_6_4_0_OWNER_DECISION_MATRIX.md). Dominated variants remain recorded. The recommendation was selected on parsimony, identifiability, transfer, falsifiability, and prospective applicability, never on goodness-of-fit.

## E. Physical parameter count

- active free physical parameters: **1**;
- parameter: signed scalar amplitude `alpha_0`;
- fixed structural object: exact normalized transferable response `s(E,t;x)`;
- active tensor parameters: **0**;
- nuisance parameters: excluded from the LSC physical count;
- count condition: the owner must supply one fixed, nondegenerate response template without additional free shape coefficients.

If the owner supplies a parameterized response family instead, this count changes and the decision package must be regenerated rather than silently expanded.

## F. Parameters requiring empirical determination

`alpha_0` requires a value and scientifically justified bounds unless an external theory/calibration supplies both. No value, bound, prior, objective, or fit is selected in STEP 07B.

If retrospective determination is authorized later, it requires one immutable development manifest containing exact rows and hashes, one objective, covariance/nuisance policy, bounds, initialization, optimizer, tolerances, rank diagnostics, stopping rule, and `MODEL_EXPOSED` labels. Physical refit for a new experiment is prohibited.

Registry: [LSC_6_4_0_PARAMETER_DETERMINATION_REGISTRY.csv](LSC_6_4_0_PARAMETER_DETERMINATION_REGISTRY.csv).

## G. Identifiability

The recommendation is **conditionally one-dimensional and identifiable** after the owner fixes a normalized response shape whose weighted image is nonzero and nondegenerate in the development design.

- exact `lambda0/f0` and `lambdaA/fA/A` scale/sign gauges remain removed;
- no tensor orientation or shape is estimated;
- nuisance parameters remain separate;
- unsupported response domains fail closed;
- general STF and observation-moment variants remain respectively underidentified or non-transferable.

The condition is explicit: absent an exact response equation, no executable model exists.

## H. Prospective transferability

After valid authorization, parameter determination, and freeze:

1. `s` and `alpha_0` are unchanged across experiments;
2. authoritative source, isotope, geometry, exposure, and detector inputs define the target measure;
3. nuisances may be treated only under the frozen statistical policy;
4. no LSC physical parameter is refitted;
5. the target output is a genuine transfer prediction or the evaluator fails closed.

This produces a clear out-of-sample falsification path.

## I. BEST-2 prospective capability

- status: **`FUTURE_ONLY`**;
- blindness: **`FUTURE_BLIND`**;
- capability: **`PROSPECTIVE_SCHEMA_CAPABLE`**;
- observed BEST-2 data accessed: **NO**;
- prediction generated: **NO**.

Capability is conditional on a complete owner-authorized equation, frozen `alpha_0`, model hash, authoritative as-built source/geometry/exposure/detector inputs, and a hashed prediction artifact created before observed outcomes are accessed.

## J. Version

**LSC 6.4.0**

Reason: completion requires new response closure, an explicit tensor-branch decision, and a cross-experiment physical-sharing rule. These change the transferable prediction space while preserving the detector-response model class. A patch-level 6.3.1 label would conceal new physical assumptions; 7.0 is not required.

## K. 6.3.1 disposition

**`ABANDONED_BEFORE_RELEASE`**

Reason: completion required new physical assumptions and therefore semantic version escalation to 6.4.0. Historical 6.3.0 remains immutable and is not retroactively completed.

## L. Implementation contract

[LSC_6_4_0_IMPLEMENTATION_CONTRACT.json](../../LSC_6_4_0_IMPLEMENTATION_CONTRACT.json) records:

- model version and parent lineage;
- exact canonical A/B/C option titles;
- all 27 combination adjudications;
- recommended `R-A/T-C/S-A` configuration;
- classification ledger separating physical, gauge, preserved, and coordinate choices;
- E1-E12 relationship;
- gauge, units, frames, observable binding, and integration normalization;
- one-parameter schema and determination requirements;
- historical/prospective validation restrictions;
- `owner_authorized=false` and `ready_for_implementation=false`.

Implementation cannot begin from this contract until a complete owner authorization and exact Response A equation payload produce a new authorized hash.

## M. Owner authorization

### Decision 1

**Recommended:** A. Physically derived transferable functions

**Owner authorization required:** **YES**

### Decision 2

**Recommended:** C. Disable the anisotropic sector

**Owner authorization required:** **YES**

### Decision 3

**Recommended:** A. One physical tensor and one response law shared across experiments/zones

**Owner authorization required:** **YES**

Authorization form: [OWNER_AUTHORIZATION_REQUIRED.md](../../OWNER_AUTHORIZATION_REQUIRED.md).

## N. Tests

- STEP 07B targeted tests: **16/16 PASS**;
- full suite: **192/192 PASS**, plus **18/18 parameterized subtests**;
- exact three-decision and canonical-option integrity: PASS;
- 27-combination completeness and uniqueness: PASS;
- no hidden fourth physical assumption: PASS;
- physical/gauge classification separation: PASS;
- version escalation and 6.3.1 abandonment: PASS;
- no per-experiment nuisance promotion: PASS;
- no axis/sky/residual selection: PASS;
- BEST-2 future/blind/no-prediction guards: PASS;
- freeze source/artifact SHA-256 bindings: PASS;
- fail-closed owner authorization gate: PASS;
- explicit E1-E12 relationship: PASS;
- historical 6.3.0 identity and equation hash: PASS.

## O. Historical integrity

- historical 6.3.0 HEAD: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`;
- historical tree dirty files: **0**;
- preserved archive hashes: **1,882/1,882 PASS**;
- nested repositories: **4/4 clean**, expected HEADs, `git fsck` PASS;
- canonical E1-E12 SHA-256: `af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981`;
- historical 6.3.0 modified: **NO**;
- fit/prediction/T1-T12/BEST-2 execution: **NONE**.

## P. Git state

- input branch: `main`;
- input HEAD: `2c7f29cab7aeb5d1ffb0aa2c2693ba9e13b6346d`;
- intended commit: `Step 07B: prepare LSC 6.4.0 owner scientific decision freeze`;
- push: **NO**;
- tag: **NO**;
- release/publication: **NO**;
- final commit and clean-worktree receipt: reported after the commit because a commit cannot contain its own hash.

## Q. Next readiness

**READY FOR OWNER AUTHORIZATION: YES**

**READY FOR STEP 07C AFTER OWNER AUTHORIZATION: YES**

Here “owner authorization” means all three decisions plus the exact Response A equation/domain/normalization/provenance payload and a regenerated hash-bound contract. A bare option tick without that payload is not valid authorization. Current immediate readiness for implementation remains **NO**.

Recommended next step after valid authorization:

**STEP 07C — Complete LSC 6.4.0 Numerical Implementation + Parameter Determination + Executable RC**

No implementation, fit, prediction, validation, release, tag, push, or publication is authorized before that gate.
