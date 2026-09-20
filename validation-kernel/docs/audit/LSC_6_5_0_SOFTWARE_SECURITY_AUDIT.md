# LSC 6.5.0 software and security audit

Status: **PASS**

Scope: frozen RC1 production evaluator, contracts, cross-section layer,
reference/reproduction tooling, schemas, manifests, and prepared public
exports. This is a Python scientific CLI/library artifact, not a network
service.

## Critical findings

None. Count: **0**.

## High findings

None. Count: **0**.

## Medium findings

None. Count: **0**.

## Informational controls

### INFO-01 — Scientific values are hash-bound, not hidden defaults

`src/lsc_kernel/lsc650/cross_section.py:52`--`56` hard-code the authorized
scenario and immutable hashes deliberately. Lines 75--144 verify the payload,
source lines, specification, freeze, and final identity before construction.
These are tracked bindings, not untracked scientific defaults.

### INFO-02 — Fail-closed parsing and domain behavior

`src/lsc_kernel/lsc650/contracts.py:89`--`164` rejects unknown/missing keys,
unsupported profiles, modified authoritative lines, mismatched bundle hashes,
and observed outcome content. `cross_section.py:162`--`174` and `193`--`230`
reject non-finite or out-of-support inputs. The spline is created with
`extrapolate=False` at line 71.

### INFO-03 — No unsafe deserialization or command construction

The RC uses strict JSON and CSV parsing. Searches found no `pickle`, `marshal`,
unsafe YAML loader, dynamic `eval`/`exec`, `os.system`, `shell=True`, or
string-built shell command. The reproduction subprocess uses an argument list
and a fixed local test target.

### INFO-04 — Network access is not part of prediction

Production and reproduction do not access the network. The publication-only
Bahcall acquisition utility performs an explicit user-invoked HTTPS request
with a 30-second timeout, a 100,000-byte cap, an exact source hash, strict
parsing, an exact output hash, and exclusive-create output semantics. A
mismatching existing file is never overwritten.

### INFO-05 — Determinism and cache independence

The evaluator has no random source, wall-clock input, environment-dependent
scientific fallback, or cache. Dependencies and numerical policy are frozen.
Two clean RC reproductions were byte-identical. Deterministic package ZIPs
fix member order, timestamp, mode, and compression settings, and were rebuilt
twice independently.

### INFO-06 — Public-package isolation

The export allowlist omits repository metadata, caches, bytecode, SQLite/private
state, session data, temporary artifacts, the local historical bulk archive,
and the author-hosted cross-section table whose redistribution permission is
unclear. Public scans reject local absolute paths, private-key markers, common
token prefixes, caches, databases, and the omitted payload.

## Additional software checks

- hidden alternate physics path: none;
- undocumented prediction-affecting input: none;
- absolute path or username dependency: none;
- secret/token/auth material in the public packages: none;
- private URL or repository state in the public packages: none;
- cache dependence or nondeterministic prediction path: none;
- unsafe overwrite by the acquisition utility: none;
- critical software/security findings: **0**.

Verdict: `SOFTWARE_AUDIT_PASS_ZERO_CRITICAL_FINDINGS`.
