# Frozen Numerical Bundle Search

## Result

**FACT:** The targeted investigation did not locate an authentic, complete numerical LSC 6.3.0 bundle.

Final status: **AUTHENTIC_FROZEN_BUNDLE_INCOMPLETE**.

This is narrower than saying that no such object ever existed. It means that no qualifying object was located in the available Git object database, reflogs, branches, release archives, Zenodo record, notebooks, generated tables, serialized-file inventory, or retained local evidence as of 2026-08-16.

## Evidence precedence

Frozen admission uses this fixed hierarchy:

1. Exact machine-readable config in the frozen release.
2. Exact config or source in the frozen commit.
3. Exact machine-readable artifact in the archived release.
4. Signed or versioned numerical table uniquely tied to that freeze.
5. Numerical appendix uniquely tied to that release.
6. Historical candidate.
7. Inference or plot digitisation.

Levels 1-5 are only potentially admissible as authentic frozen objects. They also require exact lineage, unambiguous semantics, units, frame, ordering, and no conflict. Levels 6-7 cannot automatically enter the bundle. Plot digitisation is always an UNVERIFIED_CANDIDATE.

Authenticity and clean predictive status are separate. An exact release object can be historically authentic even if produced after a dataset was known; it cannot then be relabelled as a clean pre-data prediction for that dataset. Clean use additionally requires PRE_DATA or PRE_TARGET_DATA exposure.

## Targeted Git forensics

The historical LSC-Research repository has six reachable commits from 700aa9262df66731f0fc180af44fbdea9897623d through 6ffa07bdde533fcc2a550e36c762b8edd9236c47. The canonical freeze was introduced at 75901c968c7dbde7a16ea4836b18b8163950befa and the final commit records the Zenodo publication.

The investigation covered:

- all reachable branches and commits;
- exact-string and regex history searches for every P0 symbol;
- file renames and deletions;
- blame and diff context for canonical equations and freeze boundaries;
- reflogs, stashes, tags, merge parents, and object-database integrity;
- archived release and manuscript packages;
- notebook outputs, structured configs, generated tables, and serialized-artifact inventories.

There are no LSC tags, no stashes, no merge commits, and no unreachable/dangling Git objects in the available clone. Reflogs contain clone events only. The two deleted files are continuity documents, not numerical configs. Renames preserve the same canonical symbolic files.

### Reachable commit archaeology

| Commit | Parent | Date | Author | Relevant diff context |
|---|---|---|---|---|
| 700aa9262df66731f0fc180af44fbdea9897623d | root | 2026-05-23T09:28:17+02:00 | Codex | Initial authority extraction; imports canonical, historical, toy, and post-data material but no complete 6.3.0 numerical bundle |
| e22c7fc1f55aba77ce266487cfb72951514eb0c4 | 700aa9262df66731f0fc180af44fbdea9897623d | 2026-05-23T09:33:26+02:00 | Codex | Authority-purity boundary correction; deleted continuity documents do not contain a numerical vector |
| a0956319e2a14e707f48fe2b5bf7411980abdfe7 | e22c7fc1f55aba77ce266487cfb72951514eb0c4 | 2026-05-23T09:36:59+02:00 | Codex | Boundary wording tightened; no parameter/config introduction |
| 4e4c49244b44fedb6fb062823dcb021c8eacca79 | a0956319e2a14e707f48fe2b5bf7411980abdfe7 | 2026-05-23T10:14:39+02:00 | Codex | Legacy data migration; no numerical 6.3.0 object |
| 75901c968c7dbde7a16ea4836b18b8163950befa | 4e4c49244b44fedb6fb062823dcb021c8eacca79 | 2026-05-25T11:21:31+02:00 | Codex | Canonical freeze structure finalized; E1-E12 and parameter structures are symbolic and the boundary explicitly records missing numerical content |
| 6ffa07bdde533fcc2a550e36c762b8edd9236c47 | 75901c968c7dbde7a16ea4836b18b8163950befa | 2026-05-25T13:04:43+02:00 | Codex | Zenodo publication record added; no new evaluator or parameter bundle |

Significant paths are recorded with commit, date, and SHA-256 in FROZEN_PARAMETER_ADJUDICATION.csv. The post-data toy table is rooted at 700aa9262df66731f0fc180af44fbdea9897623d with SHA-256 bea6a9a0e9878ec2aa97402b897edd2547f9597a66da2cef1b12e4ab84dbe780. The LSC 5.5 tensor candidate is rooted at the same commit with SHA-256 ca0f18fb8ccd91f0e15304dc0ef225a278ada8bfeb79ab40e01cb4824b7cc5f4. Both are preserved and rejected rather than deleted.

## Exact release findings

The Zenodo record 10.5281/zenodo.20377427 contains one archive, zenodo25maj.zip. Its local SHA-256 is f21af7f0b1a6fbc4d4011ddf5b9c5b85e9710cd7d44f8da4d91e33ac0b09635 and the archived MD5 matches the record. The inventory contains documentation, manifests, historical artifacts, and publication material. It contains no complete parameter vector, evaluator configuration, or frozen prediction table.

The additional historical package LSC_6_3_0_unified_zenodo_package.zip has SHA-256 347f8bfe2d4106050c90c2734708040fda173d438f1b07cc2eb820ca83673a60 and contains five publication/documentation files only.

The public LSC-Research repository has no GitHub release assets or tags that add a numerical object.

## Authentic objects recovered

The following remain authentic frozen specification evidence:

| Object | Commit | SHA-256 | Scope |
|---|---|---|---|
| E1-E12 symbolic equation set | 75901c968c7dbde7a16ea4836b18b8163950befa | af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981 | Symbolic only |
| Canonical parameter structures | 75901c968c7dbde7a16ea4836b18b8163950befa | c8857d6bd1c8f1cb3b6d145c4b942985cb330edea879a31de6dabafef882a762 | Names and semantics only |
| Freeze boundary | 75901c968c7dbde7a16ea4836b18b8163950befa | b38ccc4f9f67e020b6c090e548e0bdcc2e8053097e22ac5ceb6447730e6a1f05 | Explicit negative evidence |

The freeze boundary explicitly leaves exact response functions, orientation, final bounds, covariance, and BEST-2 predictions outside the frozen numerical object.

## Rejected candidates

- Toy c0=0.808281 and c1=0.012500 are post-data fitted coefficients. No source maps them to lambda0/lambdaA.
- The LSC 5.5 D tensor and optimized alpha are post-data historical objects. No source maps D to active 6.3.0 A_a^{ij}.
- LSC 6.2/6.2.1 coefficients belong to another epoch and cannot fill a 6.3.0 bundle.
- Combining 6.3 equations, 6.2 coefficients, a 5.5 tensor, and toy normalization would be HISTORICAL_COMPOSITE_INVALID_FOR_FROZEN_VALIDATION.

## Parameter-by-parameter result

The complete adjudication is in FROZEN_PARAMETER_ADJUDICATION.csv. Every required value has an explicit status. No parameter was inferred from BEST, SAGE, GALLEX/GNO, KATRIN, IceCube, or any later validation result.

## Complete-bundle rule

A future bundle can become AUTHENTIC_FROZEN_BUNDLE_COMPLETE only if all values, ordering, units, frames, tensor semantics, source identity, and evaluator configuration are complete and mutually consistent. One unresolved critical field keeps the bundle incomplete.

Even if such a bundle is later located, STEP 05 never authorizes prediction. Certification and any controlled evaluation require a separate STEP 06 decision.
