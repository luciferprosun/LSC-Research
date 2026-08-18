# Phase 1 final master report

Project: LSC Validation Kernel

Audit: STEP 08 — final independent audit and Phase 1 closure

Date: 2026-08-18

Status: **PASS**
Verdict: `PHASE_1_COMPLETE_LSC_6_5_0_PUBLICATION_READY`

This verdict means that LSC 6.5.0 is an audited, executable, reproducible,
parameter-frozen, publication-ready scientific artifact. It does **not** mean
that LSC has been experimentally validated. No Phase-2 test, BEST-2
prediction, public push, release, upload, or DOI mint occurred.

## 1. Frozen input and audit strategy

- input branch: `main`;
- input HEAD: `1f715b9b8777f89d17a84d340a24107531ccaed4`;
- input tree: `f812734327896a5e1d9b9887eb5a5953d597fdab`;
- input commit: `Step 07E: implement and freeze executable LSC 6.5.0 RC1`;
- release candidate: `release_candidate/LSC-6.5.0-rc1/`;
- initial tracked/index diff: none;
- initial `git diff --check`: PASS;
- initial `git fsck --no-dangling`: PASS.

At continuation start, ten untracked STEP 08 draft artifacts from the
interrupted audit were present. They were identified and copied to an isolated
resume area before use; none was treated as frozen scientific input. The
tracked tree and index exactly matched the input commit. The authoritative RC
and minimal third-path inputs were exported directly from the frozen commit
with `git archive`. Two clean RC exports were executed separately. Audit tools
did not mutate RC1 or any frozen scientific object.

The main filesystem was space-constrained, so the audit did not recursively
copy the multi-gigabyte historical archive. Heavy reproduction and historical
hash jobs were run sequentially. This resource strategy did not reduce audit
coverage.

## 2. Immutable model identity

| Object | Required and observed SHA-256 | Result |
|---|---|---|
| Scientific specification | `114e8398a45e6a6c8fb4a105e994ca695805b06b9ed8608b86288ea0791ef948` | PASS |
| Cross-section payload | `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5` | PASS |
| Source-line payload | `ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e` | PASS |
| Parameter protocol | `bf05812385439b0c82a53ed9bf52a26b65b6b8925903fab4f04e6d4d5a67a56c` | PASS |
| Pre-fit freeze | `7a0fdacd8fcff134386e4864228554454237ddc8da3df2429effa4b3f23403e0` | PASS |
| Parameter bundle | `617d72a303a947e8e7467efb3c745f7e44dc1c07eab7d830a90dbfd179da5c18` | PASS |
| Canonical model | `c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8` | PASS |

RC1 resolves to the same component hashes and canonical model object. The
production evaluator SHA-256 remains
`ab195449e68da7d4b19e5dbd45079add4fee0e154666d63e30d9381a59dccd8f`.
No scientific hash changed during STEP 08.

## 3. Scientific equation audit

The frozen model is exactly

`E' = E exp(alpha_0)`

`K_m(E; alpha_0) = sigma_m(E exp(alpha_0)) / sigma_m(E)`

`R_pred,a(alpha_0) = <K_m(E; alpha_0)>_a`.

The null is analytic and exact: at `alpha_0 = 0`, `E' = E`, every `K_m = 1`,
and `R_pred = 1`. Expansion gives

`K_m = 1 + alpha_0 E sigma'_m(E)/sigma_m(E) + O(alpha_0^2)`,

which reproduces the LSC 6.4.0 linear A2 generator. The independent bridge
passed for both Cr51 and Ar37 with maximum absolute difference
`5.122204552144778e-14`.

Production calls the exact finite ratio, not the derivative approximation.
Only the capture-cross-section argument is transformed. Authoritative
source-line energies, branching fractions, source spectrum, activity,
exposure, geometry, conventional probability, detector response, and
nuisance/covariance labels are unchanged. Tensor, anisotropy, direction, and
preferred axis are disabled. There is exactly one LSC physical parameter,
universally shared across experiments, isotopes, and zones.

Result: `SCIENTIFIC_EQUATION_AUDIT_PASS`.

## 4. Cross-section accounting

For conventional line prefactor `q_i`, the baseline is
`B_i = q_i sigma(E_i)`. The numerator is

`sum_i B_i sigma(E_i exp(alpha_0))/sigma(E_i)`

and therefore exactly equals `sum_i q_i sigma(E_i exp(alpha_0))`. The
denominator remains `sum_i q_i sigma(E_i)`. Production computes both numerator
forms and fails if they disagree.

