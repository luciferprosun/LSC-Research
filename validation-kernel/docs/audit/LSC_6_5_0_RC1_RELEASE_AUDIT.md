# LSC 6.5.0 RC1 release audit

Status: **PASS AS THE IMMUTABLE LOCAL SCIENTIFIC RC**

Audited directory: `release_candidate/LSC-6.5.0-rc1/` from input commit
`1f715b9b8777f89d17a84d340a24107531ccaed4`.

## Inventory and integrity

RC1 contains:

- README and explicit limitations/reproduction instructions;
- owner authorization and exact scientific specification/equations;
- scientific, pre-fit, parameter, and model-identity freezes;
- exact parameter-determination protocol/result and parameter bundle;
- cross-section/source-line provenance, interpolation policy, and payloads;
- production evaluator sources and independent reference/reproduction path;
- input, output, and parameter-bundle schemas;
- 29 golden/fail-closed vectors;
- environment and dependency locks;
- development disclosure and dataset manifest;
- preserved LSC 6.4.0 adverse-result record;
- citation metadata in the README/provenance records and scoped license
  metadata in `pyproject.toml`;
- machine-readable `MANIFEST.json` and `SHA256SUMS.txt`.

All `52/52` SHA256SUMS entries passed. The RC scientific objects resolve to
the same specification, payload, source-line, parameter bundle, and canonical
model hashes as the repository freeze. Two clean, sequential reproductions
from an exact archived RC checkout were byte-identical and each passed all
29 golden vectors, the independent parameter estimate/interval, model
identity, bundle identity, RC checksums, and preservation of the LSC 6.4.0
adverse result.

## Publication boundary

RC1 is retained byte-for-byte as the complete local audit object. It contains
the author-hosted Bahcall table, for which no explicit redistribution license
was located, so RC1 itself is not the public redistribution payload. The
separately prepared GitHub and Zenodo exports omit that table and provide
deterministic, hash-verifying acquisition instructions. This packaging repair
does not change RC1 or any scientific hash; therefore no RC2 is required.

Verdict: `RC1_SCIENTIFIC_AND_REPRODUCIBILITY_AUDIT_PASS`.
