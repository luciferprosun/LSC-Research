# Package versus scientific-model versioning decision

Status: **PASS — INTENTIONALLY INDEPENDENT VERSION LINES**

## Decision

`pyproject.toml` and `src/lsc_kernel/__init__.py` identify the reusable
Validation Kernel software package as `0.6.0`. The frozen scientific artifact
identifies the exact finite-dilation model as LSC `6.5.0`. These numbers serve
different namespaces and are intentionally independent:

- software/package version: `lsc-validation-kernel 0.6.0`;
- scientific model version: `LSC 6.5.0`.

Repository history supports this distinction. Kernel Steps 2 through 6
advanced the package series from `0.2.0` through `0.6.0`. Later scientific
model work introduced LSC 6.4.0 and 6.5.0 without reassigning the kernel
package version.

## Release treatment

Public metadata must display both identifiers with their labels; a bare
`version` must not be used where its namespace is ambiguous. The release
notes, model card, READMEs, manifests, and citation metadata identify the
scientific artifact as 6.5.0 and separately state the kernel package version
where relevant.

No package-version edit is required for Phase 1. No scientific object or hash
was changed by this adjudication. A future kernel software release may advance
the `0.x` package line through normal software versioning without relabeling
the frozen LSC 6.5.0 model.

Verdict: `INDEPENDENT_PACKAGE_AND_MODEL_VERSION_LINES_DOCUMENTED`.