No `sigma^2`, missing `sigma`, duplicate normalization, altered denominator,
clipping, or extrapolation was found. Details are in
`docs/audit/LSC_6_5_0_CROSS_SECTION_ACCOUNTING_AUDIT.md`.

Result: `PASS_EXACTLY_ONE_BASELINE_CROSS_SECTION_REPLACED`.

## 5. Domain and third-path numerical audit

From support `[0.24, 30.0]` MeV and all nine active source lines, an
independent 60-digit Decimal derivation gave

`[-0.5747389495096434, 3.6072380250767027]`.

The largest difference from the stored binary64 domain
`[-0.5747389495096434, 3.607238025076703]` was
`1.5066428236193636e-16`. Exact boundaries and `1e-12`-inside points passed;
both `1e-12`-outside points returned
`FAIL_CLOSED_UNSUPPORTED_DOMAIN`. No silent substitution occurred.

The third path imports neither production nor the existing reference core. It
solves the 58-knot natural spline as a dense Decimal system and constructs the
direct numerator. Declared tolerances were `5e-11` general, `5e-9` boundary,
`5e-15` domain, `5e-7` first-order, and `5e-10` root.

- numerical golden vectors: `20/20` PASS;
- maximum golden absolute difference: `5.4569682106375694e-12`;
- all supported line/alpha comparisons: `90/90` PASS;
- maximum production/third-path difference: `7.275957614183426e-12`;
- independent alpha root: `-0.14388795520867112`;
- root difference from frozen result: `6.490719842836765e-12`;
- interval endpoint differences: below `3.4e-16`.

Details are in
`docs/audit/LSC_6_5_0_THIRD_PATH_NUMERICAL_AUDIT.md`.

Result: `PASS_THIRD_INDEPENDENT_NUMERICAL_PATH`.

## 6. Golden-vector audit

All `29/29` frozen vectors passed: 20 numerical success vectors and nine
fail-closed vectors. Their expected values state that they were generated by
the independent stdlib natural-spline/direct-numerator path, not copied from
production. The suite constrains the analytic null, small/moderate/large
dilation, boundaries, provenance, source mutation, unsupported anisotropy,
domain errors, and label-independent universal sharing.

Result: `GOLDEN_VECTORS_PASS_29_OF_29`.

## 7. Parameter determination and effective DOF

Frozen result:

- `alpha_0 = -0.14388795521516184`;
- interval: `[-0.19024973740805776, -0.10233891434687088]`;
- objective: `2.169792942258529e-20`;
- classification: `RETROSPECTIVE_NON_BLIND_PARAMETER_DETERMINATION`;
- inference: `ASSUMPTION_BASED_SENSITIVITY_ONLY`;
- boundary: `INTERIOR`;
- identifiability: `IDENTIFIABLE_ONE_DIMENSIONAL`.

Only the BEST inner-zone published aggregate `0.791 +/- 0.05` enters the
objective. Its development-manifest SHA-256 is
`2ccccde98363954b9167263cd54c20a9dd9068686ad382ed8388560559dfc87b`.
BEST outer, GALLEX/GNO, SAGE Cr51, SAGE Ar37, and BEST-2 are absent. The frozen
one-by-one diagonal covariance, zero profiled nuisances, bounded deterministic
optimizer, support-derived bounds, convergence, interiority, identifiability,
and two-sided `Delta chi2 = 1` construction match the protocol.

There is one independent observable, one fitted LSC physical parameter, zero
fitted nuisance parameters, and zero effective residual degrees of freedom.
An equivalent monotone root solution `R_pred(alpha_0) = 0.791` exists.

The near-zero objective is expected from the construction and is not evidence
of extraordinary empirical agreement or validation.

The objective has no goodness-of-fit meaning. Details are in
`docs/audit/LSC_6_5_0_OBJECTIVE_DOF_AUDIT.md` and
`docs/audit/LSC_6_5_0_PARAMETER_FREEZE_AND_NO_REFIT_AUDIT.md`.

Result: `PARAMETER_FREEZE_VALID_ZERO_EFFECTIVE_RESIDUAL_DOF`.

## 8. Aborted-run forensics

R1 aborted at `2026-08-16T16:58:55Z`; R2 aborted at
`2026-08-16T17:00:28Z`. Both loaded frozen inputs and evaluated the objective;
the optimizer held local values. Both then raised `NameError` during Python
dictionary construction because JSON-style lowercase boolean names remained.
Neither result dictionary completed, serialized, printed, returned, or created
a result file. No value was exposed to a decision maker.

