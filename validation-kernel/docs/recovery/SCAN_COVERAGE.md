# Recovery Scan Coverage

## Current source tree

| Check | Result |
|---|---:|
| Total files inventoried outside nested `.git` stores | 1,788 |
| Substantive files scanned | 1,771 |
| Python cache files inspected separately | 17 |
| Effective file coverage | 1,788 / 1,788 |
| Text/document objects extracted | 1,235 |
| Large text/data files streamed byte-for-byte | 23 |
| PDFs extracted | 133 / 133 |
| DOCX/ODT containers inspected | 2 / 2 |
| Notebook files | 1 |
| Notebook code cells | 2 |
| Notebook saved output blocks | 0 |
| Listed serialized artifacts | 47 |
| Python bytecode cache artifacts | 17 |
| Archive containers inventoried | 21 |
| Current-tree candidate rows | 593 |
| Current-tree scan errors | 0 |

The 47 listed serialized artifacts comprise 31 HDF5 files, 15 NPZ files, and one pickle. NPZ directory entries and NPY headers were inspected without loading arrays. The pickle was never deserialized. HDF5 magic and hashes were checked; deeper HDF5 group enumeration was unavailable because neither `h5dump` nor `h5py` was installed. All 31 HDF5 paths belong to IceCube or Daya Bay external data and none matched P0 LSC-object terms by path.

The only notebook is an unexecuted null-versus-sterile baseline template with no saved outputs. It contains no numerical LSC object.

## Git history

| Check | Result |
|---|---:|
| Nested repositories scanned | 4 |
| Reachable commits scanned | 397 |
| Branch refs scanned | 12 |
| Tags scanned | 17 |
| Historical tree entries scanned | 23,880 |
| Unique blobs seen | 1,353 |
| Historical text blobs scanned | 990 |
| Historical candidate blob versions | 665 |
| Deletion events inspected | 25 |
| Git scan errors | 0 |

The primary `LSC-Research` repository has six commits and no tags. The 17 tags belong to the Daya Bay dependencies.

## Candidate and adjudication counts

- 593 current-tree candidate rows;
- 665 historical candidate blob-version rows;
- 17 Python-cache candidate rows;
- 1,275 raw scan rows before semantic deduplication;
- 39 adjudicated provenance-registry entries;
- 9 `AUTHENTIC_FROZEN`;
- 3 `DERIVED_FROM_FROZEN`;
- 9 `HISTORICAL_POST_DATA`;
- 2 `UNVERIFIED`;
- 16 `MISSING`.

Raw candidate counts are search hits and include duplicate release copies and external scientific literature. They are not a claim that 1,275 distinct LSC objects exist.

## Safety

- no fit or refit executed;
- no notebook executed;
- no pickle, checkpoint, bytecode, or opaque object deserialized;
- no source archive file modified;
- no nested Git repository modified;
- no physics test executed.
