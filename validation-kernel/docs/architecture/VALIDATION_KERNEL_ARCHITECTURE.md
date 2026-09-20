# Validation Kernel Architecture

Status: Step 03 methodology architecture. No LSC physics was changed and no numerical validation was executed.

## Design constraints

- Frozen evidence is immutable and content-addressed.
- Missing parameters remain missing.
- Validation data must never be used to reconstruct a frozen object.
- Model execution, likelihoods, baselines, and external vetoes remain separate layers.
- Negative and falsifying outcomes are first-class outputs.
- Every generated result must carry source, version, configuration, and hash provenance.

## Planned modules

| Module | Responsibility | Step 03 state |
|---|---|---|
| `frozen_core` | Authenticated equations, parameter schema, immutable manifests, and accepted frozen objects | E1-E12 descriptors, DAG, identity, contracts, quarantine, and fail-closed evaluator implemented; numerical prediction blocked |
| `data` | Versioned, licensed, hashed experiment inputs and transformations | 13 immutable dataset contracts implemented; source hashes verified; no raw write path |
| `likelihood` | Explicit likelihoods, covariance, nuisance handling, profiling/marginalization | metric, nuisance and covariance contracts implemented; numerical likelihood evaluation deferred |
| `baselines` | Null, normalization, cross-section/systematic, detector, sterile 3+1, and hierarchical competitors | M0-M6 contracts and stable aliases implemented; no scientific fit run |
| `lsc` | Thin evaluator interface around an adjudicated frozen object | Fail-closed specification evaluator implemented; no full numerical evaluator exists |
| `validation` | Preregistered T1-T12 harness, hold-outs, transfer tests, sensitivity analysis | canonical T1-T12, split policy and deterministic dry-run plans implemented; execution remains unauthorized |
| `external_veto` | KATRIN, IceCube, solar, and other independently sourced constraints | KATRIN/IceCube loaders and mapping gates implemented; both vetoes blocked by missing mappings |
| `reporting` | Machine-readable results, epistemic labels, provenance, failure retention | reporting policy, future result schema and execution-manifest schema implemented; no result instantiated |
| `tests` | Unit, integration, determinism, provenance, and fail-closed regression tests | contract, integrity, no-refit, T12, BEST-2, external mapping, deterministic planning and golden methodology tests implemented |

## Dependency boundary

`frozen_core` is the gate for every later computational module. A later evaluator may depend on an adjudicated `AUTHENTIC_FROZEN` object or a deterministic `DERIVED_FROM_FROZEN` representation. It may not depend on a `HISTORICAL_POST_DATA`, `UNVERIFIED`, or `MISSING` object as though it were frozen.

The present gate permits a specification evaluator but blocks an authentic numerical LSC 6.3.0 prediction. It does not block future development of a clearly new, preregistered model version after an explicit design decision.

## Provenance flow

1. Preserve source bytes and Git objects.
2. Hash and inventory candidates.
3. Establish commit, parent, timestamp, author, and data-exposure context.
4. Adjudicate exactly one official classification per candidate.
5. Admit only authenticated or deterministic derived objects into `frozen_core`.
6. Report conflicts and missing fields without automatic substitution.

## Explicitly deferred

- numerical likelihood implementation;
- numerical baseline implementations and fits;
- scalar or tensor evaluator code;
- parameter fitting;
- BEST-2 prediction;
- physics validation tests;
- any T1-T12 numerical execution until a separately authorized, complete frozen bundle and test-specific blockers are resolved.
