# STEP 07E RESULT

Project: LSC Validation Kernel
Status: **PASS**

Verdict: **LSC_6_5_0_EXECUTABLE_RC1_READY_FOR_FINAL_AUDIT**

This verdict means that the owner-authorized exact finite-dilation successor is explicitly specified, executable, parameter-frozen, independently reproducible, and packaged as RC1. It does not mean that LSC 6.5.0 has been scientifically validated or confirmed.

## A. Owner authorization

`OWNER_AUTHORIZATION_LSC_6_5_0.md` records `OWNER AUTHORIZATION: APPROVED` for the exact A2/C/A profile:

- Candidate X: only the gallium capture-cross-section argument is dilated;
- tensor and anisotropic sectors are disabled;
- one universal response law and one universal physical parameter are used;
- Candidate Y, experiment-specific coefficients, and any preferred axis are not authorized.

Authorization SHA-256: `6731100c50b1a35e8c0772f4ebc4130278edbbef72e618264e37a5b5cc6ef163`.

## B. LSC 6.5.0 scientific specification

The canonical source remains `spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml`, SHA-256 `114e8398a45e6a6c8fb4a105e994ca695805b06b9ed8608b86288ea0791ef948`.

LSC 6.5.0 is classified `NEW_POST_6_4_PHYSICAL_SUCCESSOR`. It is not a recovered numerical 6.3.0 model, is not the abandoned 6.3.1 release, and is not a 6.4.1 repair. The production profile has exactly one physical parameter, no tensor, no preferred axis, no anisotropic amplitude, and no experiment-, isotope-, or zone-specific LSC coefficients.

The pre-outcome scientific freeze is `LSC_6_5_0_SCIENTIFIC_FREEZE.json`, SHA-256 `f32e606e37f5e880240b446737c2e72a30395b9017c7479e20ca7bc4ebcdc0df`.

## C. Exact finite response

The implemented scientific kernel is

`E' = E exp(alpha_0)`,

`K_m(E;alpha_0) = sigma_m(E') / sigma_m(E)`,

`S_m(E;alpha_0) = K_m(E;alpha_0) - 1`,

`R_pred,a(alpha_0) = integral K_m(E;alpha_0) dnu_a / integral dnu_a`.

The baseline measure contains exactly one conventional `sigma(E)`. Multiplication by the exact ratio replaces that single factor with `sigma(E exp(alpha_0))`; regression tests reject missing or double-counted cross sections. No derivative approximation is used in production prediction. The derivative appears only in the first-order lineage test against LSC 6.4.0.

Hard invariants pass: `K(E,0)=1`, `S(E,0)=0`, `R_pred(0)=1`, positivity within support, the first-order limit, and scale-transform composition at the scientific-kernel level.

## D. Cross-section payload

The unchanged frozen scenario is `BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE`:

- cross-section payload SHA-256: `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5`;
- 51Cr/37Ar source-line payload SHA-256: `ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e`;
- support: `[0.24, 30.0] MeV`;
- interpolation: natural cubic spline in linear energy and cross section;
- extrapolation and silent clipping: forbidden.

The evaluator verifies hashes, positivity, knot ordering, support, and authoritative line identity. The RC carries publication-safe provenance and hashes but does not redistribute archived source publications or assert a new license over them.

## E. Domain

The domain was deterministically rederived before determination from every active 51Cr/37Ar line and the frozen payload support:

`max_i ln(0.24/E_i) <= alpha_0 <= min_i ln(30.0/E_i)`.

Frozen closed domain: `[-0.5747389495096434, 3.607238025076703]`.

It is `DATA_INDEPENDENT_SOURCE_SUPPORT_DERIVED`; neither the failed 6.4 result nor the later 6.5 estimate influenced it. Unsupported transformed energies fail closed. A one-ULP endpoint normalization is allowed only when the mathematically closed endpoint is detected explicitly and is reported in the result.

## F. Evaluator

`LSC650Evaluator` is deterministic, provenance-bound, hash-verifying, free of hidden defaults and fitting, and uses the exact ratio. It requires explicit source lines and context, returns per-line transformed energies and kernels, and rejects malformed, unversioned, extrapolated, tensor, axis, anisotropic, second-coefficient, and unknown-response inputs.

`alpha_0` is loaded explicitly or from the frozen bundle; after bundle freeze, refit is forbidden across experiments, isotopes, zones, runs, and future supported inputs.

## G. Independent reference

The independent reference evaluator uses a separate standard-library natural-spline and integration implementation; it does not call the production ratio or integration path. Production/reference comparisons pass across both isotopes, an alpha grid, golden cases, and boundary-adjacent inputs.

## H. Golden vectors

`spec/LSC_6_5_0_GOLDEN_VECTORS.json`, SHA-256 `27a7bcab3a77bf1d9832e63388bf5df913c41d7848e5a3abd4f0adc0f293988f`, contains 29 cases:

