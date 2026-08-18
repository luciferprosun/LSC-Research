# Publication Path Policy

## Historical evidence

The immutable input-freeze history contains a small number of machine-local capture paths. They record where source evidence existed during Step 01. Rewriting the freeze commit to remove them would falsify or replace provenance, so the history remains unchanged.

Those historical references do not authorize publication. The private remote remains unpushed.

## New artifacts

Every Step 02 source, generated manifest, and document must use repository-relative evidence paths. New artifacts must not contain:

- user-specific POSIX home paths;
- user-specific macOS home paths;
- Windows user-profile paths;
- local file URIs;
- secrets or environment-file contents.

`src/lsc_kernel/io/publication_paths.py` implements detection, and `tools/check_publication_paths.py` checks files changed since the Step 01 commit. Tests cover both a clean Step 02 tree and a deliberately local software fixture.

## Future public export

A later, separately authorized export may create a sanitized copy in a new publication tree. It may replace local capture locations with repository-relative evidence IDs in the export, while retaining checksums and an explicit mapping record. It must not rewrite the immutable freeze commit or claim that sanitized export text was the original historical text.

No public export, public push, release, or Zenodo publication is performed in Step 02.
