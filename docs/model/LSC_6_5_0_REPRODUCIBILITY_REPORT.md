# LSC 6.5.0 reproducibility report

Status: **PASS - RC1 ready for independent final audit**

## Frozen identities

- model version: `6.5.0`;
- configuration: `EXACT_FINITE_A2/C/A`;
- model SHA-256: `c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8`;
- parameter bundle SHA-256: `617d72a303a947e8e7467efb3c745f7e44dc1c07eab7d830a90dbfd179da5c18`;
- cross-section payload SHA-256: `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5`;
- source-line payload SHA-256: `ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e`;
- scientific specification SHA-256: `114e8398a45e6a6c8fb4a105e994ca695805b06b9ed8608b86288ea0791ef948`.

## Environment

The completed run used Python 3.12.3, NumPy 2.5.2, SciPy 1.18.0, pytest 9.1.1, and scipy-openblas 0.3.34.0.0 on Linux x86_64/glibc 2.39. There is no stochastic computation. Exact versions and numeric policy are in `requirements-step07e.lock` and `LSC_6_5_0_ENVIRONMENT_LOCK.json`.

## Reproduced objects

The read-only reproduction verified:

- the complete canonical model-hash rule and all component hashes;
- 29/29 golden vectors;
- production/reference agreement;
- the source-support-derived domain;
- the independent exact objective;
- `alpha_0 = -0.14388795521516184`;
- profile-Delta-chi-square-one interval `[-0.19024973740805776, -0.10233891434687088]`;
- interior boundary status and one-dimensional identifiability;
- frozen no-refit parameter bundle;
- immutable LSC 6.4.0 adverse-result record;
- no BEST-2 access or prediction;
- no publication action.

Two repository-profile executions produced bitwise-identical canonical receipts. Two release-candidate-profile executions independently produced bitwise-identical canonical receipts. Floating outputs from the production and independent implementations agree within frozen golden tolerances; all serialized receipts are bitwise identical.

## Execution-incident disclosure

Two attempts aborted after the optimizer was invoked but before a result object was constructed, serialized, returned, or printed. The cause was JSON-style `false` literals in Python result construction. The invisible outputs were not used. Each superseded pre-fit freeze and incident is preserved. The only repair was replacement with Python `False` plus an AST gate; scientific equations, payloads, data, likelihood, covariance, bounds, optimizer, and failure rules remained unchanged and were re-frozen before the one completed determination.

The write-once result path now exists and rejects any second completed execution. Reproduction uses a pure read-only recalculation and never calls the write-once function.

## Release-candidate profile

The RC contains a publication-safe execution provenance manifest and retains the original source-hash manifest separately. It does not redistribute the archived source publications. DOI/official URLs and hashes preserve source provenance; no independent relicensing is asserted.

The RC manifest and `SHA256SUMS.txt` pass. Python bytecode and cache artifacts are excluded, and the reproduction script disables bytecode writes.

## Known scientific limits

This report establishes software and numerical reproducibility, not scientific validation. The determination is retrospective and `SENSITIVITY_ONLY` under `COV_DIAGONAL`; full collaboration covariance is unavailable. No Phase-2 holdout statistic, external veto, directional test, or BEST-2 prediction was run.
