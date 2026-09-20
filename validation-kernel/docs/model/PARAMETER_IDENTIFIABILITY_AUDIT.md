# LSC 6.3.1 Parameter Identifiability Audit

## Technical verdict

**Verdict: `SPECIFICATION_NOT_IDENTIFIABLE_FROM_CURRENT_EVIDENCE`.**

The recovered E1-E12 structure does not determine a unique, source-justified numerical LSC 6.3.1 object. The missing information is not limited to serialization or floating-point defaults. It includes response-function shapes, normalization gauges, tensor semantics and orientation, and the mapping from the model outputs to the `R_pred` consumed by E10.

A software implementation could accept all of these choices from a caller, but that would implement a family of models rather than one immutable numerical successor. Selecting constants, zero effects, legacy values, a convenient celestial axis, or one of the unresolved prediction paths would manufacture predictive content. This audit therefore activates the STEP 07 stop condition.

This is a specification/reproducibility result. It is not a physical falsification result.

## Evidence boundary

The audit is bound to the following source objects:

| Object | SHA-256 | Evidentiary role |
|---|---|---|
| `STEP_07_INPUT_CONTRACT.json` | `50a5c83e134f34b1078663378dea372868483cfdb160570537d00164248f1b38` | STEP 07 admission and version boundary |
| `publication_boundary.json` | `d5ca8db12b4caedaf720e746ea3fef0f37904e36d23cece0f029f3dc817963ac` | Bound STEP 06 publication boundary |
| Canonical E1-E12 source | `af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981` | Authentic symbolic equations |
| Canonical core | `c8857d6bd1c8f1cb3b6d145c4b942985cb330edea879a31de6dabafef882a762` | Authentic model roles and restrictions |
| Freeze boundary | `b38ccc4f9f67e020b6c090e548e0bdcc2e8053097e22ac5ceb6447730e6a1f05` | Authentic negative evidence about unfrozen content |
| Physics audit | `faa968ca65f11b787d588f863d826a5cd5920156c7c421c84f872cc51b61e416` | Independent scientific identifiability critique |
| Dependency graph | `332263c620d38a79e65deccc8e884634e30bc1656367789f2912d5e043a3a281` | Recovered and unverified equation bindings |
| Parameter adjudication | `1ca80f15267d417da42a0195fb7ee668339d2630068461c51852f77bb40d97a8` | Parameter-by-parameter recovery status |

The stored `publication_boundary_sha256` in the STEP 07 input contract equals the actual boundary digest. The repository entered the audit at STEP 06 commit `9aa29d3e00e9af3d749713de2de23cc17ff3fbdb` with a clean worktree.

## Exact algebraic non-identifiability

E2 contains only the products

```text
lambda0 * f0_a(E,t)
lambdaA * q_a(t,Omega) * fA_a(E,t)
```

and E3 defines `q_a = n^T A_a n`. For any non-zero constants `c0`, `c1`, and `c2`, the following reparameterizations leave E2 and E7 unchanged:

```text
lambda0' = c0 * lambda0
f0_a'    = f0_a / c0

lambdaA' = c1 * lambdaA
fA_a'    = c2 * fA_a
A_a'     = A_a / (c1 * c2)
```

The sign can be absorbed in the same way. E1-E12 do not select a norm, reference component, sign convention, or weighting convention that removes these gauges. Only the products are identifiable.

There is also a coordinate gauge. For an orthogonal frame change `Q`,

```text
A_a' = Q A_a Q^T
n'   = Q n
```

leaves `n^T A_a n` invariant. A coordinate convention can describe an already selected physical orientation; it cannot select the physical orientation itself.

## The response functions contain unfixed predictive content

The freeze boundary (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_FREEZE_BOUNDARY.md`; archival evidence path, not redistributed) explicitly lists the exact forms of `f0_a(E,t)` and `fA_a(E,t)` as not frozen. The canonical core (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_CANONICAL_CORE.md`; archival evidence path, not redistributed) calls both templates “not yet physically fixed.”

