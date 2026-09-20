# STEP 07C RESULT

Project: LSC Validation Kernel
Status: **FAIL**

Verdict: **`LSC_6_4_0_PARAMETER_DETERMINATION_FAILED`**

The owner-authorized A2/C/A scientific profile has a complete, deterministic, fail-closed evaluator and a defensible hash-bound cross-section function. The only preregistered retrospective determination of `alpha_0` nevertheless failed: its unconstrained optimum is outside the frozen first-order analysis domain and its constrained optimum is boundary dominated. The adverse result is preserved without changing A2, the spline, the dataset, the covariance policy, or the bounds. No parameter bundle or release candidate was created.

## A. Owner authorization

PASS.

- Decision 1: `A2`, capture-energy dilation, `OWNER_AUTHORIZED`.
- Decision 2: `C`, anisotropic sector disabled, `OWNER_AUTHORIZED`.
- Decision 3: `A`, universal cross-experiment sharing, `OWNER_AUTHORIZED`.
- Version: LSC 6.4.0.
- A2 classification: `NEW_PHYSICAL_HYPOTHESIS_6_4_0`.
- Planned LSC 6.3.1 executable successor: `ABANDONED_BEFORE_RELEASE`.
- Historical LSC 6.3.0 remains immutable.

## B. A2 response

Implemented exactly as:

`F_m(E) = d ln sigma_m(E) / d ln E = E sigma_m'(E) / sigma_m(E)`

`S_a(E,t) = alpha_0 F_m(E)`

`R_pred,a = 1 + alpha_0 <F_m>_a`

There is no intrinsic scalar time dependence. Time, activity, exposure, geometry, efficiency, source lines, and conventional probability remain external conventional inputs to the normalized baseline measure. A2 contains exactly one LSC physical parameter, `alpha_0`.

## C. Cross-section function and provenance

PASS.

The 2023 paper, DOI `10.1103/PhysRevC.108.035502`, supplies exact modern `51Cr` and `37Ar` line energies and branchings but no complete continuous total-cross-section payload. The executable function therefore uses the 58-point Bahcall 1997 best-estimate table, DOI `10.1103/PhysRevC.56.3391`, whose paper explicitly prescribes cubic-spline interpolation.

Production scenario: `BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE`.

Payload SHA-256: `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5`.

No undocumented digitization or outcome-dependent model selection was used.

## D. Interpolation/derivative

PASS.

- Natural cubic spline in linear energy and cross section.
- Natural endpoint condition is an explicit pre-fit numerical convention.
- Analytic spline derivative.
- `E sigma'/sigma` and `d ln sigma/d ln E` agree.
- Independent standard-library natural-spline implementation agrees with SciPy production code.
- No extrapolation.
- Derivative-model uncertainty remains a documented limitation.

## E. Domain

- Cross-section payload: `[0.240, 30.000] MeV`.
- Production source profiles: exact frozen `51Cr` and `37Ar` line sets.
- Theory bound on `alpha_0`: not available.
- Numerical line-support bound: `[-0.5747389495096434, 3.607238025076703]`.
- Linear positivity lower bound: `-0.5487452273628239`.
- Frozen analysis bound: `[-0.06137569484389956, 0.09541395625505644]`, defined by at most 1% relative deviation from the exact finite dilation at every frozen line.
- Unsupported input fails closed.

## F. alpha_0 definition

`alpha_0` is dimensionless, signed, universal, and represents logarithmic incident-energy dilation. `alpha_0=0` is the exact null limit. It cannot be fit separately by zone, isotope, or experiment. The one-parameter production profile has no hidden physical coefficients.

## G. Evaluator

PASS for explicit supported in-domain `alpha_0`.

`LSC640Evaluator`:

- verifies all provenance hashes;
- validates exact line identities and every conventional factor;
- computes the normalized baseline measure;
- reports per-line cross section, `F_m`, `S_a`, and baseline weight;
- reports model, response, payload, source-line, and input hashes;
- rejects NaN, non-positive measure, extrapolation, unknown fields, altered line sets, and invalid profiles;
- performs no fitting;
- has no fallback or historical/toy default.

Model SHA-256: `4a8f40e59431a27f8f4d5bc9809a706125a46ebdb5728458e4b04503e935b6f2`.

## H. Schemas

PASS.

- `spec/LSC_6_4_0_PREDICTION_INPUT.schema.json`
- `spec/LSC_6_4_0_PREDICTION_OUTPUT.schema.json`

All model and conventional input fields are explicit. Covariance and nuisance identities are declared in `analysis_context`; they are not silently absorbed into LSC physics.

## I. Golden vectors

PASS, `15/15`.

They cover exact null behavior, positive and negative `alpha_0`, both source isotopes, two experiment labels with identical physics, synthetic source-line integration, both analysis bounds, and three fail-closed conditions. No observed deficit is used in a golden vector.

## J. Independent verification

PASS.

The reference path implements its own natural-spline tridiagonal solver, polynomial evaluation, derivative, and weighted integration without calling the production SciPy derivative/integration implementation. Production and reference calculations agree over a 101-point source-energy grid and all successful golden vectors.

## K. Parameter-determination preregistration

PASS and hash-frozen before execution.

