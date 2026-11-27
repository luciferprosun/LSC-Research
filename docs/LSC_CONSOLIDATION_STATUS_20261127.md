# LSC repository consolidation status — 2026-11-27

## Canonical repository

`luciferprosun/LSC-Research` is the single current LSC repository identified in the
owner's authenticated repository inventory on 2026-11-27. The audited main was
`5d29ce3fecbe64d642382e69e02498fd5691a758`.

The LSC 6.0 publication corpus was already present before this update. This change
makes that material directly discoverable; it does not claim a new source import.

| Component | Existing path | Verified scope |
| --- | --- | --- |
| Current freeze-stage research | `canonical/`, `validation/`, `implementation/`, `freeze_release/` | Existing scientific classification and freeze are preserved. |
| Separately versioned Validation Kernel | `validation-kernel/` | Existing subtree `8d1f9f02458955e23c720d6c59f86de5ae4ea895` is preserved. |
| Historical LSC 6.0 publication corpus | `historical_archive/pre_step5_repository/legacy/LSC-6.0/` | 46 tracked files, 4,483,531 bytes; subtree `355ded9ac210e2e49b3bb307c79ab80bfaa5d9c6`. |

## Preserved history and limits

The historical corpus contains the original license, citation/Zenodo metadata,
theory, simulations, outputs, release archives, and v1.2.0/6.2.0 materials.
The existing [history continuation plan](../historical_archive/pre_step5_repository/docs_pre_step5/GIT_HISTORY_CONTINUATION_PLAN.md)
states that original Git ancestry was not imported during the earlier extraction.
Content preservation is therefore established for the existing subtree, while
complete original repository ancestry is not claimed.

The historical `luciferprosun/LSC-6.0` repository URL returned 404 during this audit.
That response does not establish why it is unavailable, nor prove that the retained
corpus matches an unknown later head. No third-party mirror was imported as an
authoritative source. Existing DOI records, scientific versions, licenses, citations,
release files, and historical bytes remain unchanged.

## Integrity correction

The pre-existing main CI failed at `tools/evidence_chain.py verify --require-current`.
Commit `5d29ce3` added the public LinkedIn contact to `README.md` without appending
a corresponding root evidence record. The current files were compared with the
latest retained manifest before this update: `README.md` was the only differing
tracked path.

This change appends one root evidence record covering the earlier contact update,
the canonical navigation above, and this status document. The five previous root
records are preserved byte for byte. The Validation Kernel's independent chain and
all frozen scientific material are unchanged.

This is a repository-navigation and integrity-maintenance change. It introduces no
new scientific result, new model version, changed equations, or post-freeze analysis.