The physics audit (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/audits/extracted/LSC_Physics_Audit_2026-05-25.md`; archival evidence path, not redistributed) states that the model is formally undefined without these functions and requires physically justified a-priori forms rather than functions fitted from BEST. No such physical derivation or source-selected family is present in the available evidence.

E8 observes only weighted averages. A modification `delta f0_a` with `<delta f0_a>_a = 0` is invisible to `F0_a`; a modification `delta fA_a` with `<q_a delta fA_a>_a = 0` is invisible to `FA_a`. Aggregate historical ratios therefore cannot recover the full energy/time dependence even in principle.

Choosing `f0_a = 1` or `fA_a = 1` would be a new flat-response hypothesis, not a neutral numerical convention. Choosing both effects as zero would collapse the successor into a simpler baseline and would not complete the declared trace-plus-traceless model.

## Tensor non-identifiability

The authentic tensor constraints establish rank two, square structure, symmetry, and tracelessness. They do not establish:

- the normative dimension of the serialized tensor;
- numerical components or ordering;
- a normalization or sign gauge;
- one shared tensor versus tensors indexed by zone;
- a preferred physical direction;
- orientation in ICRS or another model frame;
- the relation between zone-indexed `A_a^{ij}` in E3 and unindexed `A^{ij}` in E12.

The physics audit analyzes the intended 3-by-3 interpretation and shows that a symmetric traceless tensor then has five independent components, while the BEST summary supplies only two independent zone ratios. The current machine contract deliberately leaves the dimension unset, so the 3-by-3 interpretation is strong historical context but still requires an explicit successor adjudication.

Reducing the tensor to a uniaxial or other low-dimensional form could improve identifiability, but the preferred axis must arise from a stated physical hypothesis. Choosing the Galactic center, ecliptic, CMB dipole, ICRS pole, or a detector axis merely because it is available would change predictions without evidence.

## Units and frames determine products, not factors

E2 requires its bracket to be dimensionless. This establishes only product constraints such as

```text
[lambda0] [f0_a] = 1
[lambdaA] [A_a] [fA_a] = 1
```

It does not uniquely allocate units or normalization to the individual factors. Declaring all factors dimensionless is a possible new convention but is not selected by the source.

E11 names ICRS and a lab frame but does not fix all axes, handedness, time scale, epoch, Earth-rotation convention, a model direction `n_ICRS`, or detector orientation. Standard astrometric conventions can implement a transformation after these choices are fixed; they cannot provide the missing model-side physical direction.

## The model-to-observable binding is unresolved

E10 consumes `R_pred(theta, eta)`, while E5 emits an event expectation and E7 emits a first-order residual. The dependency graph correctly marks both E5-to-E10 and E7-to-E10 as `UNVERIFIED_DEPENDENCY`.

A complete evaluator must decide at least:

1. whether the canonical prediction is an exact ratio derived from E5 and E1;
2. whether it is `1 + Delta R` from the approximate E7 path;
3. when the approximation is valid;
4. whether the two paths must agree and to what tolerance;
5. how nuisance parameters enter without duplicating `theta` and `eta`.

This decision changes the observable semantics and numerical outputs. It cannot be hidden inside implementation plumbing. If a future proposal adds or changes this mapping, the version gate must reassess whether 6.4.0 is required under the genesis contract.

## Blocker matrix

| Required object | Current evidence | Why a neutral default is impossible | Current status |
|---|---|---|---|
| `f0_a(E,t)` | Symbol and role only | Shape determines scalar energy/time response | `UNRESOLVED` |
| `fA_a(E,t)` | Symbol and role only | Shape determines anisotropic energy/time response | `UNRESOLVED` |
| `lambda0` | No value, norm, uncertainty, or bounds | Scale/sign degenerate with `f0_a` | `UNRESOLVED` |
| `lambdaA` | No value, norm, uncertainty, or bounds | Scale/sign degenerate with `fA_a` and `A_a` | `UNRESOLVED` |
| Tensor dimension/shape family | Rank-two symmetric/traceless only | 3-by-3 is contextual, not fixed by the machine contract | `UNRESOLVED` |
| Tensor components and norm | No admissible numerical object | Zero collapses the component; legacy 5.5 tensor has no valid mapping | `UNRESOLVED` |
| Tensor sharing rule | E3 is zone-indexed; E12 is not | Global versus per-zone changes parameter count and transfer predictions | `UNRESOLVED` |
| Tensor orientation | Explicitly not frozen | Any selected direction is a physical hypothesis | `UNRESOLVED` |
| Frames and time convention | Symbolic ICRS/lab roles only | Coordinate defaults do not select physical orientation | `UNRESOLVED` |
| E1/E5/E8 integration contract | Symbolic integrals/averages | Source measure, domain, and weight normalization are missing; a numerical quadrature may be selected as a documented implementation convention only after that mathematical contract is fixed | `UNRESOLVED` |
| E5/E7 to E10 binding | Two unverified graph edges | Exact and first-order paths are not interchangeable by default | `UNRESOLVED` |
| `theta`/`eta` boundary | Historical wording is inconsistent | Changes fitting, nuisance, and serialization semantics | `UNRESOLVED` |

## Version-gate result

Current result: **`LSC_6_3_1_SPECIFICATION_BLOCKED`**.

The audit does not establish a model-class change, so `VERSION_ESCALATION_REQUIRED_7_0` is not supported. It also does not promote a hypothetical 6.4.0, because no concrete new physical specification has been supplied for classification. A future scientific proposal may remain 6.3.1 only if it supplies the missing content while demonstrating unchanged E1-E12 and observable semantics. A proposal that adds a prediction equation, changes the tensor semantics, or selects a new physical response mechanism must be adjudicated for 6.4.0 before implementation.

## Scientific decisions required to reopen STEP 07

The project owner or an explicitly authorized scientific design step must provide:

1. physically justified forms for `f0_a` and `fA_a`, including normalization and domains;
2. a gauge convention separating the response functions, amplitudes, and tensor norm;
3. the tensor dimension, sharing rule, component parameterization, and a-priori physical orientation;
4. complete frame/time conventions and the model-side celestial direction;
5. a canonical mapping from E5/E7 to E10 `R_pred`, including approximation policy;
6. the `theta`/`eta` boundary, active ordering, values, uncertainties, and bounds;
7. the integration measure, normalization, numerical method, and edge-case policy;
8. a version decision showing whether those choices preserve 6.3.1 semantics or require 6.4.0.

Until these decisions exist, no complete parameter bundle, model hash, golden numerical vector set, or release candidate can be truthfully generated.