- Development data: BEST inner published aggregate only.
- Holdout: BEST outer, GALLEX/GNO, SAGE Cr51, SAGE Ar37.
- Exposure: `MODEL_EXPOSED`, `RETROSPECTIVE_NON_BLIND`, `DEVELOPMENT_DATA`.
- Objective: one-parameter diagonal Gaussian chi-square.
- Covariance: `COV_DIAGONAL`, `ASSUMPTION_BASED_SENSITIVITY_ONLY`.
- Nuisance: no separately profiled nuisance; published aggregate uncertainty used directly.
- Optimizer: SciPy bounded scalar minimizer, fixed tolerances.
- Fit execution count: one.
- Bounds, boundary rule, uncertainty construction, failure rules, and no-refit policy were frozen.

## L. Pre-fit audit

PASS.

Owner authorization, response, cross section, interpolation, derivative, schemas, evaluator determinism, `15/15` golden vectors, independent reference, development split, objective, covariance, bounds, and BEST-2 blindness all passed.

Pre-fit freeze SHA-256: `60380837f348cc41dc3d0b240fcba0b61a95c9f61cfab2bc3f5e7db71e9ea179`.

Full repository suite immediately before execution: `227 passed, 1 skipped, 24 subtests passed`. The skip was the expected frozen-result test before the result existed.

## M. alpha_0 determination

**FAILED as preregistered.**

| Field | Result |
|---|---:|
| observed BEST inner ratio | 0.791 +/- 0.05 |
| `mean_F_m` | 1.8020760538663734 |
| unconstrained optimum | -0.1159773471000784 |
| frozen domain | [-0.06137569484389956, 0.09541395625505644] |
| constrained optimizer result | -0.06137569305004568 |
| objective at constrained result | 3.872735360003486 |
| convergence | PASS |
| identifiability | PASS, one-dimensional |
| boundary status | `BOUNDARY_DOMINATED` |

The optimizer succeeded numerically, but the scientific determination failed because the required value lies outside the frozen first-order domain. No certified uncertainty interval is reported.

## N. Parameter freeze

NOT PERFORMED.

`LSC_6_4_0_PARAMETER_BUNDLE.json` does not exist. The boundary-dominated constrained value is a diagnostic fit output, not a frozen physical parameter. No refit is authorized.

## O. Retrospective smoke test

NOT PERFORMED. The protocol allowed a historical smoke only after successful parameter freeze. Executing it after the adverse determination would cross the frozen boundary.

## P. BEST-2 blind status

PASS.

- Status: `FUTURE_ONLY`, `FUTURE_BLIND`.
- Observed data accessed: NO.
- Prediction generated: NO.
- Schema capability: conditional on future authoritative as-built inputs and a separately authorized model revision with a valid frozen parameter.

## Q. Release candidate

NOT CREATED.

There is no `release_candidate/LSC-6.4.0-rc1/`, no parameter bundle, no RC manifest, and no RC SHA-256. Creating them would contradict the frozen failure policy.

## R. Reproducibility

PASS for implementation and adverse-result reproduction.

- Python 3.12.3, NumPy 2.5.2, SciPy 1.18.0.
- Exact dependency/environment lock recorded.
- Two fresh interpreter runs produced identical canonical receipts.
- Golden vectors, pre-fit gate, and frozen adverse result reproduce.
- The production and independent reference implementations agree.

## S. Tests

PASS: `228 passed, 24 subtests passed`.

The dedicated STEP 07C suite covers provenance, spline knots and positivity, derivative equivalence, line normalization, null/signed response, universal sharing, tensor/axis rejection, altered lines, unsupported domain, deterministic serialization, schemas, golden vectors, independent reference, pre-fit freeze, exact adverse-result reproduction, no-refit enforcement, BEST-2 blindness, and historical integrity.

## T. Historical integrity

PASS.

- Historical LSC 6.3.0 nested HEAD: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`.
- Historical nested worktree: clean.
- Historical archive SHA-256 manifest: `1882/1882 PASS`.
- E1-E12 provenance remains preserved.
- Prior STEP 07B/07B.1 freeze bindings are verified against their historical Git blobs when current successor documents legitimately evolve.
- No historical equation, parameter, or dataset was rewritten.

## U. Git state

- Input HEAD: `34e89cb5895a8d011ac31ee84f34c201f7e309a9`.
- Branch: `main`.
- Intended commit subject: `Step 07C: implement and freeze executable LSC 6.4.0`.
- Push: NO.
- Tag: NO.
- Publication: NO.
- Final STEP 07C commit: the commit containing this report; exact SHA is reported in the operator handoff because a commit cannot contain its own SHA.

## V. Remaining blockers

1. `alpha_0` could not be frozen within the preregistered A2 linear-response domain.
2. Therefore the parameter bundle and RC cannot be created.
3. Full collaboration covariance remains unavailable; the executed development objective is sensitivity-only.
4. Full retrospective validation remains unexecuted and unauthorized.
5. BEST-2 prediction remains prohibited.
6. T12/directional claims are outside the tensor-off production profile.
7. KATRIN/IceCube mappings remain unjustified.

## W. STEP 08 readiness

**READY FOR FINAL AUDIT: NO**

STEP 08 publication audit is not authorized because there is no successful parameter freeze or RC. The correct next action is to preserve this adverse result. Any new response, wider validity regime, or nonlinear energy-dilation model would be a newly owner-authorized model revision with a new preregistration, not a repair or refit of this A2 candidate.
