# STEP 01 — FROZEN OBJECT RECOVERY RESULT

Project: LSC Validation Kernel
Status: **PASS**

The Step 01 process is complete as a recovery gate. The result is partial recovery of the historical object, not a claim that an executable numerical LSC 6.3.0 model was recovered.

## A. Repository rename

- Previous project name/path: `…/LSC 6.3.1`
- New project name/path: `…/LSC-Validation-Kernel`
- Public project name: `LSC Validation Kernel`
- Previous outer Git repository: none
- New outer Git repository: initialized on `main`
- Canonical nested historical repository: `LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research`
- Nested historical HEAD: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`
- Nested historical worktree: clean before and after Step 01
- History preserved: **YES**

The 3.9 GiB source archive stayed in place under the renamed project and is ignored by the new outer repository. Its four nested repositories, hidden files, branches, tags, remotes, and object stores were not modified.

## B. Freeze

- Branch: `main`
- Outer HEAD before work: none; the outer directory was not a Git repository
- Canonical historical HEAD before work: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`
- Freeze tag: `pre-validation-kernel-recovery`
- Freeze commit: `a6d582694d55fa0260ef7ab07ed83fd06feef607`
- Freeze commit subject: `chore: freeze validation-kernel recovery input`
- Worktree status at freeze: tracked state clean; preserved archive present as one ignored tree
- Untracked input at initialization: `LSC_6_3_0_VALIDATION/`
- Important ignored input: `LSC_6_3_0_VALIDATION/`; Python/test caches; environment/secret patterns; large serialized formats

The tag records the archive identity, manifest hashes, canonical nested Git HEAD, and ignore boundary. It does not claim that a complete evaluator exists.

## C. Search coverage

| Measure | Count |
|---|---:|
| Files inventoried outside nested `.git` stores | 1,788 |
| Substantive files content-scanned | 1,771 |
| Python bytecode caches separately inspected | 17 |
| Effective current-tree file coverage | 1,788 / 1,788 |
| Extracted text/document objects | 1,235 |
| Large text/data files streamed byte-for-byte | 23 |
| PDFs extracted successfully | 133 / 133 |
| Notebooks scanned | 1 |
| Notebook saved output blocks | 0 |
| Listed serialized artifacts inspected | 47 |
| Archive containers inventoried | 21 |
| Git repositories scanned | 4 |
| Commits scanned | 397 |
| Branch refs scanned | 12 |
| Tags scanned | 17 |
| Historical tree entries scanned | 23,880 |
| Unique Git blobs seen | 1,353 |
| Historical text blobs scanned | 990 |
| Current-tree candidate rows | 593 |
| Historical candidate blob-version rows | 665 |
| Cache candidate rows | 17 |
| Raw candidate scan rows before semantic deduplication | 1,275 |
| Semantically adjudicated registry objects | 39 |
| Scan errors | 0 |

The primary `LSC-Research` history contributes 6 commits, 3 branch refs, 0 tags, 1,306 tree entries, 284 unique blobs, 241 inspected text blobs, and 327 candidate blob versions. The other repositories are Daya Bay external dependencies.

All 133 PDFs were text-extracted. DOCX and ODT XML content was inspected. NPZ directory entries and NPY headers were parsed without array loading. The pickle and Python bytecode were not deserialized or executed. The 31 HDF5 objects had their magic, size, path, and SHA-256 checked; deeper group enumeration was unavailable because `h5dump` and `h5py` were absent. They are external IceCube/Daya Bay data, not P0 LSC candidates.

## D. P0 recovery summary

