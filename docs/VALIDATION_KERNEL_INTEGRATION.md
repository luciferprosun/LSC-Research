# Validation Kernel integration boundary

`validation-kernel/` is the complete imported LSC Validation Kernel source
tree. Its source identity is `luciferprosun/LSC-Validation-Kernel` commit
`0093befe65f8acef05a2c3d97711375f10218fec`, connected to this repository's
Git history by an unrelated-history merge and preserved beneath this module
path without altering its scientific artifacts.

The module retains its own package metadata, frozen manifests, third-party
notices, and append-only evidence chain. Its historical repository identity is
accepted only for records created before this integration; subsequent module
records identify `luciferprosun/LSC-Research#validation-kernel`.

This repository-level integration is organizational only. It does not change
the LSC 6.5.0 model, thaw any frozen parameter, authorize Phase 2 or BEST-2
execution, or create a scientific claim.

Run module verification from its directory:

```bash
cd validation-kernel
python3 tools/evidence_chain.py verify --require-current
python3 -m pytest -q tests
```

The full executable suite requires an explicitly acquired, hash-verified
Bahcall 1997 source payload and a locally generated release-candidate
directory. Those inputs are intentionally not committed or downloaded by the
public CI workflow because their redistribution boundary is source-specific.
