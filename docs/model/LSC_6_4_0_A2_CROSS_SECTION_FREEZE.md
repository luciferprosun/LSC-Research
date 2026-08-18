# LSC 6.4.0 A2 cross-section freeze

Status: **PASS — A2 cross-section function available**

## Decision

The STEP 07C hard gate passes with one frozen conventional scenario:

`BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE`

This is a numerical representation decision made before `alpha_0` determination. It is not selected by LSC fit quality and is not a claim that other nuclear calculations are invalid.

## Evidence adjudication

The 2023 calculation by Elliott, Gavrin, and Haxton, DOI `10.1103/PhysRevC.108.035502`, is the primary modern source for the exact six `51Cr` and three `37Ar` line energies and branchings. Its local source bundle contains analytic ground-state machinery and aggregate cross sections, but no complete continuous executable total-cross-section curve.

Bahcall's 1997 calculation, DOI `10.1103/PhysRevC.56.3391`, supplies 58 positive best-estimate cross-section points from 0.240 through 30.000 MeV. Crucially, the paper explicitly instructs users to fit the table with a cubic spline and states that the table reproduces standard-spectrum best-estimate cross sections to 1% or better. This is the authoritative support for a continuous representation.

No plot digitization, residual-driven selection, or hidden curve reconstruction is used.

## Frozen representation

| Object | Frozen value |
|---|---|
| Interpolation coordinates | linear `E`, linear `sigma` |
| Family | piecewise cubic spline |
| Endpoint convention | natural second-derivative boundary |
| Continuity | `C2` |
| Derivative | analytic derivative of each cubic segment |
| Extrapolation | forbidden |
| Energy unit | MeV |
| Cross-section unit | `10^-46 cm^2` |
| Arithmetic | IEEE-754 binary64 |

Bahcall specifies the interpolation family, not the endpoint boundary. The natural boundary is explicitly classified as a numerical representation convention. A not-a-knot sensitivity calculation agrees with the natural spline at the source lines to numerical precision. PCHIP gives visibly different derivatives and is therefore not silently interchangeable with the frozen model.

## Integrity

| Artifact | SHA-256 |
|---|---|
| Best-estimate CSV | `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5` |
| Source-line JSON | `ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e` |
| Provenance manifest | `f428477ffa8b5077b64c16a53b887ec3f17bea87445e7fcf8dc1e8fea39ca73e` |
| Interpolation policy | `604028a6c846a7fe7ff3173f211410087d63a1e89a21c2f1f5b93f6bd9f21ec7` |
| Response specification | `c548592b44d0f75ecfd24f2392e07492920711415b207cf74c4bd31526fdceb8` |

## Source-line checks

- `51Cr`: six branchings sum exactly to one; baseline-weighted `mean_F_m = 1.8020760538663734`.
- `37Ar`: three branchings sum exactly to one; baseline-weighted `mean_F_m = 1.7195489304485911`.
- Interpolated source-line cross sections are finite and positive.
- The production spline and an independent standard-library natural-spline implementation agree over a 101-point source-energy grid.

## Limitation

The publications establish cross sections and the spline representation, but do not publish a separate uncertainty guarantee for the logarithmic derivative. `F_m` is therefore representation-defined conventional input with exact provenance. This limitation is exposed in every production output.
