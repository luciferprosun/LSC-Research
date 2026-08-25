# LSC Evidence Chain

This directory is the append-only integrity and chronology layer for the LSC
material identified in `scope.json`. It is designed to make later alteration,
misattribution, or unattributed copying easier to detect and document.

## What is bound

Each line of `chain.jsonl` is one canonical JSON record. A record binds:

- the repository and its authority role in the LSC research line;
- a sorted manifest of the staged files selected by `scope.json`;
- the SHA-256 digest, byte length, Git mode, and type of every selected file;
- the SHA-256 digest of the complete manifest;
- the SHA-256 digest of the scope definition;
- the parent Git commit, UTC recording time, recorder, and purpose statement;
- the digest of the preceding record; and
- the digest of the complete current record.

The chain file excludes itself because a file cannot contain its own final
digest. Its integrity is instead protected by record-to-record links, Git
history, the central LSC network checkpoint, and—on eligible public
repositories—a GitHub/Sigstore artifact attestation.

## Verification

Run from the repository root:

```bash
python3 tools/evidence_chain.py verify --require-current
```

Verification fails if the JSONL structure is non-canonical, a record digest or
link is invalid, the scope changed without a new record, or the current staged
manifest differs from the newest record.

## Recording an authorized update

1. Make the intended changes.
2. Stage every in-scope change with Git.
3. Append a record:

   ```bash
   python3 tools/evidence_chain.py snapshot \
     --event update \
     --statement "Concise description of the research change"
   ```

4. Verify with `--require-current`.
5. Stage `evidence-chain/chain.jsonl` and commit it together with the research
   changes.

Never edit, delete, reorder, or reformat existing JSONL lines. Corrections are
new records with event `correction`; they do not rewrite history.

## Trust and legal boundary

This mechanism supplies tamper-evident integrity and chronology evidence. It
does not by itself prove originality, scientific correctness, legal ownership,
or the identity of a human author. Repository administrators can rewrite Git
history, so externally visible commits, DOI deposits, cross-repository
checkpoints, and Sigstore attestations remain important independent anchors.

Hashing a third-party work records custody only; it never transfers copyright
or authorship. `RESEARCH_ATTRIBUTION.md`, `CITATION.cff`, the repository
license, and third-party notices remain authoritative for attribution and use.
This evidence layer does not change any existing license.
