# Model card: LSC 6.5.0

## Identity

- Model: LSC 6.5.0, `EXACT_FINITE_A2/C/A`
- Canonical model SHA-256:
  `c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8`
- Physical parameters: exactly one, universal dimensionless `alpha_0`
- Frozen value: `-0.14388795521516184`
- Profile-Delta-chi-square-one interval:
  `[-0.19024973740805776, -0.10233891434687088]`
- Status: parameter frozen; not experimentally validated

## Model

The model transforms only the energy argument of the frozen gallium capture
cross section:

`E' = E exp(alpha_0)`

`K_m(E; alpha_0) = sigma_m(E') / sigma_m(E)`

`R_pred,a(alpha_0) = <K_m(E; alpha_0)>_a`

The baseline measure already contains exactly one conventional `sigma(E)`.
Multiplication by `K_m` replaces it with exactly one `sigma(E')`. Source-line
energies, source spectrum, geometry, detector response, exposure, conventional
probability, and nuisance physics are not dilated.

## Scope and safeguards

The production model has no tensor, preferred axis, anisotropic amplitude,
second physical coefficient, or experiment-, isotope-, zone-, exposure-, or
run-specific `alpha_0`. Inputs outside frozen cross-section support fail with
`FAIL_CLOSED_UNSUPPORTED_DOMAIN`; extrapolation and clipping are forbidden.
The frozen parameter bundle has `no_refit=true`.

## Development evidence

The parameter was determined from one BEST inner-zone published aggregate
ratio under a diagonal published-total-uncertainty approximation. Labels are
`MODEL_EXPOSED`, `POST_6_4_DEVELOPMENT`, `RETROSPECTIVE_NON_BLIND`, and
`DEVELOPMENT_DATA`. There is one independent development observable, one
fitted physical parameter, zero fitted nuisances, and zero effective residual
degrees of freedom. The near-zero objective is structurally expected and is
not goodness-of-fit or validation evidence.

BEST outer, GALLEX/GNO, SAGE, and BEST-2 were absent from the parameter
objective. Historical experiments are model-exposed and not strict blind
holdouts. BEST-2 remains `FUTURE_ONLY` and `FUTURE_BLIND`; no observed BEST-2
data were accessed and no prediction was generated.

## Intended use

The artifact supports reproducible evaluation, independent retrospective
validation under a frozen Phase-2 protocol, and a later separately authorized
prospective freeze. It may be described as explicitly specified, executable,
reproducible, parameter-frozen, and ready for independent retrospective
validation.

## Prohibited interpretation

It is not evidence of discovery, confirmation, blind validation, directional
or anisotropic physics, or confirmation/exclusion by BEST, GALLEX/GNO, SAGE,
BEST-2, KATRIN, or IceCube. The interval is
`ASSUMPTION_BASED_SENSITIVITY_ONLY`, not collaboration-equivalent inference.

## Reproducibility and external material

Use `tools/acquire_bahcall_1997_payload.py` when the publication artifact omits
the cross-section transcription for license safety, then run
`tools/reproduce_lsc650.py`. See `THIRD_PARTY_NOTICES.md` and the frozen
provenance manifest.