- 20 numerical cases covering null, small and moderate signed alpha, 51Cr, 37Ar, mixed weights, multiple context labels, and boundary vicinity;
- 9 fail-closed cases covering domain, source-line/hash, unsupported response/profile, and forbidden anisotropic inputs.

Result: **PASS 29/29**. Expected numerical values come from the independent implementation rather than a snapshot of the production evaluator.

## I. Parameter protocol

The pre-fit protocol is `LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json`, SHA-256 `bf05812385439b0c82a53ed9bf52a26b65b6b8925903fab4f04e6d4d5a67a56c`.

It freezes BEST-inner published aggregate data only, exact dataset hashes, diagonal Gaussian chi-square, `COV_DIAGONAL`, no profiled nuisance, source-support bounds, deterministic bounded scalar optimization, convergence and boundary criteria, a profile-Delta-chi-square-one interval, identifiability checks, failure rules, and permanent no-refit policy.

The data are permanently labelled `MODEL_EXPOSED`, `POST_6_4_DEVELOPMENT`, `RETROSPECTIVE_NON_BLIND`, and `DEVELOPMENT_DATA`. BEST outer, GALLEX/GNO, SAGE 51Cr, SAGE 37Ar, and BEST-2 were excluded from the determination.

## J. Pre-fit freeze

The completed run is bound to `LSC_6_5_0_PREFIT_FREEZE.json` revision 3, SHA-256 `7a0fdacd8fcff134386e4864228554454237ddc8da3df2429effa4b3f23403e0`.

All hard gates passed before the completed determination: authorization, exact response, scientific and payload hashes, domain, schemas, deterministic evaluator, 29/29 goldens, independent reference, exact baseline accounting, frozen protocol/data/covariance/bounds/environment, immutable 6.4 adverse record, and BEST-2 non-access.

Two earlier software attempts invoked the optimizer but aborted before result-object construction, serialization, return, printing, or file creation because JSON-style `false` literals were present in Python result construction. No optimizer outcome was exposed or used. Both superseded freezes and both incident records are retained. The only repair was replacing those literals with Python `False` and adding an AST pre-fit gate. No equation, payload, datum, objective, covariance, bound, optimizer, or failure rule changed. Revision 3 was re-frozen before the single completed scientific determination.

## K. alpha_0 determination

- estimate: `-0.14388795521516184`;
- profile `Delta chi-square = 1` interval: `[-0.19024973740805776, -0.10233891434687088]`;
- objective: `2.169792942258529e-20`;
- objective at null: `17.47239999999999`;
- optimizer: `scipy.optimize.minimize_scalar`, bounded;
- evaluations / iterations: `20 / 20`;
- convergence: **PASS**;
- boundary: **INTERIOR**;
- identifiability: **IDENTIFIABLE_ONE_DIMENSIONAL**;
- objective curvature: `1030.133948537873`;
- completed determination count: `1`;
- classification: `RETROSPECTIVE_NON_BLIND_PARAMETER_DETERMINATION` and `ASSUMPTION_BASED_SENSITIVITY_ONLY`.

The result is parameter development, not validation. No unconstrained diagnostic was run because it was not preregistered.

## L. Parameter bundle

`LSC_6_5_0_PARAMETER_BUNDLE.json` is frozen with SHA-256 `617d72a303a947e8e7467efb3c745f7e44dc1c07eab7d830a90dbfd179da5c18`.

It contains one dimensionless universal `alpha_0`, its domain and profile interval, response/payload/protocol/data/pre-fit/result bindings, exposure labels, and `no_refit=true`. No boundary solution or optimum from LSC 6.4.0 was imported.

## M. Model hash

Canonical model SHA-256: `c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8`.

It is derived from a canonical JSON identity containing model version/configuration and hashes of the scientific specification/freeze, owner authorization, payloads, parameter bundle/schema, evaluator/cross-section/contracts sources, prediction schemas, golden vectors, and environment lock.

## N. Retrospective smoke

A technical end-to-end schema smoke test passed after parameter freeze. It loaded no observed holdout outcome, computed no holdout statistic, and caused no parameter change. Its `R_pred` output is retained solely as pipeline evidence and has no allowed compatibility, fit-quality, validation, confirmation, or exclusion interpretation.

## O. BEST-2

BEST-2 remains `FUTURE_ONLY` and `FUTURE_BLIND`. Observed data accessed: **NO**. Prediction generated: **NO**. Prediction authorized in STEP 07E: **NO**. Only schema capability was checked.

## P. RC1

Release candidate: `release_candidate/LSC-6.5.0-rc1/`.

It contains the scientific and owner records, exact implementation and independent reference, sanitized external-physics provenance, schemas, frozen parameter/result/protocol/pre-fit objects, goldens, model identity/hash, environment lock, disclosures, reproduction tools, manifest, and checksums.