Byte reconstruction proved the exact source sequence:

- R1: `86070aded79a0c9c5e959d441414bed83f5598d8f4a9d69a65a741c3e94bc02b`;
- R2: `86c0bd75072da14f6260eeca9b82ed3c8a95b6148022f25054beadf8ffaa86b3`;
- R3: `fc8b7e1517b98995e6a140aa190d264fa2f19c1899d20927996558bcf9818879`.

The transitions changed exactly two, then three, boolean tokens. No physics,
data, bound, objective, covariance, nuisance, optimizer, interval, or decision
changed. Details are in `docs/audit/STEP_07E_ABORTED_RUN_FORENSICS.md`.

Verdict: `NO_RESULT_EXPOSURE_BEFORE_PRIMARY_RUN`.

## 9. Data exposure and permanent no-refit enforcement

- BEST inner: `MODEL_EXPOSED`, `POST_6_4_DEVELOPMENT`,
  `RETROSPECTIVE_NON_BLIND`, `DEVELOPMENT_DATA`;
- BEST outer, GALLEX/GNO, and SAGE: excluded from the objective but
  historically exposed, therefore not strict blind;
- BEST-2: `FUTURE_ONLY`, `FUTURE_BLIND`;
- BEST-2 observed data accessed: **NO**;
- BEST-2 prediction generated: **NO**.

Production has no optimizer and accepts one scalar parameter. Frozen-bundle
use verifies the exact file hash, value, and `no_refit=true`. An alternate
value fails closed. Authorized lines must match canonical IDs, energies, and
branching fractions. Unknown profile keys and all tensor/axis/directional or
second-parameter keys fail closed. `execute_once` refuses when the frozen
result exists. Recalculation tools verify but cannot replace the result.

No experiment-, isotope-, zone-, run-, or exposure-specific alpha, silent
override, alternate response, alternate payload/spline, or hidden tensor/axis
activation path was found.

Result: `FROZEN_UNIVERSAL_ALPHA_NO_REFIT_FAIL_CLOSED`.

## 10. Clean-room reproduction

Two independent directories were exported directly from the frozen input
commit and executed sequentially. Both receipts were byte-for-byte identical,
with receipt SHA-256
`4d32ae3cbb8508ba08f0af353fd8a479d64258b2791145033cfa4584507bd2ce`.
Each reproduced:

- scientific/component/model hashes;
- `29/29` golden vectors;
- frozen alpha and interval;
- parameter-bundle hash;
- preserved LSC 6.4.0 adverse result;
- `BEST2_observed_data_accessed=false`;
- `BEST2_prediction_generated=false`;
- RC checksum result PASS.

The final public model package also reproduced after deterministic local
materialization of the omitted Bahcall payload. The final GitHub export
reproduced and passed its 12-case public closure suite. Frozen serialized
objects and receipts are classified `BITWISE_IDENTICAL`; the independently
implemented third-path calculation is
`NUMERICALLY_IDENTICAL_WITHIN_FROZEN_TOLERANCE`.

Result: `CLEAN_ROOM_REPRODUCTION_PASS`.

## 11. Software and security audit

No hidden scientific defaults, alternate physics, undocumented prediction
input, cache dependency, nondeterministic prediction source, unsafe
deserialization, dynamic code execution, shell command construction, absolute
path dependency, secret, private URL, or production network access was found.
The only network-capable file is the explicit publication acquisition utility.
It uses HTTPS, a timeout, a response-size cap, exact source/output hashes,
strict parsing, and exclusive-create semantics.

Severity counts: critical **0**, high **0**, medium **0**. Details and source
locations are in `docs/audit/LSC_6_5_0_SOFTWARE_SECURITY_AUDIT.md`.

Three non-scientific export defects were found and repaired:

1. public execution initially selected historical integration tests whose bulk
   archive is intentionally not redistributed; the public default now selects
   the self-contained STEP 08 closure suite;
2. 17 links into the omitted archive were converted to explicit non-clickable
   archival evidence paths, and unresolved-link checking became mandatory;
3. unclear Bahcall-table redistribution was handled by omission plus
   deterministic hash-verified acquisition.

The repairs affect documentation/export mechanics only. RC1 and every
scientific hash remain unchanged, so RC2 is not required.

Result: `SOFTWARE_AUDIT_PASS_ZERO_CRITICAL_FINDINGS`.

