# Open Model Checks

Reproduce two model comparisons from traceable input data. This post-freeze open-data demonstration builds on LuciferSun's LSC neutrino research and Gary Leckey's Harmonic Nexus Core (HNC) preprint. Both cases record their inputs, baseline, evaluation boundary and result. The [JSON-LD graph](provenance.jsonld) links scientific sources to the inputs and outputs, and [source notices](DATA_SOURCES.md) document licenses.

| Case | Comparison | Result |
|---|---|---|
| Gallium-source neutrinos | Energy-dependent response versus a free overall normalization | Under equal energy weights, both give an outer-zone ratio of 0.790 when matched to the published inner ratio. The published outer ratio is 0.77. The two ratios do not by themselves identify the energy-dependent response under this assumption. |
| Monthly F10.7 solar radio flux | HNC-inspired nonlinear feedback versus an equally sized linear model and last-month persistence | Held-out one-month prediction RMSE in solar flux units is 26.98 for HNC-inspired feedback, 14.40 for the matched linear model and 12.31 for persistence. The nonlinear variant loses on this split. |

## Run it

Download this branch or the two input files and the script in their existing directory layout. Run `python3 run.py` from this folder, with Python 3.10 or newer. No packages, credentials, external services, or downloads are required during execution.

- The two frozen input tables are [BEST rates](data/best-rates.csv) and [F10.7 monthly observations](data/f107-monthly.csv).
- The script writes [model-comparison summaries](results/summary.json) and [all 84 holdout observations and predictions](results/f107-holdout.csv).
- [Input checksums](SHA256SUMS) let readers check that they have the same source tables.

## Case 1 · Structural check using public BEST rates

The [frozen LSC 6.5.0 model](https://doi.org/10.5281/zenodo.22007108) changes the energy argument of the gallium capture cross section, `E′ = E exp(α₀)`. The release fitted its constant retrospectively to the published inner zone. If both zones average the response factor with identical weights, the rate multiplier is identical in both zones. A free overall normalization matched to the same inner result therefore yields the same outer prediction. The measured outer value was already public and is not a blind test. The difference from the prediction is reported as a raw residual because this demonstration has no joint covariance.

The code also uses two explicitly synthetic response factors (0.71 and 0.87) to illustrate how altered weights can break the equality. Equal weights average to 0.790. Changing the outer weights to 0.8 and 0.2 yields 0.742, while free normalization remains 0.79. These illustrative factors do not come from a cross-section table. The example is a structural check and does not numerically rerun the frozen model or predict a future BEST result.

## Case 2 · Held-out check of a discrete HNC-inspired variant

[Leckey's HNC preprint](https://doi.org/10.5281/zenodo.21526354) describes a sum of oscillatory terms, saturating `tanh` feedback and a delayed term. For a single operational demonstration, both fitted models use an intercept, an eleven-year sine/cosine pair and the observed twelve-month lag. The HNC-inspired model adds `tanh` of the preceding month's standardized value. The matched model uses the preceding month's standardized value directly. Persistence predicts the last observed month. The period and delay are demonstration choices, and the solar application is distinct from the original HNC paper's applications.

Preprocessing and coefficients use 2005–2017 only, with 144 fitted targets after the lag. The score uses 84 one-step predictions from January 2018 to December 2024. Test-time lagged observations are only used once they would have been available. This retrospective split tests one operational variant of the feedback term and does not test the broader HNC framework. The comparisons do not establish a connection between solar flux and gallium neutrino measurements.

## Credits

Submitted by Łukasz Żuchowski (LuciferSun). LSC 6.5.0 is credited to LuciferSun, flAmeBorn and LINZ HOSS. The HNC equation is credited to Gary Leckey, Aureon Institute. The Python demonstration and JSON-LD graph are released under [MIT](LICENSE). Source data keep the terms listed in [DATA_SOURCES.md](DATA_SOURCES.md).