- RC file count at final package verification: `52`;
- `MANIFEST.json` SHA-256: `5118142cb11e91c3102ffa34157094bac5fba75ff0528bfda4be1e4c81772c0f`;
- `SHA256SUMS.txt` SHA-256: `87212f2645fd8375b000777b3fdbc21b7a1cf45bd4d743511a6ac64192cff5e8`;
- `sha256sum -c SHA256SUMS.txt`: **PASS**;
- publication-safety scan: **PASS**, zero critical secret, absolute-local-path, private-URL, cache/temp, or original-publication redistribution findings.

No publication, push, tag, release, DOI mint, or announcement occurred.

## Q. Reproducibility

The environment is frozen to Python 3.12.3, NumPy 2.5.2, SciPy 1.18.0, pytest 9.1.1, scipy-openblas 0.3.34.0.0, IEEE-754 binary64, and deterministic non-stochastic execution.

`make reproduce-650` verifies hashes, the immutable 6.4 adverse record, exact domain, 29 golden cases, reference agreement, read-only alpha reproduction, parameter bundle, model hash, and RC integrity without downloading unversioned data.

- two repository-profile reproductions: **BITWISE_IDENTICAL** receipts;
- two RC-profile reproductions: **BITWISE_IDENTICAL** receipts;
- reproduced alpha, interval, bundle hash, model hash, and RC manifest: **PASS**.

## R. Development disclosure

`LSC_6_5_0_DEVELOPMENT_DISCLOSURE.md` records the complete adverse lineage, the post-6.4 scientific decision, the one development datum, excluded historical holdouts, permanent exposure labels, two pre-result software incidents, no-refit boundary, and permitted/prohibited claims.

The 6.4 linear A2 parameter-determination failure remains a shipped scientific artifact; it is neither deleted nor reframed as an implementation failure.

## S. Tests

- STEP 07E focused suite: **24 passed, 4 subtests passed**;
- full repository suite: **268 passed, 28 subtests passed**;
- golden vectors: **29/29 PASS**;
- production/reference agreement: **PASS**;
- numerical stability and exact-support tests: **PASS**;
- deterministic repository and RC reproductions: **PASS**;
- RC SHA-256 verification: **PASS**;
- historical archive SHA-256 verification: **PASS**;
- nested-repository integrity: **PASS**;
- `git diff --check`: **PASS**;
- `git fsck --no-dangling`: **PASS**;
- secret/path/publication-safety scan: **PASS**.

The first full-suite command used `PYTHONPATH=src` and failed during collection because repository-root test helpers were not importable. The canonical repository invocation `PYTHONPATH=src:.` then passed the full suite. This was an invocation correction, not a code or scientific change. Two generated baseline-control manifests touched by the suite were restored exactly to their pre-STEP-07E content.

## T. Historical integrity

- historical LSC 6.3.0 commit remains `6ffa07bdde533fcc2a550e36c762b8edd9236c47`;
- LSC 6.3.1 remains `ABANDONED_BEFORE_RELEASE`;
- LSC 6.4.0 remains `DEVELOPMENT_PARAMETER_DETERMINATION_FAILED`;
- `LSC_6_4_0_ADVERSE_RESULT_FREEZE.json` remains hash-bound at `0a45c0f3e03d1691d3f9141de6c9a2cc33a0ad7ed878422f045b8b7a714275bc`;
- the historical archive and nested source repository remain unchanged and clean;
- no 6.4 boundary value or failed optimum entered 6.5;
- STEP 07E is a successor implementation, not a rewrite of any historical release.

## U. Git state

- input HEAD: `c522e344f7c0e43352626a7e435099c1da174286`;
- branch: `main`;
- STEP 07E commit subject: `Step 07E: implement and freeze executable LSC 6.5.0 RC1`;
- final commit: the commit containing this report (`HEAD` after closure);
- push performed: **NO**;
- tag/release/publication performed: **NO**;
- final worktree: required to be clean after the closure commit.

## V. Remaining validation blockers

- full scientific Phase-2 validation has not been executed;
- collaboration covariance/likelihood remains unavailable, so the development interval is `SENSITIVITY_ONLY` under `COV_DIAGONAL`;
- historical holdouts are retrospective/non-blind under the existing exposure audit;
- T12 is outside the trace-only production profile because anisotropy is disabled;
- KATRIN and IceCube mappings remain unjustified and no external veto was run;
- BEST-2 requires a separate prospective authorization, authoritative inputs, prediction freeze, and continued non-access to observed results;
- independent publication, licensing/provenance, and claims audit remains required before any public action.

These are validation or publication blockers, not executable-model blockers.

## W. STEP 08 readiness

**READY FOR FINAL INDEPENDENT AUDIT: YES**

Recommended next step: STEP 08 should perform an independent, read-only audit of RC integrity, scientific/claim boundaries, licenses and external-source provenance, reproducibility on a clean environment, and GitHub/Zenodo packaging. It must not alter the response, payload, alpha, parameter bundle, or adverse-history record.
