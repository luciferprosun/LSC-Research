# Covariance engine

## Validation contract

`CovarianceMatrix` requires a non-empty square, finite, symmetric, positive-semidefinite matrix with dimensions matching the observation vector. Diagnostics record shape, tolerances, eigenvalue extrema, rank, conditioning, singularity, and inversion strategy.

There is no implicit matrix repair. A singular matrix is rejected by default. Pseudoinverse use requires `SingularPolicy.PSEUDOINVERSE`; the `rcond`, effective rank, and fallback warning are then present in the result. A matrix with a materially negative eigenvalue is rejected rather than clipped.

## Frozen scenarios

The engine implements exactly the Step 03 scenarios:

- `COV_DIAGONAL`: explicit marginal variances only;
- `COV_UNCORRELATED_SYSTEMATICS`: statistical and declared systematic variances added diagonally;
- `COV_FULLY_COMMON_SELECTED`: only named shared effects enter as an outer product;
- `COV_PLAUSIBLE_SCAN`: the complete preregistered correlation grid `0.00, 0.25, 0.50, 0.75, 0.90`;
- `COV_COLLABORATION`: unavailable unless an authenticated collaboration matrix is supplied.

The first four are `SENSITIVITY_ONLY`. A correlation point is never selected by fit quality, and the complete scan must be reported. These scenarios cannot support discovery, exclusion, sigma evidence, or decisive-preference language.

## Public control diagnostics

The machine-readable record is `statistics/statistical_control_diagnostics.json`.

- MicroBooNE: 364×364, finite, symmetric, PSD, rank 364; positive-subspace condition number approximately `6.68e8`.
- PROSPECT: all three archived matrices are 990×990, finite, and symmetric. Their individual spectra show rank deficiency and negative eigenvalues at archived precision. This is reported, not repaired. They pass the requested file/shape/symmetry/finite control but are not automatically admissible as standalone likelihood covariances.
- STEREO: archived covariance is 44×44, finite, symmetric, and PSD; the 22-bin prompt-energy axis matches the response prompt axis. The response's second axis is neutrino energy and is intentionally not equated with prompt energy.

These datasets are `STATISTICAL_ENGINE_CONTROL`, not evidence for LSC.