## 12. Historical lineage

- **6.3.0:** historical commit, version DOI, concept DOI, symbolic equations,
  and identity are preserved; its complete numerical state remains
  incompletely recoverable;
- **6.3.1:** `ABANDONED_BEFORE_RELEASE`;
- **6.4.0:** `DEVELOPMENT_PARAMETER_DETERMINATION_FAILED`; the adverse result
  remains immutable and is not softened;
- **6.5.0:** new owner-authorized exact finite-dilation successor, not a
  repair or relabeling of 6.4.0.

The current enclosing historical archive checksum ledger passed `1882/1882`.
The nested historical repository is clean at
`6ffa07bdde533fcc2a550e36c762b8edd9236c47`, and nested
`git fsck --no-dangling` passed.

Legacy nested PRE/POST checksum lists are retained as point-in-time migration
evidence, not current-tree manifests. When applied to the current nested tree,
`CHECKSUMS.sha256` has 397/399 matches (the self checksum and companion
manifest are stale), POST has 249/253 matches after later documentation
updates, and PRE references pre-migration paths. They were not rewritten.
Current integrity is established by the clean Git object database and the
outer 1882-entry ledger. This is part of the already disclosed historical
recoverability limitation and does not affect the frozen 6.5.0 object.

Result: `HISTORICAL_LINEAGE_PRESERVED_WITH_DISCLOSED_6_3_0_LIMITATION`.

## 13. Package versus model versioning

The Validation Kernel software/package version is `0.6.0`; the scientific
model version is LSC `6.5.0`. Repository history shows that the package series
advanced with kernel Steps 2--6 and remained independent from later scientific
model versions. Public metadata labels both namespaces prominently. No version
or scientific hash was changed.

Details are in `docs/audit/PACKAGE_VS_MODEL_VERSIONING_DECISION.md`.

Result: `INDEPENDENT_PACKAGE_AND_MODEL_VERSION_LINES_DOCUMENTED`.

## 14. Claim-language audit

Allowed claims are limited to explicitly specified, executable,
deterministic, reproducible, parameter-frozen, retrospective parameter
determination completed, ready for independent retrospective validation, and
prospectively freeze-capable. The retrospective/non-blind and
sensitivity-only labels are mandatory where relevant.

Experimental validation/confirmation, discovery, blind confirmation,
BEST/GALLEX/SAGE/BEST-2 confirmation, KATRIN/IceCube confirmation or exclusion,
and directional/anisotropic evidence are prohibited. The 10-row frozen claim
matrix contains three allowed and seven prohibited claims; all were preserved.
Five public-facing release documents passed contextual claim checks.

Details are in `docs/audit/LSC_6_5_0_CLAIM_LANGUAGE_AUDIT.md`.

Result: `CLAIM_BOUNDARY_ENFORCED_VALIDATION_NOT_YET_PERFORMED`.

## 15. RC1 release audit

RC1 contains its README, owner authorization, exact specification/equations,
parameter protocol/result/bundle, provenance and interpolation policy,
production and independent evaluators, schemas, golden vectors, environment
lock, development disclosure, limitations/reproduction instructions,
citation/license metadata, manifest, and checksums.

- files: 52;
- manifest rows: 50;
- checksum entries: `51/51` PASS;
- `SHA256SUMS.txt` SHA-256:
  `87212f2645fd8375b000777b3fdbc21b7a1cf45bd4d743511a6ac64192cff5e8`;
- `MANIFEST.json` SHA-256:
  `5118142cb11e91c3102ffa34157094bac5fba75ff0528bfda4be1e4c81772c0f`.

RC1 is the immutable complete local audit object. Because it contains the
Bahcall table with unclear redistribution permission, public distribution uses
the sanitized export, not RC1 itself. Details are in
`docs/audit/LSC_6_5_0_RC1_RELEASE_AUDIT.md`.

Result: `RC1_SCIENTIFIC_AND_REPRODUCIBILITY_AUDIT_PASS`.

## 16. License and provenance

Original Validation Kernel code/documentation is prepared under MIT with an
explicit third-party exclusion. External sources have citation, DOI/URL,
version, exact local/source hashes, transformations, and redistribution status.

- Bahcall 1997 cross section: DOI `10.1103/PhysRevC.56.3391`, arXiv
  `hep-ph/9710491`; no explicit author-table redistribution license found, so
  the table is omitted and deterministically acquired;
