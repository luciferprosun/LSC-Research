# LSC Successor Parameter-Determination Requirements

## Result

Gauge reduction does not supply numerical predictive content. A future LSC 6.4.0 development step must determine the response functions and tensor hypothesis before any validation run. No such determination was performed in STEP 07A.

## Separation of model, development data, and validation data

1. The scientific model consists of the invariant response objects `S_a(E,t)` and `B_a(E,t)=h_A,a(E,t)T_a`.
2. Experimental source, geometry, exposure, timing, and detector inputs define the integration measure; they are not LSC parameters.
3. `eta` and `C` belong to the likelihood/data layer, not the LSC physical vector.
4. Any historical dataset used to determine a response parameter becomes development data for that parameter and remains `MODEL_EXPOSED` / `RETROSPECTIVE_NON_BLIND`.
5. BEST-2 observed results must not enter model development if a future BEST-2 prediction is to remain `FUTURE_BLIND`.

## Required determinations

| Object | What must determine it | Admissible development evidence | Fit required? | Exposure consequence | Required protocol |
|---|---|---|---:|---|---|
| scalar response family `S_a(E,t)` | a-priori detector, cross-section, geometry, or other explicit physical mechanism | theory/calibration preferred; historical gallium only under a declared development objective | Conditional | historical gallium becomes non-blind for fitted coefficients | freeze family, normalization, domain, coefficients, bounds, objective and data hashes before diagnostics |
| anisotropic response family `h_A,a(E,t)` | a-priori directional detector mechanism | theory/calibration preferred | Conditional | any fitted directional information becomes model-exposed | freeze functional family and its zone/experiment transfer rule before fitting |
| normalized tensor family `T_a` | explicit physical tensor hypothesis | external physical hypothesis or calibration; not goodness-of-fit selection | Preferably no | fitted orientation invalidates a strict blind sidereal claim for the same data | freeze general versus uniaxial shape, sharing rule, frame, orientation, and sign representative |
| scalar amplitude, if a fixed scalar shape is selected | one preregistered development objective or external theory | an explicitly named historical development subset | Yes unless theoretical | every used row is `MODEL_EXPOSED` | use one objective, one covariance scenario fixed in advance, bounds, optimizer manifest and uncertainty interpretation |
| anisotropic amplitude, if shape and tensor are fixed | one preregistered development objective or external theory | historical directional data only if timing/orientation are adequate | Yes unless theoretical | used directional data are non-blind | do not fit tensor shape or direction simultaneously unless that larger model was preregistered and identifiable |
| parameter bounds | theory, calibration range, or preregistered numerical domain | not validation outcomes | No | none if fixed before evaluation | record physical rationale and distinguish hard domain from probabilistic prior |

## Exact future fitting protocol if empirical determination is authorized

Before fitting, create an immutable development manifest containing:

- model version and model hash;
- response-family equations and parameter ordering;
- every development dataset, row identifier, and SHA-256;
- the single objective function;
- baseline and nuisance policy;
- covariance scenario and its inferential limitations;
- parameter bounds and initialization;
- optimizer, tolerances, convergence criteria, and seed policy;
- identifiability rank test and profile diagnostics;
- stopping rule;
- explicit `MODEL_EXPOSED` labels;
- prohibited hold-out and future datasets.

After the fit, freeze the parameter bundle before running retrospective diagnostics. A failed diagnostic cannot trigger an undocumented parameter revision. Any revision is a new development candidate with a new hash and complete audit trail.

## Parameter-free and low-parameter possibilities

- **Zero free physical parameters:** possible only if a physical derivation supplies all nonzero response fields and tensor content. No such derivation exists locally. Setting the response to zero is the null model, not a completed LSC model.
- **One scalar amplitude:** possible only after a fixed normalized scalar response shape is supplied and anisotropy is explicitly disabled. This is a restricted trace-only M5 model.
- **Scalar plus anisotropic amplitude:** possible only after both response shapes and a normalized tensor shape/orientation are fixed a priori. This is the minimum full trace/traceless option.
- **Larger parameter set:** a general normalized STF tensor contributes four tensor shape/orientation degrees per active tensor, and unrestricted response functions are infinite-dimensional. This form is not identifiable from current aggregate gallium data.

## Authorization boundary

No fit, optimizer, likelihood evaluation, T1-T12 run, or numerical prediction is authorized by this document. The next scientific design must first resolve the owner decisions and create a separately versioned 6.4.0 model-development contract.
