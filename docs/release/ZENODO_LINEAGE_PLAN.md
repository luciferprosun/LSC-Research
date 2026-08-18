# Zenodo lineage plan

Status: **PREPARED — NOT EXECUTED**

## Preserved historical model identity

- historical LSC 6.3.0 version DOI: `10.5281/zenodo.20377427`;
- historical model concept DOI: `10.5281/zenodo.19780615`;
- historical commit: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`.

The 6.3.0 record must remain unchanged. Its identity and symbolic lineage are
preserved, while its complete historical numerical state remains
incompletely recoverable.

## LSC 6.5.0 model record

If the repository owner confirms that the existing Zenodo record controls the
same LSC model lineage, use Zenodo's **New version** operation from that record
for LSC 6.5.0. This must create a new version record and a new version DOI
while preserving the existing concept DOI. Do not reuse the 6.3.0 version DOI
for 6.5.0.

- proposed model version: `6.5.0`;
- existing concept DOI: `10.5281/zenodo.19780615`;
- new 6.5.0 version DOI: **not assigned**;
- upload performed: **NO**;
- DOI minted: **NO**.

The upload payload is the deterministic `LSC-6.5.0.zip`, not the local RC1,
because the public ZIP omits material with unclear redistribution permission.
Before upload, a human must review creators, affiliations, dates, access
rights, related identifiers, and the final package checksum.

## Validation Kernel companion

Create the Validation Kernel as a separate linked Zenodo record with its own
concept/version identity, using `LSC-Validation-Kernel.zip`. Link it as a
companion to the model lineage after the model record exists. No companion DOI
has been assigned or invented.

No Zenodo API call, upload, publication, or DOI reservation is authorized by
this plan.
