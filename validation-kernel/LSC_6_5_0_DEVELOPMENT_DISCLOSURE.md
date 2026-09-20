# LSC 6.5.0 development disclosure

## Scientific lineage

LSC 6.5.0 is a new post-6.4 physical successor. It is not a recovered numerical LSC 6.3.0 object, not the abandoned 6.3.1 release, and not a patch to LSC 6.4.0.

LSC 6.4.0 implemented the owner-authorized linear A2 response and failed its preregistered parameter-determination gate because the optimum was boundary dominated. That adverse result is preserved verbatim in `LSC_6_4_0_ADVERSE_RESULT_FREEZE.json`. No 6.4 boundary value was promoted into 6.5.

The exact finite ratio already existed as a hash-frozen reference before the 6.4 determination, but its promotion to the production response was a new, owner-authorized 6.5 physical decision made after the 6.4 adverse result. It is therefore classified `NEW_POST_6_4_PHYSICAL_SUCCESSOR` and `POST_6_4_DEVELOPMENT`, not blind pre-existing physics.

## What changed

The linear response `alpha_0 d ln sigma/d ln E` was not repaired. LSC 6.5.0 instead defines a separately versioned exact scale transformation:

`K_m(E;alpha_0) = sigma_m(E exp(alpha_0)) / sigma_m(E)`.

Only the capture-cross-section argument is transformed. Source energies, activity, survival probability, detector response, efficiency, geometry, exposure, time, and nuisance parameters are not transformed.

## Data exposure

The single parameter was determined from one published BEST-inner aggregate ratio. Its permanent labels are:

- `MODEL_EXPOSED`;
- `POST_6_4_DEVELOPMENT`;
- `RETROSPECTIVE_NON_BLIND`;
- `DEVELOPMENT_DATA`.

BEST outer, GALLEX/GNO, SAGE 51Cr, SAGE 37Ar, and BEST-2 were excluded from the determination objective. The historical datasets are not promoted to strict blind status because earlier LSC development was already exposed to them.

BEST-2 remains `FUTURE_ONLY` and `FUTURE_BLIND`. No observed BEST-2 data were accessed and no BEST-2 prediction was generated in STEP 07E.

## Determination and limitations

The frozen development objective used the published BEST-inner value `0.791 +/- 0.05` with `COV_DIAGONAL`, no additional profiled nuisance, and a data-independent source-support domain. This is `ASSUMPTION_BASED_SENSITIVITY_ONLY`; it is not a collaboration-equivalent likelihood or validation claim.

The completed result is `alpha_0 = -0.14388795521516184` with the frozen profile-Delta-chi-square-one interval `[-0.19024973740805776, -0.10233891434687088]`. It is an interior, identifiable, retrospective development estimate.

Two attempts aborted after optimizer invocation but before result construction, serialization, return, or exposure because Python result dictionaries contained JSON-style boolean literals. Both incidents and both superseded pre-fit freezes are preserved. The repair changed only `false` to `False`, an AST gate was added, and all scientific and numerical bindings were re-frozen before the one completed determination. No unseen optimizer output influenced a scientific or methodological choice.

After parameter freeze, refitting by experiment, isotope, zone, run, or holdout is forbidden. Any later refit creates a new model-development version.

## Claim boundary

This package supports claims of explicit specification, deterministic execution, and reproducible retrospective parameter determination. It does not support claims that LSC is validated, confirmed, prospectively successful, directionally supported, compatible with KATRIN/IceCube, or confirmed by BEST-2.
