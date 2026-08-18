# M3 Geometry Assessment

## Verdict

**PUBLISHED_AVERAGE_GEOMETRY**

No exact machine-readable source/detector volume model sufficient for production M3 integration was located for the gallium experiments. Published averages and Monte Carlo descriptions are useful but cannot be relabelled as exact geometry.

## Required M3 inputs

The sterile 3+1 survival probability is nonlinear in L/E. A production implementation therefore needs isotope line energies and weights plus the source-to-capture path-length distribution, or an authoritative integration implementation over source and target volumes. A single average path length is not generally equivalent to the volume integral.

## Dataset classification

| Dataset | Recovered geometry | Classification | Production consequence |
|---|---|---|---|
| BEST | Source cylinder and two-zone dimensions; average paths 52.03 plus/minus 0.18 cm and 54.41 plus/minus 0.18 cm; published Monte Carlo description | PUBLISHED_AVERAGE_GEOMETRY | Summary-rate approximation possible only under declared policy; exact L/E integration unavailable |
| SAGE 51Cr/37Ar | Central-source apparatus descriptions and average path 72.6 plus/minus 0.2 cm; published Monte Carlo statement | PUBLISHED_AVERAGE_GEOMETRY | Exact source/target volume integration unavailable |
| GALLEX Cr | Published effective geometry coefficients for the two campaigns | PUBLISHED_AVERAGE_GEOMETRY | No machine-readable L distribution or exact integration asset |

No dataset is classified EXACT_GEOMETRY for the production M3 path in the current archive. No geometry was reconstructed from photographs or schematic pixels.

## Gate

T10 may use M3 as an exact production baseline only after an authoritative geometry definition or validated collaboration integration code is acquired. Any interim average-length implementation must be labelled APPROXIMATE_GEOMETRY and SENSITIVITY_ONLY. It cannot support a claim that LSC outperforms an exact sterile prediction.
