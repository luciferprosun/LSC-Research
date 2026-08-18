# Frozen Specification Kernel

Status: `FROZEN_SPECIFICATION_KERNEL_READY_NUMERICAL_EXECUTION_BLOCKED`

## Purpose

The Step 02 kernel is a machine-executable boundary around the evidence recovered in Step 01. It authenticates the historical object, exposes its symbolic structure, and refuses to manufacture the missing numerical object.

It is not a fit engine, a new LSC version, a likelihood implementation, or a physics-validation result.

## Immutable identity

| Field | Value |
|---|---|
| Model name | `LSC` |
| Canonical version | `6.3.0-pre-BEST2-freeze-update` |
| Historical Git commit | `6ffa07bdde533fcc2a550e36c762b8edd9236c47` |
| Validation Kernel input freeze commit | `a6d582694d55fa0260ef7ab07ed83fd06feef607` |
| Zenodo version DOI | `10.5281/zenodo.20377427` |
| Zenodo concept DOI | `10.5281/zenodo.19780615` |
| Symbolic equation source SHA-256 | `af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981` |
| Provenance registry SHA-256 | `f8c595a27f4352424712dab2300c2e01bdafd8cdda4ba5fabef50c1feb77d67c` |
| Source manifest SHA-256 | `e16b7b5ac775389aa3fdf5b319d0ecb3460eab3bf3126f850d1ef4da84c659ce` |
| Kernel schema version | `1.0.0` |

The Python identity object is a frozen dataclass. Bundle validation compares every identity field, not only the model version.

## Execution boundary

The evaluator performs these stages in order:

1. verify the immutable model identity;
2. verify the provenance-registry checksum;
3. admit the symbolic equation and parameter-structure sources;
4. validate the parameter-bundle schema and content hash;
5. validate every numerical source against the central provenance registry;
6. validate value shape, units, frames, tensor structure, and orientation;
7. test full-bundle completeness;
8. authorize or refuse execution.

The current authentic evidence fails closed at stages 5-7 because no complete authentic numerical bundle exists.

## Safe executable subset

Three source-defined operations have code:

- E4 checks that a supplied rank-2 square tensor is symmetric and traceless;
- E6 computes an observed-to-baseline ratio from explicitly supplied compatible scalars;
- E9 assembles the BEST ratio tuple from explicitly supplied ratios.

These functions are labelled `NON_PREDICTIVE_STRUCTURAL_CHECK_ONLY` or `NON_LSC_ALGEBRAIC_TRANSFORM_ONLY`. They cannot authorize or emit a numerical LSC prediction.

E1-E3, E5, E7-E8, and E10-E12 remain blocked where their authentic numerical, functional, covariance, timing, orientation, unit, or frame contracts are missing.

## Components

| Component | Location | Role |
|---|---|---|
| Identity | `src/lsc_kernel/frozen/identity.py` | Immutable release identity and mismatch rejection |
| Provenance | `src/lsc_kernel/frozen/provenance.py` | Single admission decision for all frozen objects |
| Parameter schema | `src/lsc_kernel/frozen/parameter_schema.py` | Value-free active and required-object contract |
| Bundle validator | `src/lsc_kernel/frozen/parameter_bundle.py` | JSON/hash/identity/provenance/unit/frame/shape gate |
| Units and frames | `src/lsc_kernel/frozen/units.py`, `frames.py` | Explicit known/missing contracts |
| Tensor | `src/lsc_kernel/frozen/tensor.py` | Rank, square, symmetry, trace, frame, and orientation contract |
| Equations and DAG | `src/lsc_kernel/frozen/equations.py`, `dependency_graph.py` | E1-E12 descriptors and deterministic dependencies |
| Evaluator | `src/lsc_kernel/frozen/evaluator.py` | Fail-closed execution boundary |
| Validation interfaces | `src/lsc_kernel/validation/` | Value-neutral future API; no T-test execution |
| CLI | `src/lsc_kernel/cli/main.py` | Machine-readable inspection and validation |

## Non-actions

Step 02 performed no parameter fit, no refit, no BEST/GALLEX/SAGE evaluation, no KATRIN or IceCube tuning, no likelihood calculation, no statistical-significance calculation, no T1-T12 execution, and no BEST-2 prediction.
