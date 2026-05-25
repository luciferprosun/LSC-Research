# LSC 6.2.1 Codex Analysis

Working continuation on the gallium source data package.

## Selected Fit

| coefficient | value |
| --- | ---: |
| beta_length | -0.39830548 |
| beta_shape | -0.71268732 |
| beta_source | 0.14607627 |
| beta_zone | 0.01969744 |
| beta_intercept | -0.13689794 |
| condition number | 78.224 |

## Anchor Predictions

| name | observed R | predicted R | residual |
| --- | ---: | ---: | ---: |
| BEST_inner | 0.790000 | 0.790000 | +0.000000 |
| BEST_outer | 0.770000 | 0.770000 | -0.000000 |
| GALLEX_combined | 0.882000 | 0.882000 | +0.000000 |
| SAGE_51Cr | 0.950000 | 0.950000 | +0.000000 |
| SAGE_37Ar | 0.790000 | 0.790000 | +0.000000 |

## Validation Predictions

| name | observed R | predicted R | residual |
| --- | ---: | ---: | ---: |
| BEST_ratio | 0.970000 | 0.974684 | +0.004684 |
| GALLEX_Cr1 | 0.953000 | 0.882000 | -0.071000 |
| GALLEX_Cr2 | 0.812000 | 0.882000 | +0.070000 |

## Leave-One-Out

| omitted | predicted R | observed R | residual |
| --- | ---: | ---: | ---: |
| BEST_inner | 0.965858 | 0.790000 | +0.175858 |
| BEST_outer | 0.941584 | 0.770000 | +0.171584 |
| GALLEX_combined | 0.583630 | 0.882000 | -0.298370 |
| SAGE_51Cr | 0.789343 | 0.950000 | -0.160657 |
| SAGE_37Ar | 0.817808 | 0.790000 | +0.027808 |

## Notes

- mean source cross section, 51Cr: 5.749407e-45 cm^2
- mean source cross section, 37Ar: 7.011960e-45 cm^2
- the anchor fit is exact by construction, so leave-one-out is the real stability check
- GALLEX source-by-source split remains a useful nuisance test
