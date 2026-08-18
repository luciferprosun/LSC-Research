# LSC 6.5.0 exact finite-dilation model

This is the publication-prepared scientific-model artifact for LSC 6.5.0.
It is explicitly specified, executable, reproducible, and parameter-frozen.
It has **not** been experimentally validated, and no Phase-2 validation was
performed while preparing this package.

## Identity

- scientific model version: `6.5.0`;
- model profile: `EXACT_FINITE_A2/C/A`;
- model SHA-256:
  `c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8`;
- universal parameter: `alpha_0 = -0.14388795521516184`;
- parameter-bundle SHA-256:
  `617d72a303a947e8e7467efb3c745f7e44dc1c07eab7d830a90dbfd179da5c18`;
- supporting Validation Kernel software/package line: `0.6.0`.

The package version and scientific-model version are intentionally separate
version namespaces.

## Model

Only the capture-cross-section argument is dilated:

`E' = E exp(alpha_0)`

`K_m(E; alpha_0) = sigma_m(E') / sigma_m(E)`

`R_pred,a(alpha_0) = <K_m(E; alpha_0)>_a`

There is exactly one LSC physical parameter, shared across all experiments,
isotopes, and zones. Tensor, preferred-axis, and anisotropic sectors are
disabled. Refitting is forbidden for this model version.

## Reproduce

Use Python 3.11 with the dependencies pinned in `requirements-step07e.lock`.
The Bahcall 1997 table is omitted because no explicit redistribution license
was located. Materialize it explicitly with:

```text
python tools/acquire_bahcall_1997_payload.py
```

The acquisition utility verifies both the exact author-hosted source and the
frozen output SHA-256 before creating the file. Then run:

```text
python tools/reproduce_lsc650.py
```

The expected receipt is `status=PASS`, `29/29` golden vectors, the frozen
parameter and interval, and the canonical model/bundle hashes above. See
`docs/model/LSC_6_5_0_REPRODUCTION_INSTRUCTIONS.md` and the STEP 08 audit
reports for detail.

## Evidence boundary

The parameter determination used one historically exposed BEST inner-zone
aggregate and is `RETROSPECTIVE_NON_BLIND_PARAMETER_DETERMINATION`. Its
covariance classification is `ASSUMPTION_BASED_SENSITIVITY_ONLY`. The zero
effective residual degrees of freedom mean that the near-zero objective is
not goodness-of-fit or validation evidence.

BEST-2 remains `FUTURE_ONLY` and `FUTURE_BLIND`: observed data accessed **NO**,
prediction generated **NO**. KATRIN and IceCube mappings are not established.

## Integrity, citation, and license

Verify `SHA256SUMS.txt` and `MANIFEST.json` before use. Cite this artifact and
the external scientific sources in `THIRD_PARTY_NOTICES.md`. The MIT license
covers original code/documentation only; source-specific terms continue to
apply to external material.

Publication state: prepared, not uploaded, no DOI minted.
