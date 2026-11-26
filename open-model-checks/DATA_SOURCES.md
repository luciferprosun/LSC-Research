# Data and attributions

## BEST gallium experiment

`data/best-rates.csv` transcribes the inner and outer ratios and their reported uncertainties from equation (20) of V. V. Barinov et al., *A Search for Electron Neutrino Transitions to Sterile States in the BEST Experiment*. The [arXiv author manuscript](https://arxiv.org/abs/2201.07364) carries [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The manuscript is also linked to [Phys. Rev. C 105, 065502](https://doi.org/10.1103/PhysRevC.105.065502). The transformation to CSV selects two rows and gives their columns English names. The synthetic inputs in the Python script are project-generated examples. No publication PDF or Bahcall cross-section table is bundled.

## Solar radio flux

`data/f107-monthly.csv` is a two-column extract of `time-tag` and `f10.7` from the [NOAA/NWS Space Weather Prediction Center Solar Cycle Progression observations](https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json), retrieved on 26 November 2026. The extract contains January 2005 through December 2024. The underlying 10.7 cm measurements are credited to the National Research Council Canada Solar Monitoring Program at the Dominion Radio Astrophysical Observatory. The [Canadian open-data record](https://data.asc-csa.gc.ca/dataset/cfd2331e-6d68-41c0-9cf2-f2e9c4d68eb7) lists the [Open Government Licence – Canada](https://open.canada.ca/en/open-government-licence-canada). The timestamp labels and source numbers are preserved in the extract. The `ssn` fields and other solar indices are omitted. This use does not imply endorsement by any data provider.

## Scientific models

- [LSC 6.5.0](https://doi.org/10.5281/zenodo.22007108), LuciferSun, flAmeBorn and LINZ HOSS. See the [validation kernel](https://github.com/luciferprosun/LSC-Research/tree/main/validation-kernel) for the frozen model and upstream reproduction procedure.
- [HNC Aureon Unified WhitePaper](https://doi.org/10.5281/zenodo.21526354), Gary Leckey, Aureon Institute. The preprint is CC BY 4.0. The example instantiates part of its equation as a single-oscillator prediction model and discloses all additional choices. It uses an independent implementation and does not redistribute Aureon OS code.
