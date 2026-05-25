# LSC Request for Data Access

## Purpose

This document defines the data needed to test, constrain, falsify, or reject LSC within the frozen pre-BEST-2 validation framework. It is a request-for-data instrument, not a theory extension.

## General Required Data Classes

| Data class | Why it matters | Validation enabled | What remains impossible without it |
|---|---|---|---|
| Covariance matrices | Required for likelihood-grade model comparison and penalty-aware fitting. | M0-M6 comparisons, uncertainty propagation, overfitting control. | Publication-grade likelihood validation. |
| Extraction-level data | Required to separate spatial/extraction effects from normalization effects. | M4 vs M6 distinguishability, leave-one-out stability. | Discrimination between detector/systematics and LSC-like structure. |
| Orientation/timestamp metadata | Required to test orientation/timing artifacts and anisotropy-related claims. | M4 timing/orientation competitor and transfer tests. | Any strong anisotropy inference. |
| Exposure-level data | Required for reproducible normalization and time-dependent checks. | Cross-experiment transfer and source-normalization tests. | Stable cross-dataset comparison. |
| Calibration/systematics datasets | Required to model detector/systematics competitors. | Full M4 implementation. | Distinguishing physical signal from instrument structure. |
| External constraint mappings | Required to check compatibility with other neutrino measurements and tensor bounds. | External veto policy. | Publication confidence. |

## BEST

Required:

- full covariance matrix or covariance construction protocol;
- extraction-level event counts, uncertainties, and correlations;
- source activity and calibration history;
- detector geometry metadata;
- timing and orientation metadata;
- background subtraction and extraction efficiency details.

Why it matters:

BEST is the central near-term comparison point for the LSC freeze. Without covariance and extraction-level detail, M4 and M6 remain underidentified.

Validation enabled:

- M0-M6 baseline comparison;
- M4 detector/systematics competitor implementation;
- LOO stability;
- sensitivity analysis.

Without it:

Only qualitative or non-validation-grade placeholder analysis is possible.

## GALLEX and SAGE

Required:

- run-level or extraction-level measurements;
- isotope/source details;
- covariance or uncertainty model documentation;
- detector geometry and calibration history;
- metadata sufficient for cross-experiment transfer tests.

Why it matters:

GALLEX/SAGE provide lineage and transfer tests. They help determine whether LSC-like structures are experiment-specific, isotope-specific, or systematics-driven.

Validation enabled:

- cross-experiment transfer protocol;
- isotope consistency checks;
- normalization/systematics comparison.

Without it:

LSC cannot claim stable transfer behavior across Gallium experiments.

## BEST-2

Required before unblinding:

- preregistered data format;
- covariance policy;
- frozen analysis hierarchy;
- extraction-level structure;
- orientation/timestamp metadata;
- calibration and background logs.

Why it matters:

BEST-2 is the intended future test environment for the frozen framework.

Validation enabled:

- anti-posthoc assessment;
- direct confrontation of frozen M0-M6 hierarchy;
- negative-result acceptance.

Without it:

BEST-2 cannot function as a disciplined freeze test.

## KATRIN

Requested:

- mappings from LSC-relevant parameter structures to KATRIN-sensitive observables where applicable;
- sterile-neutrino and endpoint constraint summaries;
- uncertainty and covariance documentation for relevant limits.

Why it matters:

KATRIN can act as an external veto or constraint for interpretations that overlap sterile-neutrino or spectrum-shape claims.

Without it:

External compatibility remains unresolved.

## IceCube

Requested:

- public constraint summaries relevant to anisotropy, sterile-neutrino, or high-energy neutrino propagation interpretations;
- detector/systematics caveats and covariance assumptions;
- mapping guidance for whether LSC claims are in scope.

Why it matters:

IceCube is not a primary LSC dataset but may constrain broad anisotropy or sterile-like interpretations if formal mapping exists.

Without it:

IceCube remains analogy/context only.

## Solar-Neutrino Constraints

Requested:

- solar-neutrino flux and oscillation constraint summaries;
- uncertainty budgets;
- correlation/covariance tables where available.

Why it matters:

Any LSC interpretation touching solar or low-energy neutrino consistency must not conflict with established solar-neutrino constraints.

Without it:

Solar compatibility cannot be asserted.

## SME/Lorentz-Style Constraint Literature

Requested:

- bounds relevant to anisotropy or tensor-like structures;
- mapping requirements;
- allowed coefficient spaces and uncertainty ranges.

Why it matters:

External tensor freedom concerns from audits require explicit veto checks.

Without it:

Tensor-like LSC language must remain constrained and non-claiming.

## Detector Calibration/Systematics Literature

Requested:

- calibration drift models;
- source normalization uncertainty models;
- extraction efficiency uncertainty;
- detector geometry uncertainty;
- background subtraction models;
- environmental drift data.

Why it matters:

These data define the M4 competitor. If M4 explains M6-level structures, LSC is not distinguishable.