| Object | Status | Source | Commit | SHA-256 | Exposure |
|---|---|---|---|---|---|
| Frozen repository object | `AUTHENTIC_FROZEN` | Git object evidence | `6ffa07bdde533fcc2a550e36c762b8edd9236c47` | `8c8bcf64f4dc6ac1ef6cbf27815464f7a73049df160ced86e8f74275f09e116e` | Post-BEST; pre-BEST-2 |
| E1-E12 symbolic equation set | `AUTHENTIC_FROZEN` | `canonical/LSC_ACTIVE_EQUATION_SET.md` | `75901c968c7dbde7a16ea4836b18b8163950befa` | `af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981` | Post-BEST; pre-BEST-2 |
| Active parameter structures | `AUTHENTIC_FROZEN` | `canonical/LSC_CANONICAL_CORE.md` | `75901c968c7dbde7a16ea4836b18b8163950befa` | `c8857d6bd1c8f1cb3b6d145c4b942985cb330edea879a31de6dabafef882a762` | Post-BEST; pre-BEST-2 |
| Freeze boundary | `AUTHENTIC_FROZEN` | `canonical/LSC_FREEZE_BOUNDARY.md` | `75901c968c7dbde7a16ea4836b18b8163950befa` | `b38ccc4f9f67e020b6c090e548e0bdcc2e8053097e22ac5ceb6447730e6a1f05` | Post-BEST; pre-BEST-2 |
| Full `theta` vector | `MISSING` | No authoritative artifact | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Parameter ordering | `MISSING` | No authoritative artifact | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Numerical `lambda0` | `MISSING` | Symbol only | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Numerical `lambdaA` | `MISSING` | Symbol only | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Exact `f0_a` | `MISSING` | Explicitly not frozen | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Exact `fA_a` | `MISSING` | Explicitly not frozen | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Active tensor components | `MISSING` | Historical convention-conflicted candidates only | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Tensor orientation | `MISSING` | Explicitly not frozen | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Complete coordinate frame | `MISSING` | E11 is symbolic and metadata-blocked | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Complete active units | `MISSING` | No vector-level schema | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| E1-E12 executable evaluator | `MISSING` | Canonical equations are document-only | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Authentic frozen prediction table | `MISSING` | Existing tables are fitted/post-data | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Frozen numerical configuration | `MISSING` | Historical configs are incompatible | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |
| Native frozen Git tag | `MISSING` | Preserved LSC repo has zero tags | `NOT_FOUND` | `NOT_APPLICABLE` | Unknown |

## E. Recovered authentic frozen objects

1. Canonical historical Git object `6ffa07bdde533fcc2a550e36c762b8edd9236c47`.
2. Canonical symbolic E1-E12 equation set.
3. Canonical active parameter *names and roles*.
4. Canonical frozen/non-frozen boundary.
5. Canonical historical lineage.
6. Pre-BEST-2 freeze statement.
7. Zenodo release identity: version `6.3.0-pre-BEST2-freeze-update`, version DOI `10.5281/zenodo.20377427`, concept DOI `10.5281/zenodo.19780615`.
8. Canonical validation protocol.
9. Canonical M0-M6 specification templates.

These objects authenticate the release and symbolic methodology. They do not constitute a complete numerical evaluator.

## F. Derived objects

1. `FROZEN_MODEL_MANIFEST.md`, a source-hashed summary that explicitly records the absence of a complete numerical vector.
2. `FrozenPredictionAdapter`, which verifies a manifest and consumes an external precomputed prediction table without fitting.
3. `LSC_MASTER_DATA_MANIFEST.csv`, a file-level archive inventory and checksum layer.

All three are deterministic provenance/validation infrastructure. None supplies a missing LSC prediction.

## G. Post-data historical objects

1. Toy M5/M6 `c0=0.808281` and `c1=0.012500` table.
2. The generator proving those toy coefficients were fit to observed ratios.
3. LSC 6.2.1 five-anchor coefficient vector and retained poor leave-one-out results.
4. The LSC 6.2.1 least-squares implementation.
5. LSC 5.5 input `D=(1,-0.5,-0.5)`, alpha range, and BEST/GALLEX deficits.
6. LSC 5.5 optimized `alpha=5.320180123926299e-06` output.
7. LSC 6.0 toy `amplification=3.5` and selected response scenarios.
8. LSC 6.2 illustrative `delta≈0.05`, explicitly stated not to be fitted or measured.
9. Deprecated LSC 4.x PBH-era numerical configuration.

These objects remain preserved. None can be used as the authentic 6.3.0 frozen vector.

## H. Unverified candidates

1. Mapping toy `c0/c1` to active `lambda0/lambdaA`: `UNVERIFIED`. The symbols differ, the values are fitted post-data, and no source-defined transform exists.
2. Mapping LSC 5.5 `D` to active 6.3.0 `A_a^{ij}`: `UNVERIFIED`. Scale, frame, zone index, normalization, and version semantics conflict.

The registry uses the official class `UNVERIFIED`; `UNVERIFIED_CONFLICT` appears only in the notes as required.

## I. Missing objects

