# Validation split and hold-out policy

Split IDs, membership rules and ordering are serialized in `preregistration/splits.json`. Membership is based only on canonical dataset, zone, isotope, experiment and stable run IDs. Run folds use lexicographic canonical IDs. No split may be changed after seeing a prediction or held-out outcome.

The registry includes inner-to-outer and outer-to-inner BEST transfer, early-to-late BEST, four LORO families, four explicit LOEO families, BEST-to-GALLEX, BEST-to-SAGE, legacy-gallium-to-BEST, 51Cr-to-37Ar and experiment-family hold-out.

All current historical splits are `MODEL_EXPOSED`, `NON_BLIND_HISTORICAL`, and explicitly `holdout_is_clean_unexposed=false`. Calling them blind or pre-data is prohibited. They remain useful as out-of-sample software/statistical splits, but not as proof of an unexposed historical prediction.

BEST-2 is separate and `FUTURE_BLIND`. It has no observed rows and no split that authorizes a prediction in Step 03.

Controls and failures retain their source roles: SAGE secondary extractions are not silently promoted to independent primary observations, and GALLEX solar rows are not source-exposure hold-outs.