- Cr51/Ar37 source lines: DOI `10.1103/PhysRevC.108.035502`, arXiv
  `2303.13623`, author-manuscript license CC BY 4.0;
- BEST development aggregate: DOI `10.1103/PhysRevC.105.065502`, arXiv
  `2201.07364`, author-manuscript license CC BY 4.0.

No paper PDF/source or historical bulk mirror is redistributed. Critical
license/provenance findings after the omission/acquisition control: **0**.
Details are in `docs/audit/LSC_6_5_0_LICENSE_PROVENANCE_AUDIT.md` and
`THIRD_PARTY_NOTICES.md`.

Result: `PUBLICATION_SAFE_PROVENANCE_WITH_BAHCALL_NON_REDISTRIBUTION`.

## 17. Prepared publication packages

All packages are prepared but unpublished.

| Package | Files | Manifest SHA-256 | SHA256SUMS SHA-256 |
|---|---:|---|---|
| `publication/github/` | 334 | `75f52fdaeb9ce3aa722b470cd94357ae646074df09052dcd35bc068d2e673ca7` | `b5e107a07b6c4c3946f22594ac2fff9aaf1d1b13587807e2c9957024ac956c8d` |
| `publication/zenodo/LSC-6.5.0/` | 67 | `966e167e314f320398ca7b9df81692943e5cc026196e750676f95c86abce0e43` | `1646dd9422ecf1c3ed68aa22b20a2a39f16c4a613739fc93bab07751feebfba6` |
| `publication/zenodo/LSC-Validation-Kernel/` | 335 | `740fde2187c5f1654c289724f572109b14bb7b5b6d39f8544897b9ce26de3641` | `c7ab8a4179ac35cabc0c19e2dc436e15b3690590ed7627c9c530ad6656fb27e6` |

Checksum entries passed `333/333`, `66/66`, and `334/334`, respectively.
Package-index SHA-256 is
`1827601d7a06065bb1d30fe4d99b2275fc8cf38bf6fd907d568997c85c2832e2`.

Deterministic ZIPs were each rebuilt twice and matched:

- `LSC-6.5.0.zip`:
  `483fe617af8bce7213e9dff072103264ea99edd69d3f495c348bc3a58bbe4e3c`;
- `LSC-Validation-Kernel.zip`:
  `e5ea73c1127da3ba510029c38df6142feed7d5d26797fef2ccfae653d7f56e74`.

The GitHub export includes public-ready source, README, LICENSE, CITATION.cff,
CHANGELOG, release notes, model card, disclosure, reproduction instructions,
integrity metadata, and safe publication state. The Zenodo model artifact is
model-focused; the Validation Kernel remains a separate companion artifact.
No package contains the unlicensed table or bulk historical archive.

Result: `PUBLICATION_PACKAGES_PREPARED_CHECKSUMS_PASS`.

## 18. Zenodo lineage and remote state

The historical 6.3.0 version DOI `10.5281/zenodo.20377427` and concept DOI
`10.5281/zenodo.19780615` remain preserved. Subject to human ownership review,
6.5.0 is planned through Zenodo's New version operation in that model lineage,
with a new version DOI that has not been assigned. The Validation Kernel is a
separate linked record. Metadata placeholders contain null new DOI/date fields.

Git remote state remains:

- `origin` fetch/push:
  `https://github.com/luciferprosun/LSC-Validation-Kernel.git`;
- local branch: `main`;
- upstream: none;
- local `origin/main`: absent.

The future command, after explicit owner/publication authorization, is
`git push --set-upstream origin main`. It was not run. No remote state changed.
Details are in `docs/release/ZENODO_LINEAGE_PLAN.md` and
`docs/audit/LSC_6_5_0_REMOTE_UPSTREAM_AUDIT.md`.

## 19. Phase-2 and BEST-2 handoffs

`PHASE_2_VALIDATION_HANDOFF.md` freezes the model/specification/evaluator,
parameter and input hashes, no-refit policy, covariance limitation, exposure
classifications, mapping blockers, T12 status, and BEST-2 status. The primary
sequence remains:

`T11 -> T7 -> T3 -> T1 -> T10`.

No Phase-2 statistic was executed. KATRIN/IceCube mappings remain unavailable;
T12 remains inapplicable because anisotropy/tensor/axis sectors are disabled.

