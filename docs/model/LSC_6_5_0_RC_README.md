# LSC 6.5.0 RC1

This is an unpublished release candidate for the exact finite-dilation LSC 6.5.0 model.

The model has exactly one universal physical parameter, `alpha_0`, and computes

`R_pred = sum_i c_i sigma(E_i exp(alpha_0)) / sum_i c_i sigma(E_i)`.

The tensor and directional sectors are disabled. No experiment-, isotope-, zone-, exposure-, or run-specific LSC coefficient exists.

The frozen parameter was determined retrospectively from BEST inner under `COV_DIAGONAL`; this is development, not validation. Read `LSC_6_5_0_DEVELOPMENT_DISCLOSURE.md` and `LSC_6_4_0_ADVERSE_RESULT_RECORD.md` before interpreting the model.

Run the integrity and reproduction check from the RC root:

```bash
PYTHONPATH=src python3 tools/reproduce_lsc650.py
```

The command performs no refit and writes no result. It independently recalculates the frozen objective and verifies the stored parameter, hashes, golden vectors, and manifest.

This RC is not a public release, has no DOI, makes no validation claim, and contains no BEST-2 prediction.