1. Full `theta` vector.
2. Exact parameter ordering.
3. Numerical `lambda0`.
4. Numerical `lambdaA`.
5. Exact `f0_a` functional form.
6. Exact `fA_a` functional form.
7. Active numerical `A_a^{ij}` components.
8. Tensor orientation.
9. Complete coordinate/reference-frame object.
10. Complete unit schema.
11. E1-E12 machine-executable evaluator.
12. Authentic frozen prediction table.
13. Complete frozen numerical configuration.
14. Final parameter bounds/priors.
15. Numerical integration defaults and normalization order.
16. Native frozen Git tag.

## J. Conflicts

| Conflict | Resolution |
|---|---|
| Toy `c0/c1` versus `lambda0/lambdaA` | No mapping. Keep source as `HISTORICAL_POST_DATA`; mapping claim is `UNVERIFIED`. |
| LSC 5.5 `D` versus 6.3.0 `A_a^{ij}` | No version-safe transform. Keep source as `HISTORICAL_POST_DATA`; mapping claim is `UNVERIFIED`. |
| LSC 6.2 illustrative `delta≈0.05` versus an active amplitude | Source expressly labels it illustrative. Preserve as historical, never frozen. |
| File/import timestamps versus claimed earlier version dates | Native Git begins with a 2026-05-23 import. Earlier dates are source-derived, not native-Git facts. |
| Zenodo version versus Git tag | DOI/version provenance exists, but no Git tag exists. Do not equate them. |

## K. Data leakage assessment

### PRE_DATA

- The 2026-05-25 canonical freeze is pre-data only relative to future BEST-2 outcomes.

### POST_DATA

- The canonical freeze is post-data relative to published BEST, GALLEX/GNO, and SAGE values.
- The toy M5/M6 table is generated by a fit to observed ratios.
- The LSC 6.2.1 coefficient vector is an exact five-anchor fit to BEST/GALLEX/SAGE.
- LSC 5.5 optimized values contain BEST/GALLEX targets.
- The LSC 6.0 toy source contains `TARGET_R_BEST=0.79`.
- The LSC 6.2 illustrative magnitude was written after relevant data were public, although the source says it was not fitted.

### UNKNOWN_EXPOSURE

- Every missing object.
- Any claimed pre-import timestamp not independently supported beyond filename or internal prose.

No project-wide accusation of tuning is made. The classification follows direct source evidence and preserves uncertainty.

## L. Files created

### Project and architecture

- `README.md`
- `docs/architecture/VALIDATION_KERNEL_ARCHITECTURE.md`
- `frozen_core/README.md`
- `frozen_core/candidates/README.md`
- `frozen_core/equations/README.md`
- `frozen_core/parameters/README.md`

### Provenance and recovery documentation

- `docs/provenance/FROZEN_PROVENANCE_REGISTRY.csv`
- `docs/provenance/GIT_ARCHAEOLOGY.md`
- `docs/provenance/DATA_EXPOSURE_ASSESSMENT.md`
- `docs/recovery/MISSING_OBJECT_MATRIX.md`
- `docs/recovery/SCAN_COVERAGE.md`
- `docs/recovery/STEP_01_FROZEN_OBJECT_RECOVERY_REPORT.md`

### Evidence and manifests

- `frozen_core/manifests/INPUT_ARCHIVE_IDENTITY.csv`
- `recovery/evidence/STEP_01_INPUT_STATE.md`
- `recovery/evidence/GIT_OBJECT_IDENTITY.csv`
- `recovery/evidence/IMPORTANT_ARTIFACTS_SOURCE.csv`
- `recovery/evidence/IMPORTANT_ARTIFACT_HASHES.csv`
- `recovery/evidence/FROZEN_PROVENANCE_ADJUDICATION_SOURCE.csv`
- `recovery/reports/README.md`

### Deterministic scans

- `recovery/scans/REPOSITORY_CANDIDATES.csv`
- `recovery/scans/REPOSITORY_SCAN_SUMMARY.json`
- `recovery/scans/REPOSITORY_SCAN_ERRORS.csv`
- `recovery/scans/SERIALIZED_ARTIFACTS.csv`
- `recovery/scans/NOTEBOOK_OUTPUT_SCAN.csv`
- `recovery/scans/ARCHIVE_MEMBER_SCAN.csv`
- `recovery/scans/DUPLICATE_HASH_GROUPS.json`
- `recovery/scans/PYTHON_CACHE_SCAN.csv`
- `recovery/scans/PYTHON_CACHE_SCAN_SUMMARY.json`
- `recovery/scans/GIT_REPOSITORY_SUMMARY.csv`
- `recovery/scans/GIT_HISTORY_CANDIDATES.csv`
- `recovery/scans/GIT_HISTORY_SCAN_SUMMARY.json`
- `recovery/scans/GIT_DELETED_FILES.csv`
- `recovery/scans/GIT_SCAN_ERRORS.csv`

