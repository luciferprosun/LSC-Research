# LSC Validation Kernel companion artifact

This package is the separately prepared reproducibility and validation
infrastructure companion to the LSC 6.5.0 scientific-model artifact. It keeps
the kernel, tests, audit methods, preregistration, and historical decision
trail distinct from the model-only Zenodo package.

## Identity and scope

- Validation Kernel software/package version: `0.6.0`;
- related frozen scientific model: LSC `6.5.0`;
- related model SHA-256:
  `c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8`.

The companion supports deterministic reproduction, fail-closed validation
inputs, audit evidence, and future separately authorized Phase-2 execution.
It is not itself an experimental result and does not imply validation.

## Reproduce

Use Python 3.11 and `requirements-step07e.lock`. The author-hosted Bahcall
table is intentionally not redistributed. Run the explicit hash-verifying
acquisition utility before model reproduction:

```text
python tools/acquire_bahcall_1997_payload.py
python tools/reproduce_lsc650.py
python -m pytest -q
```

Check `MANIFEST.json` and `SHA256SUMS.txt` before use.

The default public-package test target is the 12-case STEP 08 closure suite.
The retained historical integration tests require the non-redistributed local
evidence archive; their complete local run is kept in the final STEP 08
source-audit record outside this self-checksummed export.

## Governance boundary

Phase 2 was not executed. The primary future sequence remains
`T11 -> T7 -> T3 -> T1 -> T10`, with stop rules and limitations fixed in
`PHASE_2_VALIDATION_HANDOFF.md`. BEST-2 remains `FUTURE_ONLY` and
`FUTURE_BLIND`, with no observed-data access and no prediction.

This companion is planned as a separate linked Zenodo record. No upload,
public release, or DOI mint has occurred.
