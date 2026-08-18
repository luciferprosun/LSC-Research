# Third-party notices

The MIT license in `LICENSE` covers only original LSC Validation Kernel code
and documentation. Scientific inputs remain source-specific.

## Gallium capture cross section

The model uses the best-estimate gallium cross-section table associated with
John N. Bahcall, *Phys. Rev. C* **56**, 3391 (1997), DOI
`10.1103/PhysRevC.56.3391`, arXiv `hep-ph/9710491`. The frozen machine-readable
payload has SHA-256
`55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5`.

No explicit redistribution license for that author-hosted table was located
during STEP 08. Public packages therefore do not redistribute the payload.
They include `tools/acquire_bahcall_1997_payload.py`, which retrieves the
official author-hosted source, verifies source SHA-256
`bba57204fb909a846f8fd77034ef420755c10ffeeb07acb8adc1f043e921f92a`,
extracts the published best-estimate table, and verifies the frozen output
hash. Acquisition remains subject to the source site's terms.

## Source-line energies

The 51Cr and 37Ar line transcription is attributed to S. R. Elliott,
V. N. Gavrin, and W. C. Haxton, *Phys. Rev. C* **108**, 035502 (2023), DOI
`10.1103/PhysRevC.108.035502`, arXiv `2303.13623`. The arXiv author manuscript
is distributed under CC BY 4.0. The machine-readable transcription identifies
its source and modifications and has SHA-256
`ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e`.

## BEST development datum

The published BEST inner-zone aggregate ratio is attributed to V. V. Barinov
et al., *Phys. Rev. C* **105**, 065502 (2022), DOI
`10.1103/PhysRevC.105.065502`, arXiv `2201.07364`. The arXiv author manuscript
is distributed under CC BY 4.0. Only the cited aggregate value, uncertainty,
and provenance metadata are included; no paper source or PDF is redistributed.

APS versions of record may have separate publisher terms. Nothing in this
repository grants permission over those versions.
