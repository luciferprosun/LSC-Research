# LSC 6.5.0 license and provenance audit

Status: **PASS WITH NON-REDISTRIBUTION CONTROL**

## Original project material

New Validation Kernel source and documentation are prepared under the MIT
license in `LICENSE`. That license explicitly does not relicense external
scientific publications, tables, or transcriptions.

## Gallium capture cross section

Source: John N. Bahcall, *Phys. Rev. C* **56**, 3391 (1997), DOI
`10.1103/PhysRevC.56.3391`, arXiv `hep-ph/9710491`; author data page and exact
author-hosted table URL are recorded in the frozen provenance manifest. The
archived source SHA-256 is
`bba57204fb909a846f8fd77034ef420755c10ffeeb07acb8adc1f043e921f92a`.
The deterministic 58-row best-estimate transcription SHA-256 is
`55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5`.

No explicit redistribution license for the author-hosted table was found.
Consequently no public package redistributes the table, its mirror, paper
PDF, or paper source. `tools/acquire_bahcall_1997_payload.py` instead performs
explicit deterministic acquisition, verifies the source bytes, extracts only
the frozen Best table, and verifies the final payload hash. Use remains
subject to the source site's terms.

## Source-line energies

Source: S. R. Elliott, V. N. Gavrin, and W. C. Haxton, *Phys. Rev. C* **108**,
035502 (2023), DOI `10.1103/PhysRevC.108.035502`, arXiv `2303.13623`. The
machine-readable six-line Cr51 and three-line Ar37 transcription records its
source and modifications and has SHA-256
`ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e`.
The arXiv record identifies CC BY 4.0 for the author manuscript. Attribution
and source/license notices are present; APS versions may have separate terms.

## BEST development aggregate

Source: V. V. Barinov et al., *Phys. Rev. C* **105**, 065502 (2022), DOI
`10.1103/PhysRevC.105.065502`, arXiv `2201.07364`. The one aggregate value and
published uncertainty are recorded with exact source hashes. No PDF, paper
source, or run-level dataset is redistributed in the model export. The arXiv
record identifies CC BY 4.0 for the author manuscript; attribution is present.

## Other historical material

The multi-gigabyte historical archive is excluded from public packages. It is
used locally only for lineage and hash evidence. Public packages include
citations, hashes, frozen adverse-result metadata, and acquisition/provenance
instructions rather than unlicensed mirrors.

Critical licensing/provenance findings after mitigation: **0**. The publication
package is not blocked, provided the omission/acquisition policy remains in
force.

Verdict: `PUBLICATION_SAFE_PROVENANCE_WITH_BAHCALL_NON_REDISTRIBUTION`.
