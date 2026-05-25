# Git History Continuation Plan

## Goal

Continue LSC as an independent repository without treating mixed monorepo history as its canonical future root.

## Immediate state

- This repository was physically extracted into a standalone git root.
- Source ancestry remains documented, but commit history was not rewritten into this repo during extraction.

## Recommended continuation

1. Preserve this root as the forward authority for LSC scientific work.
2. Import selected source history later with `git filter-repo`, `git subtree`, or archival merge notes if full commit ancestry is required.
3. Keep `legacy/` content as provenance anchors until commit-level replay is completed.
4. Treat mixed-root READMEs and continuity bridge docs as archive references, not active LSC doctrine.

## Provenance anchors

- `WORKFLOW NOWE` source HEAD recorded in extraction log
- `LSC-6.0` source HEAD recorded in extraction log
- `neutrino-oscillations-pbh` source HEAD recorded in extraction log
