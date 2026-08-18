# LSC 6.4.0 STEP 07C reproducibility report

## Environment

- Python 3.12.3
- NumPy 2.5.2
- SciPy 1.18.0
- pytest 9.1.1
- Linux x86_64, glibc 2.39
- SciPy OpenBLAS 0.3.34.0.0, 64-bit integer interface, Haswell target
- dependency lock: `requirements-step07c.lock`

## Identities

| Object | SHA-256 |
|---|---|
| A2 model | `4a8f40e59431a27f8f4d5bc9809a706125a46ebdb5728458e4b04503e935b6f2` |
| Cross-section payload | `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5` |
| Response specification | `c548592b44d0f75ecfd24f2392e07492920711415b207cf74c4bd31526fdceb8` |
| Golden vectors | `3071c125f5840d530339b49de495c358402355e5ed44aee7f8272a24d44e498b` |
| Production evaluator | `215d76108119d4fbef25c681afc1f6890d4e5184fd3a1af9fff718754e079448` |
| Independent reference | `5dae5318662a188b510be39c873e9dc33d27d6e6b3262682722fb1f959393619` |
| Pre-fit freeze | `60380837f348cc41dc3d0b240fcba0b61a95c9f61cfab2bc3f5e7db71e9ea179` |
| Determination result | `86ab235e39237ef7ef86f3ce6609c2a33b9e36aab1b3940fac6e0736b8e08f7a` |

## Reproduction command

From the repository root:

```bash
PYTHONPATH=src:. .venv/bin/python tools/reproduce_step07c.py
```

This command is read-only. It verifies all pre-fit hashes, all 15 golden vectors, the independent reference calculation, and exact reproduction of the already frozen adverse result. It never invokes `execute_once` and cannot refit `alpha_0`.

## Double verification

Two fresh interpreter processes returned identical canonical receipts for:

- model identity;
- golden-vector count and results;
- pre-fit freeze identity;
- constrained/unconstrained diagnostics;
- failure verdict.

The scientific result is adverse but reproducible. No RC hash exists because the failure policy prohibits creating a parameter bundle or release candidate.
