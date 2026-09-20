# LSC 6.5.0 release notes

LSC 6.5.0 is the exact finite-dilation successor to the failed LSC 6.4.0
linear development gate. It is an audited, executable, reproducible,
one-parameter scientific artifact. It has not yet been experimentally
validated.

## Historical lineage

- **6.3.0:** the historical release identity, symbolic equations, commit, and
  Zenodo lineage are preserved. Its complete numerical state is incompletely
  recoverable, so historical numerical reproduction is not claimed.
- **6.3.1:** `ABANDONED_BEFORE_RELEASE`; it never became an executable release.
- **6.4.0:** the frozen linear A2 parameter determination ended with
  `DEVELOPMENT_PARAMETER_DETERMINATION_FAILED`. This adverse result is
  immutable and remains part of the 6.5.0 package.
- **6.5.0:** a new, owner-authorized exact finite-dilation physical successor;
  it is not a repair or relabeling of 6.4.0.

## Frozen model

Only the gallium capture-cross-section argument is transformed:

`E' = E exp(alpha_0)`

`K_m(E; alpha_0) = sigma_m(E') / sigma_m(E)`

`R_pred,a(alpha_0) = <K_m(E; alpha_0)>_a`

There is exactly one universal physical parameter. Tensor, directional,
anisotropic, preferred-axis, per-experiment, per-isotope, and per-zone sectors
are disabled. The frozen value is `alpha_0 = -0.14388795521516184`; refitting
is permanently forbidden for this model version.

## Development and inference boundary

The parameter determination used only the published BEST inner-zone aggregate
ratio. It is permanently classified
`RETROSPECTIVE_NON_BLIND_PARAMETER_DETERMINATION`. The diagonal covariance and
published aggregate uncertainty support only
`ASSUMPTION_BASED_SENSITIVITY_ONLY` inference. With one observable fitted by
one parameter, the effective residual degrees of freedom are zero; the
near-zero objective is expected by construction and has no goodness-of-fit or
validation meaning.

BEST outer, GALLEX/GNO, and SAGE were not used in the 6.5.0 objective, but they
are historically exposed and are not strict blind tests. BEST-2 remains
`FUTURE_ONLY` and `FUTURE_BLIND`: observed data accessed **NO**, prediction
generated **NO**.

## Release boundary

Allowed claims include explicitly specified, executable, reproducible,
parameter-frozen, retrospective parameter determination completed, ready for
independent retrospective validation, and prospectively freeze-capable.
Claims of experimental validation, confirmation, discovery, blind
confirmation, or directional evidence are prohibited.

The prepared publication artifacts have not been pushed, released, uploaded,
or assigned a new DOI. Phase-2 validation is a separate future action.
