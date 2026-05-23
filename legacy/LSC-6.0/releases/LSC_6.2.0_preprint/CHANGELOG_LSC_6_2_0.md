# LSC 6.2.0 Changelog

## Main Model Upgrade

LSC 6.2.0 advances the LSC 6.0 phenomenological framework by introducing a detector-frame tensor anisotropy formulation.

## Changes

- Reframed the newest model as a conservative preprint rather than a claim of confirmed new physics.
- Added detector-frame rank-2 tensor `D_ij`.
- Added separation between:
  - propagation-level true energy `E_true`,
  - detector-level reconstructed energy `E_rec`.
- Added reconstruction ansatz:

```text
E_rec = E_true [1 + alpha_D D_ij p^i p^j]
```

- Added traceless tensor parameterization:

```text
D_ij = delta (n_i n_j - delta_ij / 3)
```

- Added contraction:

```text
D_ij p^i p^j = delta [(p dot n)^2 - 1/3]
```

- Added standard-framework recovery limit:

```text
D_ij -> 0
delta_G -> 0
```

- Added binned chi-square comparison form:

```text
chi^2 = sum_k [N_obs,k - N_pred,k(D_ij, delta_G)]^2 / sigma_k^2
```

- Added explicit systematic/statistical uncertainty split:

```text
sigma_k^2 = sigma_stat,k^2 + sigma_sys,k^2
```

- Added validation targets:
  - gallium source experiments,
  - KATRIN,
  - IceCube,
  - standard oscillation data.

## arXiv Status

The preprint package is arXiv-ready and compiled successfully. The arXiv submission process is waiting for endorsement.

Endorsement request:

https://arxiv.org/auth/endorse?x=7KLAMS

## Zenodo Continuity

Recommended publication path:

- publish as a new version of the LSC 6.0 conceptual Zenodo record,
- preserve concept DOI continuity,
- assign LSC 6.2.0 its own version DOI through Zenodo's new-version mechanism.
