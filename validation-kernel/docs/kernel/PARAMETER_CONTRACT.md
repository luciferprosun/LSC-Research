# Frozen Parameter Contract

## Contract boundary

The canonical sources authenticate parameter names and roles. They do not authenticate a complete numerical vector. Consequently the schema contains descriptions and constraints but no numerical values.

Machine-readable sources:

- `frozen_core/parameters/frozen_parameter_schema.json`
- `frozen_core/parameters/frozen_parameter_bundle.schema.json`
- `frozen_core/parameters/frozen_missing_parameters.json`
- `frozen_core/parameters/unit_contract.json`
- `frozen_core/parameters/frame_contract.json`
- `frozen_core/parameters/tensor_contract.json`

## Required objects

| Canonical field | Symbol/role | Type | Numerical status | Unit status | Frame status |
|---|---|---|---|---|---|
| `theta` | complete parameter vector | vector | `MISSING` | `MISSING_FROZEN_UNIT` | not applicable |
| `parameter_ordering` | order of `theta` | ordered names | `MISSING` | not applicable | not applicable |
| `lambda0` | scalar response amplitude | scalar | `MISSING` | `MISSING_FROZEN_UNIT` | not applicable |
| `lambdaA` | anisotropic response amplitude | scalar | `MISSING` | `MISSING_FROZEN_UNIT` | not applicable |
| `f0_a` | `f0_a(E,t)` | function | `MISSING` | `MISSING_FROZEN_UNIT` | not applicable |
| `fA_a` | `fA_a(E,t)` | function | `MISSING` | `MISSING_FROZEN_UNIT` | not applicable |
| `active_anisotropy_tensor` | `A_a^{ij}` | rank-2 square tensor | `MISSING` | `MISSING_FROZEN_UNIT` | `MISSING_FROZEN_FRAME` |
| `tensor_orientation` | orientation of active tensor | orientation object | `MISSING` | not applicable | `MISSING_FROZEN_FRAME` |
| `complete_reference_frame` | ICRS/lab transform contract | frame object | `MISSING` | not applicable | `MISSING_FROZEN_FRAME` |
| `eta` | nuisance-parameter structure | structured vector | `MISSING` | `MISSING_FROZEN_UNIT` | not applicable |
| `covariance` | `C` | square matrix | `MISSING` | `MISSING_FROZEN_UNIT` | not applicable |
| `numerical_configuration` | equation/config binding | object | `MISSING` | not applicable | not applicable |
| `parameter_bounds` | final priors/bounds | object | `MISSING` | not applicable | not applicable |
| `numerical_defaults` | integration and normalization rules | object | `MISSING` | not applicable | not applicable |
| `frozen_prediction_table` | authentic precomputed predictions | table | `MISSING` | `MISSING_FROZEN_UNIT` | not applicable |
| `executable_evaluator_inputs` | complete E1-E12 inputs | object | `MISSING` | not applicable | not applicable |

`eta` and `C` are authentic active structures, but their numerical representation is not frozen. Their presence in the symbolic core is not a numerical admission.

## Bundle format

`FrozenParameterBundle` is JSON with these required top-level fields:

- `bundle_schema_version`;
- complete `model_identity`;
- `parameters`;
- `unit_definitions`;
- `frame_definitions`;
- `tensor_definitions`;
- `source_references`;
- `provenance_state`;
- `bundle_sha256`.

Each parameter entry contains `value`, `units`, `frame`, `dimensions`, and a provenance triple: registry `artifact_id`, official `classification`, and SHA-256.

The bundle digest is SHA-256 over canonical JSON excluding the `bundle_sha256` field. Unknown critical parameters and unknown entry fields are rejected.

## Tensor contract

The authentic E3-E4 structure establishes:

- expected rank: 2;
- square shape;
- symmetry `A_a^{ij}=A_a^{ji}`;
- tracelessness `Tr(A_a)=0`;
- required orientation and frame compatibility for directional use.

The frozen source does not establish the complete component dimension, active components, orientation, or full frame transform. The structural checker therefore does not infer a three-dimensional tensor and does not supply an orientation.

## No fallback rule

The schema has no defaults. A missing value cannot be filled from an older version, a similarly named field, a fitted result, a toy coefficient, or an illustrative number. A complete numerical bundle is currently impossible to validate from the available registry, which is the correct Step 02 result.
