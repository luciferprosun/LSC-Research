# LSC Validation Kernel and LSC 6.5.0

This repository export contains the public-ready Validation Kernel source,
tests, audit trail, and the frozen LSC 6.5.0 exact finite-dilation model. Phase
1 is complete; experimental validation has not yet been performed.

## Version lines

- Validation Kernel software/package: `0.6.0`;
- scientific model: LSC `6.5.0`;
- model SHA-256:
  `c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8`.

These are intentionally independent version namespaces.

## Install and verify

Use Python 3.11 and the pinned environment in `requirements-step07e.lock`.
The public export does not redistribute the Bahcall 1997 table because its
redistribution permission is unclear. Acquire and hash-verify it explicitly:

```text
python tools/acquire_bahcall_1997_payload.py
```

Then run the frozen reproduction and tests:

```text
python tools/reproduce_lsc650.py
python -m pytest -q
```

The reproduction must report the canonical model hash, parameter bundle,
frozen parameter/interval, and `29/29` golden vectors. `MANIFEST.json` and
`SHA256SUMS.txt` bind this export.

The publication-safe default test configuration runs the STEP 08 closure
suite. Older integration tests are retained as audit source, but some require
the large historical evidence archive and third-party mirrors that are
deliberately not redistributed.

## Scientific boundary

LSC 6.5.0 has one universal parameter and applies the exact response
`sigma(E exp(alpha_0)) / sigma(E)`. The parameter estimate is retrospective,
non-blind, and sensitivity-only. It is not experimental validation or
confirmation. The immutable LSC 6.4.0 failed parameter gate remains preserved.

Phase-2 validation requires separate authorization and must follow
`PHASE_2_VALIDATION_HANDOFF.md`. BEST-2 remains future blind; no observed data
were accessed and no prediction was generated.

## Publication and licensing

The LSC 6.5.0 model is published as Zenodo version DOI
`10.5281/zenodo.22007108` in concept lineage
`10.5281/zenodo.19780615`. The Validation Kernel remains a separate,
unpublished companion pending creator confirmation. No GitHub Release or
Phase-2 execution occurred. `LICENSE` applies to original project
code/documentation; `THIRD_PARTY_NOTICES.md` records source-specific provenance
and terms.