### Tools and tests

- `tools/recovery_lib.py`
- `tools/scan_repository.py`
- `tools/scan_python_cache.py`
- `tools/scan_git_history.py`
- `tools/hash_artifacts.py`
- `tools/build_recovery_registry.py`
- `tests/test_recovery_tools.py`
- `.gitignore`

## M. Files modified

- Preserved source archive files modified: **NONE**
- Nested Git repositories modified: **NONE**
- Existing LSC equations, parameters, data, notebooks, outputs, and history modified: **NONE**
- Project directory renamed: **YES**, from the former 6.3.1-style name to `LSC-Validation-Kernel`
- Outer local `.git/config`: private `origin` remote added; not a committed project file

## N. Tests

| Check | Result |
|---|---|
| Python syntax compilation for recovery tools | PASS |
| Correct SHA-256 | PASS |
| Stable registry output | PASS |
| Duplicate-content detection | PASS |
| Same filename with different hashes remains distinct | PASS |
| Official five-class enforcement | PASS |
| No automatic replacement of `MISSING` | PASS |
| Current-tree scan | PASS, 0 errors |
| PDF extraction | PASS, 133/133 |
| Notebook code/output scan | PASS, 1 notebook and 0 saved outputs |
| Serialized metadata scan | PASS, no deserialization |
| Python cache scan | PASS, no import/unmarshal |
| Complete reachable Git-history scan | PASS, 0 errors |
| Important artifact hashing | PASS, 25/25 |
| Preserved source archive checksums | PASS, 1,882/1,882 |
| Registry build and enum validation | PASS, 39/39 |
| Registry/hash-manifest regeneration | PASS, byte-for-byte deterministic |
| Nested repository cleanliness | PASS, 4/4 clean at original HEADs |
| High-confidence secret scan | PASS, 0 findings |
| Intended tracked files over 10 MiB | PASS, 0 files |
| GitHub visibility | PASS, `PRIVATE` |
| Remote publication-path gate | PASS by withholding push; 2 tracked evidence/scan files contain required absolute historical capture paths |

No LSC physics test, fit, refit, model evaluation, or BEST-2 prediction was run.

## O. Git state after Step 01

- Final branch: `main`
- Final commit subject: `Step 01: establish Validation Kernel and recover frozen object provenance`
- Final commit hash: resolve the committed `main` ref; the literal SHA is reported in the final handoff because a commit cannot contain its own hash
- Clean worktree after commit: **YES**
- Tags: `pre-validation-kernel-recovery` at `a6d582694d55fa0260ef7ab07ed83fd06feef607`
- Remote repository: `luciferprosun/LSC-Validation-Kernel`
- `REMOTE_VISIBILITY: PRIVATE`
- `REMOTE_PUSH_PERFORMED: NO`
- Public remote received changes: **NO**

The private repository was created and verified, but push was withheld. The immutable input-freeze commit records required local capture paths; remote policy prohibits publishing local filesystem paths, while Step 01 prohibits rewriting the freeze history. No force-push, history rewrite, or sanitized replacement history was attempted.

## P. Recovery verdict

**PARTIAL_FROZEN_OBJECT_RECOVERED**

Recovered: exact release identity, historical commit object, symbolic E1-E12 set, active parameter names, freeze boundary, validation protocol, version/DOI provenance, and historical candidates with exposure classifications.

Not recovered: a complete numerical parameter vector or executable evaluator contract.

## Q. Step 02 readiness

**READY FOR STEP 02: YES**

This means the evidence set is ready for human review and the next explicitly authorized provenance/design decision. It does **not** mean a numerical LSC evaluator is ready to implement. Any evaluator, likelihood, baseline implementation, scalar/tensor development, or BEST-2 prediction remains blocked until separately authorized and must not substitute post-data candidates for missing frozen fields.

Step 02 was not started.
