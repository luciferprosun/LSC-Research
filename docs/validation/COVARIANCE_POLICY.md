# Covariance policy

No complete public gallium collaboration covariance was found. The kernel therefore freezes five named scenarios:

- `COV_DIAGONAL`: explicit marginal variances only, off-diagonal zero;
- `COV_UNCORRELATED_SYSTEMATICS`: published systematic components independent unless explicitly common;
- `COV_FULLY_COMMON_SELECTED`: only preregistered named shared nuisances fully correlated;
- `COV_PLAUSIBLE_SCAN`: a correlation grid/range frozen before outcomes;
- `COV_COLLABORATION`: enabled only after an authentic collaboration matrix/likelihood and nuisance definition are acquired and hash-verified.

The first four are assumption-based sensitivity tools. They may not support the words discovery, exclusion, sigma evidence or decisive preference, and they may not be described as collaboration covariance. `COV_COLLABORATION` is currently unavailable.

Cross-section correlations require special care: 51Cr and 37Ar share nuclear, atomic and transition inputs, but the archive has no complete numerical joint covariance. The registered models are scanned without selecting a preferred model after results. Krofcheck and Frekers alternatives are not combined.

Every run manifest must name exactly one scenario. Scenario envelopes are reported completely; no scenario is selected after inspecting LSC performance.
