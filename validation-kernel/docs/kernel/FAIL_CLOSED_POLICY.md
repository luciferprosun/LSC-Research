# Fail-Closed Policy

## Governing rule

Missing authentic frozen numerical information causes an explicit execution failure. It never causes an inferred, default, interpolated, fitted, or historical numerical prediction.

## Central provenance admission

All admission decisions are implemented in `src/lsc_kernel/frozen/provenance.py`.

| Registry status | Symbolic/specification use | Frozen numerical use |
|---|---:|---:|
| `AUTHENTIC_FROZEN` | allowed | allowed only when the registry object itself is a hashed numerical artifact |
| `DERIVED_FROM_FROZEN` | allowed for deterministic non-numerical representations | rejected unless a later explicit policy proves a value-preserving numerical derivation |
| `HISTORICAL_POST_DATA` | evidence only | rejected |
| `UNVERIFIED` | evidence only | rejected |
| `MISSING` | absence record only | rejected |

Claim labels `UNVERIFIED_CONFLICT`, `TOY`, `ILLUSTRATIVE`, and `DEPRECATED` are always rejected as frozen numerical provenance.

An authentic Markdown specification is not a numerical parameter source. This prevents a bundle from citing the correct document while inserting an unsupported value.

## Historical quarantine

`frozen_core/manifests/HISTORICAL_ARTIFACT_QUARANTINE.json` contains every Step 01 post-data and unverified candidate, including:

- toy `c0=0.808281` and `c1=0.012500` and their post-data generator;
- LSC 6.2.1 five-anchor coefficients and fit implementation;
- LSC 5.5 tensor inputs and optimized alpha;
- LSC 6.0 toy amplification/scenarios;
- LSC 6.2 illustrative `delta approximately 0.05`;
- deprecated 4.x numerical configuration;
- both unverified cross-version mappings.

These bytes remain provenance evidence. Quarantine means non-admission, not deletion.

## Explicit blockers

The kernel exposes distinct error types for identity mismatch, missing parameters, bad provenance, unknown units, unknown frames, missing orientation, incomplete tensors, blocked equations, post-data artifacts, unverified candidates, unauthorized prediction, and unauthorized validation.

CLI exit codes are:

| Code | Meaning |
|---:|---|
| 0 | inspection or validation command completed successfully |
| 2 | authentic frozen bundle or execution contract is incomplete |
| 3 | provenance was rejected |
| 4 | input is malformed or inconsistent |

## Prediction and validation gates

The current evaluator can load and inspect the symbolic model. It cannot authorize a full numerical prediction because the parameter, unit, frame, and tensor contracts are incomplete.

T1-T12 are interfaces only and all carry `SPECIFICATION_INCOMPLETE`. T12 additionally requires precise timing, surveyed orientation, sufficient geometry, a complete active tensor, and all required reference frames. An exposure midpoint is explicitly rejected as a substitute for event time.

## Prohibited recovery methods

No Step 02 path invokes optimization, fitting, interpolation, parameter search, data-derived reconstruction, or a fallback to LSC 4.x, 5.5, 6.0, 6.2, or 6.2.1.
