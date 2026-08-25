# LSC Validation Kernel and LSC 6.5.0

LSC Validation Kernel is the reproducibility, provenance, execution, and
validation infrastructure for the LSC model line. This GitHub snapshot
contains the publication-safe kernel source, tests, audit trail, and frozen
LSC 6.5.0 exact finite-dilation model.

## Phase 1 release state

The current frozen scientific model artifact is **LSC 6.5.0**. It is:

- executable;
- parameter-frozen;
- independently audited;
- reproducible;
- published as a version-specific Zenodo record;
- **not yet experimentally validated**.

Phase 1 is complete. The frozen model artifact is published on Zenodo as
[version DOI `10.5281/zenodo.22007108`](https://doi.org/10.5281/zenodo.22007108)
within concept lineage `10.5281/zenodo.19780615`. No GitHub Release, final tag,
Validation Kernel Zenodo publication, BEST-2 prediction, or Phase 2 execution
is implied by this repository snapshot.

The Validation Kernel software/package version (`0.6.0`) and scientific model
version (`6.5.0`) are intentionally independent version lines. The frozen
model SHA-256 is
`c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8`.

## Core LSC 6.5.0 model

Only the capture-cross-section argument is dilated:

```text
E' = E exp(alpha_0)
K(E; alpha_0) = sigma(E') / sigma(E)
R_pred = <K>
```

Exactly one universal physical parameter is active. Its frozen value is
`alpha_0 = -0.14388795521516184`. Tensor, anisotropy, and preferred-axis
sectors are disabled. Per-experiment, per-isotope, and per-zone variants are
prohibited, and the permanent no-refit policy applies to this model version.

## Historical boundary

- **LSC 6.3.0** is the preserved historical frozen identity. Its symbolic
  specification and provenance survive, but its complete numerical state is
  not recoverable from the available authenticated evidence.
- **LSC 6.3.1** was `ABANDONED_BEFORE_RELEASE` because completion required new
  physical choices rather than a patch-level reconstruction.
- **LSC 6.4.0** was the owner-authorized linear development attempt. Its
  adverse result, `DEVELOPMENT_PARAMETER_DETERMINATION_FAILED`, remains
  immutable.
- **LSC 6.5.0** is the separately versioned exact finite-dilation successor;
  it is not a repaired or relabelled historical object.

See [the release notes](RELEASE_NOTES_LSC_6_5_0.md) and
[version history](docs/scientific/LSC_VERSION_HISTORY_DRAFT.md) for the concise
lineage.

## Validation boundary

- Phase 1 specification, freeze, independent audit, and publication
  preparation are complete.
- Phase 2 validation has **not** been executed.
- Historical development results are retrospective and non-blind.
- BEST-2 remains `FUTURE_ONLY` and `FUTURE_BLIND`: observed data were not
  accessed and no prediction was generated.
- Phase 2 requires separate authorization and must follow
  [the frozen handoff](PHASE_2_VALIDATION_HANDOFF.md).

## Install and reproduce

Use Python 3.12 and the pinned environment in `requirements-step07e.lock`.
The Bahcall 1997 table is not redistributed because its redistribution
permission is unclear. Acquire and hash-verify it explicitly:

```bash
python tools/acquire_bahcall_1997_payload.py
```

Then run the frozen reproduction and publication-safe tests:

```bash
python tools/reproduce_lsc650.py
python -m pytest -q
```

The reproduction verifies the canonical scientific hashes, frozen parameter
and interval, independent evaluator agreement, and all `29/29`
golden/fail-closed vectors. `MANIFEST.json` and `SHA256SUMS.txt` bind this
snapshot.

Further reading:

- [Phase 1 final master report](PHASE_1_FINAL_MASTER_REPORT.md)
- [RC reproduction instructions](docs/model/LSC_6_5_0_REPRODUCTION_INSTRUCTIONS.md)
- [Phase 2 validation handoff](PHASE_2_VALIDATION_HANDOFF.md)
- [BEST-2 prospective handoff](BEST2_PROSPECTIVE_HANDOFF.md)
- [Development disclosure](LSC_6_5_0_DEVELOPMENT_DISCLOSURE.md)

## Contributors and dedication

Current project and Validation Kernel metadata recognize **LINZ HOSS** for
conceptual discussion, intellectual feedback, and contribution to the
conceptual development environment of the LSC research program. This does not
attribute code, equations, numerical fits, validation experiments, or
datasets. Separate from scientific claims, the project acknowledges LINZ HOSS
as an important inspiration in LSC's development history. See the
[contribution record](docs/project/LINZ_HOSS_CONTRIBUTION.md).

## Licensing and provenance

`LICENSE` applies to original project code and documentation.
`THIRD_PARTY_NOTICES.md` records external scientific provenance and
source-specific terms. The complete local RC1 and historical evidence archive
are not redistributed in this sanitized GitHub snapshot.

## LSC Evidence Chain

The repository is protected by an append-only, file-level SHA-256 evidence
chain with CI verification. See [the evidence protocol](evidence-chain/README.md)
and [research attribution boundary](RESEARCH_ATTRIBUTION.md). The chain records
integrity and chronology without changing the MIT license or scientific status.
