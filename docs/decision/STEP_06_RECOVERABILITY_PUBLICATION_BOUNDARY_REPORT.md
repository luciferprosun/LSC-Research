# STEP 06 Recoverability and Publication Boundary Report

## Technical summary

Project: **LSC Validation Kernel**

Status: **PASS**

Decision verdict: **`LSC_6_3_0_NUMERICALLY_UNRECOVERABLE_SUCCESSOR_BOUNDARY_DEFINED`**

The historical 6.3.0 identity and symbolic E1-E12 framework are recoverable. The complete numerical state is not recoverable with current admissible evidence, so exact numerical execution and frozen validation of 6.3.0 remain unauthorized. This is a reproducibility limitation and `TEST_BLOCKED` state, not `MODEL_FALSIFIED`.

The only honest completion path is a separately identified executable successor. The candidate name is **LSC 6.3.1** if E1-E12 and the model class remain unchanged. Any new values are 6.3.1 specifications, not recovered 6.3.0 values. Historical gallium analyses are retrospective/non-blind; BEST-2 remains future-blind and has no prediction.

Current publication readiness stops at **`P1_SPECIFICATION_BOUNDARY_READY`**. No model release, release tag, DOI action, LSC fit, LSC prediction, LSC validation, or BEST-2 prediction occurred.

## Scope, evidence, and decision method

STEP 06 is a decision and policy layer over the complete STEP 01-05 evidence chain. It does not reopen the numerical search, lower the evidentiary standard, or make parameter choices. The decision uses the exact STEP 05 input commit `030d5b0ce31aa3c065aea8267693058d7773c473`, the historical LSC commit `6ffa07bdde533fcc2a550e36c762b8edd9236c47`, and freeze commit `a6d582694d55fa0260ef7ab07ed83fd06feef607`.

The method separates:

1. identity recoverability;
2. symbolic recoverability;
3. numerical recoverability;
4. model falsification;
5. test authorization;
6. publication readiness.

Each conclusion is tied to the recovery registry, parameter adjudication, unlock matrix, negative findings, fail-closed kernel, validation contracts, and independent statistical controls. Missing evidence remains missing.

## A. 6.3.0 identity recoverability is complete

Verdict: **`FULLY_RECOVERABLE`**.

The model name/version, historical Git commit, freeze lineage, Zenodo version DOI, concept DOI, symbolic equation identity, and archive evidence agree. The historical identity is immutable:

- version: `6.3.0-pre-BEST2-freeze-update`;
- commit: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`;
- version DOI: `10.5281/zenodo.20377427`;
- concept DOI: `10.5281/zenodo.19780615`.

This establishes a citable historical object. It does not imply the presence of a complete executable parameter object.

## B. Symbolic recoverability is complete within the recovered scope

Verdict: **`FULLY_RECOVERABLE`**, symbolic only.

The canonical E1-E12 source is fixed at SHA-256 `af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981`. Parameter names/roles and the explicit freeze boundary are also authentic. All twelve equations have machine-readable descriptors.

Two graph edges remain `UNVERIFIED_DEPENDENCY` because their exact historical prediction binding is not source-defined. This uncertainty is retained instead of converted into an invented evaluation order.

## C. Numerical recoverability is not established

Verdict: **`NUMERICALLY_UNRECOVERABLE_WITH_CURRENT_EVIDENCE`**.

The available evidence does not supply a complete vector, ordering, numerical amplitudes, response functions, active tensor state, complete units/frames, covariance, initialization, bounds/defaults, evaluator configuration, or frozen prediction table. Historical candidates are toy, post-data, illustrative, version-conflicted, or semantically incomplete.

Consequences:

- 6.3.0 cannot be numerically executed without new decisions;
- an exact frozen validation of 6.3.0 cannot be performed;
- newly selected values cannot be labelled recovered 6.3.0;
- `prediction_authorized=false` and `numerical_validation_authorized=false` remain mandatory.

The wording “with current evidence” is essential. Private or unpublished evidence was outside the searched scope, so this is not a claim that a numerical object never existed.

## D. Historical 6.3.0 is preserved without repair

The [preservation policy](LSC_6_3_0_PRESERVATION_POLICY.md) fixes the historical tree, DOI meaning, canonical hashes, negative findings, and rejected artifacts. The 6.3.0 record remains immutable, identifiable, and citable with an explicit numerical-reconstruction limitation.

No historical file, nested repository, raw scientific source, equation, data file, Zenodo archive, or DOI metadata was modified. No history rewrite, rebase, force push, tag change, or release occurred.

## E. Scientific claims are bounded by capability, not optimism

The canonical [allowed-claims table](LSC_6_3_0_ALLOWED_CLAIMS.csv) permits publication of the recovered identity, symbolic equations, and scoped provenance. It prohibits unsupported capability claims for numerical reproducibility, historical prediction recovery, BEST/SAGE/GALLEX validation, KATRIN/IceCube vetoes, T12, and BEST-2 prediction.

Three states remain distinct:

| State | STEP 06 result | Publication meaning |
|---|---|---|
| `MODEL_FALSIFIED` | NO | No authorized numerical test produced a falsification result. |
| `MODEL_NOT_NUMERICALLY_RECOVERABLE` | YES | The historical executable object is incomplete. |
| `TEST_BLOCKED` | YES | Required model/data/mapping prerequisites are absent. |

### Approved publication language

- “The historical LSC 6.3.0 identity and symbolic E1-E12 specification are preserved.”
- “The complete numerical state could not be independently recovered from the available evidence as of 2026-08-16.”
- “LSC 6.3.1 is intended as an explicitly specified executable successor, not a retroactive completion of 6.3.0.”
- “Historical gallium analyses are retrospective/non-blind where the successor is model-exposed.”
- “Prospective tests are reported separately and require a pre-outcome model and prediction freeze.”

### Prohibited publication language without new evidence

- “6.3.1 reproduces exactly the original frozen 6.3.0 numerical model.”
- “6.3.0 passed independent validation.”
- “BEST blindly confirms 6.3.1.”
- “KATRIN or IceCube exclude or confirm LSC.”
- “The blocked T12 test falsifies or validates the directional component.”

## F. Data exposure makes historical gallium non-blind

BEST, GALLEX/GNO, SAGE 51Cr, and SAGE 37Ar are classified `MODEL_EXPOSED` and `NON_BLIND_HISTORICAL`. If 6.3.1 numerical choices are made with knowledge of these data, later analyses of the same data cannot become strict blind validation by naming or preregistration alone.

The code now rejects `MODEL_EXPOSED -> BLIND_STRICT` and `MODEL_EXPOSED -> PROSPECTIVE_BLIND` relabelling. Fit-derived parameters must disclose training data and remain non-predictive for those data.

## G. Retrospective validation has a precise role

Track A is labelled **`RETROSPECTIVE_NON_BLIND`**. It may support:

- model development;
- compatibility assessment;
- retrospective benchmark;
- parameter illustration;
- baseline comparison.

It may not support a strict blind confirmation claim. Frozen methodology, covariance labels, negative-result reporting, and the no-refit distinction remain required even for retrospective work.

## H. Prospective validation is reserved for truly future outcomes

Track B is labelled **`PROSPECTIVE_BLIND`** only when the full model, evaluator, target inputs, analysis policy, and prediction artifact are frozen and hashed before observed outcomes are accessed.

BEST-2 remains `FUTURE_ONLY` and `FUTURE_BLIND`. A future BEST-2 prediction additionally requires final as-built geometry, source specification/assay, exposure design, frozen nuisance/covariance policy, and a timestamped prediction artifact. STEP 06 generated no prediction value.

New gallium-source and independent experiments are `FUTURE_ELIGIBLE`, not automatically blind. Their exposure state must be adjudicated before data access.

## I. The 6.3.1 genesis contract is explicit

The [genesis contract](LSC_6_3_1_GENESIS_CONTRACT.md) establishes 6.3.1 as a reproducibility and executable-specification successor. Every active element must have exactly one class:

- `UNCHANGED_FROM_6_3_0_AUTHENTIC`;
- `FORMALIZED_FROM_6_3_0`;
- `NEW_NUMERICAL_SPECIFICATION_6_3_1`;
- `NEW_METHOD_6_3_1`;
- `HISTORICAL_REFERENCE_ONLY`;
- `UNRESOLVED`.

`UNRESOLVED` cannot enter an executable release. Newly specified content cannot be classified as authentic unchanged 6.3.0 content. Legacy values are never inherited silently.

## J. Versioning decision is conditional but unambiguous

The approved next design identity is **LSC 6.3.1 Explicit Numerical Specification + Executable Successor** if the symbolic equations and model class remain unchanged.

Use:

- `6.3.1` for explicit numerical completion, executable formalization, provenance, methodology, and reproducibility without physics change;
- `6.4.0` when a compatible but scientifically substantive physical/model extension is required;
- `7.0` when the model class or conceptual contract changes incompatibly.

The version must be escalated before freeze if STEP 07 crosses those boundaries. STEP 06 does not create a release branch or tag.

Future Git structure:

- keep the imported historical LSC tree and its original commit history read-only;
- keep LSC Validation Kernel as the separate provenance/methodology repository;
- develop successor content on a dedicated future branch such as `successor/lsc-6.3.1-specification`;
- place the versioned source, parameter bundle, JSON Schema, decision log, evaluator, golden vectors, and release manifest under a clearly versioned successor namespace;
- bind the final parameter bundle and release manifest to SHA-256 and, if the approved release workflow supports it, a cryptographic signature;
- create a release tag only after the complete clean-checkout gate passes;
- make the future tag point to the exact commit whose manifest records every release artifact hash.

Names are planning identifiers only. No branch, bundle, tag, signature, or release manifest is created in STEP 06.

## K. Zenodo and publication strategy is OPTION C

| Option | Advantages | Disadvantages | Citation semantics | 6.3.0 preservation | Reproducibility consequence |
|---|---|---|---|---|---|
| A - new model version in the existing version lineage | Clear model continuity; users can browse versions; exact successor gets its own persistent identifier. | Risks mixing model and methodology if the package is overloaded; requires careful limitation text. | Cite the new version DOI for 6.3.1 results and the historical version DOI for 6.3.0. The concept-level lineage may be used for the evolving model family. | Strong, provided the historical record is not edited and the Zenodo `New version` workflow is used. | Makes the successor reproducible if its files are complete, but does not independently identify the Validation Kernel methods. |
| B - separate Validation Kernel/reproducibility companion | Clean separation of physical model, audit software, and methodology; independent citation and release cadence. | Does not by itself create a citable executable 6.3.1 model; readers must follow relationships between records. | Cite the companion DOI for methods/software and historical DOI for 6.3.0. | Strong because no model-record mutation is needed. | Reproduces the audit framework, but leaves a future model successor needing its own release record. |
| C - both model version and separate companion | Preserves model lineage and gives the methodology an independent citable identity; supports exact citations for predictions and validation tooling. | Requires two synchronized records, explicit relations, compatible licenses, and clear user guidance. | Cite the 6.3.1 version DOI for model outputs and companion DOI for kernel/methods; cite both when both underpin a result. | Strongest if both records link to, but never rewrite, 6.3.0. | Separates model reproducibility from validation reproducibility while keeping both auditable. |

Recommendation: **OPTION C**.

1. Publish a future executable 6.3.1 model, when ready, through the existing Zenodo `New version` workflow so it remains linked to the 6.3 version lineage. It must receive a new version DOI. Before publication, verify in the draft that the intended concept DOI lineage is retained.
2. Publish the Validation Kernel/reproducibility package as a separate companion record with its own DOI and explicit relationship to the model release.

Zenodo states that a new version is a new record with separate files, metadata, and persistent identifier, linked to prior and future versions ([Manage versions](https://help.zenodo.org/docs/deposit/manage-versions/)). Zenodo also states that published record files and persistent identifiers are immutable ([About records](https://help.zenodo.org/docs/deposit/about-records/)). Therefore `10.5281/zenodo.20377427` must retain its historical meaning. No Zenodo action was taken.

## L. Executable successor requirements are frozen before implementation

The [executable release requirements](LSC_6_3_1_EXECUTABLE_RELEASE_REQUIREMENTS.md) require a complete parameter object, evaluator, unit/frame/tensor contracts, deterministic I/O, golden reference vectors, environment lock, provenance, source commit, hashes, and release manifest.

Golden cases must be experiment-independent and provide `input -> exact or precision-bounded expected output`. They may test types, equations, units, frames, tensor behavior, numerical stability, and fail-closed behavior, but may not be tuned to experiment results.

Current status:

- P0 historical preservation: READY;
- P1 specification boundary: READY;
- P2 executable successor: NOT READY;
- P3 release package: NOT READY;
- P4 retrospective validation: NOT READY;
- P5 prospective prediction: NOT READY.

## M. STEP 07 input contract prevents boundary erosion

`STEP_07_INPUT_CONTRACT.json` is hash-bound to `publication_boundary.json` and records:

- E1-E12 allowed for preservation only if unchanged;
- all unresolved numerical objects;
- required parameter-decision fields;
- allowed content classifications;
- provenance and exposure requirements;
- numerical bundle schema identity;
- freeze and golden-vector requirements;
- release naming and version-escalation rules;
- historical and prospective validation restrictions;
- all execution/publication gates as false.

STEP 07 may create a new explicit object. It may not call it recovered 6.3.0, run validation before freeze, or generate BEST-2 predictions.

## N. Tests and deterministic validation

Final validation results:

- full Python suite: **159/159 PASS**, plus **18/18 parameterized subtests**;
- STEP 06 tests: **18/18 PASS**;
- deterministic artifact regeneration: **39/39 byte-identical PASS**;
- preserved archive SHA-256: **1,882/1,882 PASS**;
- nested repositories: **4/4 clean**, exact expected HEADs, `git fsck` PASS;
- publication-path scan: **0 findings**;
- high-confidence secret scan: **0 findings across 25 changed/new files**;
- local documentation links: **47/47 PASS**;
- `git diff --check`: **PASS**;
- parent `git fsck`: **PASS** with informational dangling blobs and no broken-object error;
- dependency consistency: **PASS**;
- `can-predict`: **NO**, expected exit code 2;
- `run-validation T11 --model LSC`: **BLOCKED before statistic**, expected exit code 2;
- LSC fits/refits: **0**;
- numerical LSC predictions: **0**;
- T1-T12 numerical LSC validations: **0**;
- BEST-2 predictions: **0**;
- Zenodo actions, releases, tags, and pushes: **0**.

The golden STEP 06 state passes only when historical identity is preserved, numerical recovery remains incomplete, the successor boundary is defined, historical data remain retrospective, BEST-2 remains future-blind, and publication remains unauthorized.

## O. Git state and changed scope

Input branch: `main`.

Input STEP 05 commit: `030d5b0ce31aa3c065aea8267693058d7773c473`.

One logical STEP 06 commit will use subject:

`Step 06: define recoverability and successor publication boundary`

Created scope:

- decision-policy Python module and regression gates;
- required `docs/decision/` documents and claims CSV;
- `publication_boundary.json`;
- `STEP_07_INPUT_CONTRACT.json`;
- deterministic STEP 06 golden state;
- STEP 06 generator and tests.

Modified scope:

- README and kernel-status documentation;
- package/status metadata;
- deterministic generated manifests whose version/status fields include STEP 06.

No historical, physics, raw-data, infrastructure, or publication mutation is in scope. No push is authorized.

## P. Remaining blockers are explicit

1. A complete new 6.3.1 parameter decision and bundle.
2. Exact response functions, units, frames, active tensor, orientation, initialization, bounds/defaults, and numerical conventions.
3. A deterministic full evaluator and golden numerical vectors.
4. Complete release provenance, environment, manifest, commit, and future tag.
5. Authenticated collaboration covariance/likelihood where inferential historical claims require it.
6. Justified external mappings where KATRIN or IceCube is invoked.
7. Exact geometry for production M3 where required.
8. Complete T12 timing/orientation/geometry/tensor/frame/unit/statistic prerequisites.
9. Authoritative BEST-2 as-built/source/exposure inputs before prospective prediction freeze.

These blockers prevent execution or stronger inference. They do not alter the STEP 06 recoverability decision.

## Q. STEP 07 readiness

**READY FOR STEP 07: YES**

Recommended STEP 07:

**STEP 07 - LSC 6.3.1 Explicit Numerical Specification + Executable Successor**

Readiness means the genesis and publication boundaries are complete enough to control a new specification. It does not mean the numerical values, executable model, release, retrospective validation, or prospective prediction are ready.

## Limitations and questions carried forward

- Would STEP 07 preserve E1-E12 exactly, or does scientific completion require a 6.4.0/7.0 change?
- What non-post-hoc rule will determine each new parameter and uncertainty?
- Which values, if any, are fit-derived, and which datasets become training data?
- Can authoritative collaboration covariance/likelihood objects be obtained before retrospective inference?
- What exact future target inputs can be frozen without accessing outcomes?
- What authorship, license, and citation metadata should be used for the model release and companion record?

These are design questions for STEP 07 and later human publication review. STEP 06 does not answer them by inventing values.
