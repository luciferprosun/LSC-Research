# LSC 6.3.0 Preservation Policy

## Policy result

Historical LSC 6.3.0 is preserved as an immutable, identifiable, citable symbolic release with an incompletely recoverable numerical state.

Canonical identifiers:

- historical version: `6.3.0-pre-BEST2-freeze-update`;
- historical Git commit: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`;
- Validation Kernel input freeze: `a6d582694d55fa0260ef7ab07ed83fd06feef607`;
- freeze tag: `pre-validation-kernel-recovery`;
- Zenodo version DOI: `10.5281/zenodo.20377427`;
- Zenodo concept DOI: `10.5281/zenodo.19780615`.

## Immutable objects

The following objects must not be rewritten, replaced, or assigned a successor meaning:

1. historical Git tree and commit lineage;
2. files in the historical Zenodo record;
3. version DOI `10.5281/zenodo.20377427`;
4. canonical E1-E12 source and its SHA-256;
5. canonical core and freeze-boundary sources;
6. historical toy, illustrative, post-data, and deprecated artifacts;
7. STEP 01-05 recovery, provenance, and negative-evidence records.

Preserving a rejected artifact does not promote it. Its original status remains part of the evidence.

## Mandatory limitation statement

Any future citation or description that discusses numerical reproducibility must state:

> The historical identity and symbolic E1-E12 specification of LSC 6.3.0 are preserved. Its complete numerical parameter state and executable evaluator could not be independently recovered from the available evidence as of 2026-08-16.

This limitation is not optional metadata and may not be hidden behind a later implementation.

## Prohibited preservation actions

- Do not edit the historical release to add newly specified values.
- Do not move the historical version DOI to a successor.
- Do not create a replacement bundle labelled as authentic frozen 6.3.0.
- Do not combine 6.3 equations with 6.2 coefficients, a 5.5 tensor, or toy normalization.
- Do not delete negative findings or failed historical results.
- Do not rewrite Git history to make later methodology appear contemporaneous with 6.3.0.
- Do not relabel post-data objects or historical analyses as clean predictions.

## Permitted preservation actions

- Add external addenda that link to, but do not alter, the historical record.
- Preserve hashes, manifests, source inventories, and provenance registries.
- Publish a successor with a distinct version identity and explicit relationship to 6.3.0.
- Publish the Validation Kernel as a separately citable reproducibility companion.
- Adjudicate newly located historical evidence without changing the original artifact.

## DOI integrity

The historical version DOI must continue to identify its original files. Zenodo documents that published records have immutable files and persistent identifiers, and that substantive file updates should be represented by a new version. See [Zenodo: About records](https://help.zenodo.org/docs/deposit/about-records/) and [Zenodo: Manage versions](https://help.zenodo.org/docs/deposit/manage-versions/).

No Zenodo action is authorized by this policy. Publication remains a later manual step.

## Verification

Preservation is checked by:

- the 1,882-file historical SHA-256 manifest;
- nested repository HEAD and clean-worktree checks;
- fixed hashes for canonical equations and freeze boundary;
- regression tests preventing identity reassignment and numerical promotion;
- `git fsck` on the Validation Kernel and nested repositories.
