# Frozen core gate

This directory contains authenticated symbolic representations and deterministic Step 02 manifests. It does not contain a recovered numerical LSC model.

- `equations/` contains E1-E12 descriptors and the source-bounded dependency DAG.
- `parameters/` contains the value-free schema, bundle JSON Schema, missing-object manifest, and unit/frame/tensor contracts.
- `manifests/` contains the immutable identity, current status, validation interfaces, and historical-artifact quarantine.

Every generated file is reproducible with `tools/generate_kernel_artifacts.py`. Missing numerical values remain `MISSING`.
