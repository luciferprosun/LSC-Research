# Git Archaeology

Status: read-only Step 01 scan

## Coverage

All reachable commits, local/remote branch refs, tags, tree entries, text blobs, and deletion events were scanned for every nested Git repository in the source archive.

| Scope | Result |
|---|---:|
| Git repositories | 4 |
| Commits | 397 |
| Branch refs | 12 |
| Tags | 17 |
| Tree entries across commits | 23,880 |
| Unique blobs seen | 1,353 |
| Text blobs inspected | 990 |
| Candidate blob versions | 665 |
| Deletion events | 25 |
| Scan errors | 0 |

Only `LSC-Research` is primary LSC history. The other three repositories are Daya Bay external dependencies. Their 17 tags are not LSC release tags.

## Primary LSC history

| Commit | Parent | Date | Author | Subject |
|---|---|---|---|---|
| `700aa9262df66731f0fc180af44fbdea9897623d` | root | 2026-05-23 09:28:17 +02:00 | Codex | Initial LSC authority extraction |
| `e22c7fc1f55aba77ce266487cfb72951514eb0c4` | `700aa926…` | 2026-05-23 09:33:26 +02:00 | Codex | Authority purity boundary fix |
| `a0956319e2a14e707f48fe2b5bf7411980abdfe7` | `e22c7fc…` | 2026-05-23 09:36:59 +02:00 | Codex | Tighten authority boundary wording |
| `4e4c49244b44fedb6fb062823dcb021c8eacca79` | `a095631…` | 2026-05-23 10:14:39 +02:00 | Codex | Migrate LSC data block from legacy mixed root |
| `75901c968c7dbde7a16ea4836b18b8163950befa` | `4e4c492…` | 2026-05-25 11:21:31 +02:00 | Codex | Finalize LSC Pre-BEST-2 freeze repository structure |
| `6ffa07bdde533fcc2a550e36c762b8edd9236c47` | `75901c9…` | 2026-05-25 13:04:43 +02:00 | Codex | Record LSC Zenodo final publication update |

Primary repository results:

- 6 commits scanned;
- 3 branch refs (`main`, `origin/main`, `origin/HEAD`) pointing to the same HEAD;
- 0 tags;
- 1,306 tree entries scanned;
- 284 unique blobs seen;
- 241 text blobs inspected;
- 327 candidate blob versions;
- 3 deletion events, none containing a P0 filename match;
- clean worktree at capture.

## Important object provenance

| Object | First native Git provenance | Parent | Path context | Decision |
|---|---|---|---|---|
| E1-E12 canonical equations | `75901c968c7d…` | `4e4c49244b44…` | `canonical/LSC_ACTIVE_EQUATION_SET.md` | `AUTHENTIC_FROZEN`, symbolic only |
| Canonical parameter structures | `75901c968c7d…` | `4e4c49244b44…` | `canonical/LSC_CANONICAL_CORE.md` | `AUTHENTIC_FROZEN`, no values |
| Freeze boundary | `75901c968c7d…` | `4e4c49244b44…` | `canonical/LSC_FREEZE_BOUNDARY.md` | `AUTHENTIC_FROZEN` negative evidence |
| Final Zenodo publication report | `6ffa07bdde53…` | `75901c968c7d…` | `freeze_release/LSC_FINAL_ZENODO_PUBLICATION_REPORT.md` | `AUTHENTIC_FROZEN` release provenance |
| Toy `c0/c1` output | traceable with `--follow` to root `700aa9262df6…` | root | originally `LSC_core/.../model_parameters.csv`, later moved below `historical_archive/` | `HISTORICAL_POST_DATA` |
| LSC 6.2.1 coefficient output | traceable with `--follow` to root `700aa9262df6…` | root | originally `LSC_core/.../analysis.json`, later moved below `historical_archive/` | `HISTORICAL_POST_DATA` |
| LSC 5.5 optimized values | traceable with `--follow` to root `700aa9262df6…` | root | originally `LSC_core/.../optimized_parameters.json`, later moved below `historical_archive/` | `HISTORICAL_POST_DATA` |

The root commit is an authority extraction/import. It proves that objects were present by 2026-05-23, but it does not by itself prove their original creation time. Filename dates and internal statements are retained as source-derived claims, not upgraded to native Git timestamps.

## Deletions

The primary history deleted three continuity documents in `e22c7fc…` while tightening the authority boundary. None matched P0 parameter/evaluator terms by path. All deleted paths and commit metadata are preserved in `recovery/scans/GIT_DELETED_FILES.csv`.

## Machine-readable evidence

- `recovery/scans/GIT_REPOSITORY_SUMMARY.csv`
- `recovery/scans/GIT_HISTORY_CANDIDATES.csv`
- `recovery/scans/GIT_DELETED_FILES.csv`
- `recovery/scans/GIT_HISTORY_SCAN_SUMMARY.json`
- `recovery/scans/GIT_SCAN_ERRORS.csv`
