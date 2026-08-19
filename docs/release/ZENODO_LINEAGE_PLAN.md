# Zenodo lineage plan

Status: **MODEL NEW VERSION PUBLISHED — COMPANION PENDING**

## Preserved historical model identity

- historical LSC 6.3.0 version DOI: `10.5281/zenodo.20377427`;
- historical model concept DOI: `10.5281/zenodo.19780615`;
- historical commit: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`.

The 6.3.0 record must remain unchanged. Its identity and symbolic lineage are
preserved, while its complete historical numerical state remains
incompletely recoverable.

## LSC 6.5.0 model record

The repository owner confirmed control of the existing LSC model lineage.
Zenodo's native **New version** operation was executed from record `20377427`
for LSC 6.5.0. It created a distinct version record and preserved the existing
concept DOI. The 6.3.0 version DOI was not reused or modified.

- published model version: `6.5.0`;
- existing concept DOI: `10.5281/zenodo.19780615`;
- new 6.5.0 version DOI: `10.5281/zenodo.22007108`;
- record: `https://zenodo.org/records/22007108`;
- upload performed: **YES**;
- DOI minted: **YES**;
- publication timestamp: `2026-08-19T06:08:44.682234+00:00`;
- uploaded ZIP SHA-256: `9f1f1ad0402c42602a37b064a5601b5827fcfaa31abe4a6481c321038b07a4e9`.

The uploaded payload is the deterministic `LSC-6.5.0.zip`, not the local RC1,
because the public ZIP omits material with unclear redistribution permission.
The published download was re-hashed and matched the audited local ZIP.

## Validation Kernel companion

Create the Validation Kernel as a separate linked Zenodo record with its own
concept/version identity, using `LSC-Validation-Kernel.zip`. Link it as a
companion to the model lineage after the model record exists. No companion DOI
has been assigned or invented.

The model publication is complete. No Validation Kernel record or GitHub
Release was created by this action.