`BEST2_PROSPECTIVE_HANDOFF.md` keeps BEST-2 `FUTURE_ONLY` and `FUTURE_BLIND`.
Future work requires authoritative as-built inputs, all model/parameter/input
hashes, a pre-outcome freeze timestamp, no-refit guarantee, explicit
prediction authorization, and a hashed prediction artifact before outcome
access.

Result: `READY_FOR_SEPARATELY_AUTHORIZED_PHASE_2_VALIDATION`.

## 20. Publication-safety audit

The three package trees were scanned file-by-file for secrets/tokens/auth
files, private-key markers, local paths/usernames, private/local URLs,
repository metadata, caches, bytecode, shell history, temporary files,
SQLite/private state, session data, machine-specific state, symlinks, and the
non-redistributed payload.

- files/text files scanned: `736/736`;
- critical findings: `0`;
- Markdown files scanned: `241`;
- local links checked: `58/58`;
- unresolved local links: `0`;
- ZIP members: 67 model and 335 companion, with no forbidden member.

Result: `PUBLICATION_SAFETY_PASS_ZERO_CRITICAL_FINDINGS`.

## 21. Test and integrity matrix

| Gate | Exact result |
|---|---|
| Full historical/current repository suite | `280 passed, 28 subtests passed` |
| Dedicated LSC 6.5.0 suite | `24 passed, 4 subtests passed` |
| STEP 08 closure suite | `12 passed` |
| LSC 6.5.0 goldens | `29/29` |
| Third-path numerical goldens | `20/20` |
| All-line third-path comparisons | `90/90` |
| Domain boundary/inside/outside cases | `6/6` |
| First-order isotope bridges | `2/2` |
| Aborted source-revision reconstructions | `2/2` |
| Clean RC reproductions | `2/2`, byte-identical receipt |
| Final public model/GitHub reproductions | `2/2` |
| RC checksum entries | `51/51` |
| Public package manifests/checksum sets | `3/3` |
| Deterministic Zenodo ZIPs | `2/2` |
| Frozen claim rows | `10/10` adjudicated |
| Public-facing claim documents | `5/5` |
| Current historical archive checksums | `1882/1882` |
| Nested historical Git integrity | clean HEAD and fsck PASS |
| Publication safety | `736/736` files, zero critical findings |
| Local links | `58/58` |
| Main `git diff --check` | PASS |
| Main `git fsck --no-dangling` | PASS |

The full suite regenerated two tracked historical fixture manifests because
the code-tree hash includes new audit source. They were restored exactly to
the frozen input as required. No other tracked input changed and no unintended
generated diff remains.

## 22. Remaining limitations

1. The parameter estimate fits one observable with one parameter; effective
   residual DOF is zero and the objective is not goodness-of-fit evidence.
2. Collaboration covariance/nuisance decomposition is unavailable; inference
   remains `ASSUMPTION_BASED_SENSITIVITY_ONLY`.
3. Historical BEST/GALLEX/SAGE data are model-exposed, not strict blind tests.
4. BEST-2 lacks authoritative as-built inputs and remains future blind; no
   prediction exists.
5. KATRIN/IceCube mappings remain scientifically unjustified; T12 is disabled.
6. The complete numerical state of historical 6.3.0 remains incompletely
   recoverable; legacy point-in-time checksum ledgers are not current ledgers.
7. The Bahcall author table requires explicit hash-verified acquisition because
   redistribution permission is unclear.
8. Zenodo creators, affiliations, dates, access rights, and newly assigned DOI
   require human review at future upload time.
9. The public default suite is the self-contained STEP 08 closure suite; the
   complete historical integration suite requires the non-redistributed local
   evidence archive.

None of these limitations is concealed or converted into a validation claim.

## 23. Final decision and publication state

No scientific inconsistency was found. Parameter-freeze/preregistration
integrity is valid. Reproduction passes. Licensing/provenance does not block
the sanitized package. Critical findings are zero.

- Phase 1 complete: **YES**;
- publication ready: **YES**;
- publication performed: **NO**;
- public push performed: **NO**;
- GitHub Release created: **NO**;
- Zenodo upload performed: **NO**;
- DOI minted: **NO**;
- ready for separately authorized Phase-2 validation: **YES**;
- experimental validation performed: **NO**.

Final verdict:

`PHASE_1_COMPLETE_LSC_6_5_0_PUBLICATION_READY`

The STEP 08 commit is named
`Step 08: independently audit LSC 6.5.0 and close Phase 1`. Its final commit
hash is recorded by Git and in the external final audit response; a commit
cannot contain its own SHA-1 without changing that SHA-1.
