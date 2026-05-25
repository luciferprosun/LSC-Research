# LSC M4 Implementation Schema

Status: Step 3 implementation artifact  
Purpose: detector/systematics competitor schema  

## 1. Core Rule

M4 is the full detector/systematics competitor. It must be implemented before M6 preference can be claimed.

## 2. Machine-Readable Top-Level Structure

```yaml
model_id: M4
model_name: detector_systematics_baseline
validation_grade: NON-VALIDATION-GRADE until covariance and metadata are complete
components:
  calibration_drift: {}
  source_normalization_uncertainty: {}
  detector_geometry_asymmetry: {}
  extraction_efficiency_asymmetry: {}
  environmental_background_drift: {}
  covariance_incompleteness: {}
  timing_artifacts: {}
  orientation_artifacts: {}
  background_subtraction_uncertainty: {}
outputs:
  predicted_ratios: []
  nuisance_parameters: []
  covariance_assumptions: []
  comparison_scores: []
```

This is an implementation schema, not a new physics model.

## 3. Component Schemas

### Calibration Drift

```yaml
calibration_drift:
  status: placeholder
  inputs_required:
    - calibration_run_id
    - timestamp
    - calibration_value
    - uncertainty
  sensitivity_hooks:
    - drift_amplitude_scan
    - time_split_test
```

### Source Normalization Uncertainty

```yaml
source_normalization_uncertainty:
  status: placeholder
  inputs_required:
    - source_activity
    - source_activity_uncertainty
    - calibration_method
    - isotope
  sensitivity_hooks:
    - source_scale_scan
    - isotope_split_test
```

### Detector Geometry Asymmetry

```yaml
detector_geometry_asymmetry:
  status: placeholder
  inputs_required:
    - detector_geometry_file
    - source_position
    - zone_boundaries
    - dead_volume_map
  sensitivity_hooks:
    - geometry_perturbation_scan
    - source_position_shift_test
```

### Extraction Efficiency Asymmetry

```yaml
extraction_efficiency_asymmetry:
  status: placeholder
  inputs_required:
    - extraction_id
    - zone_id
    - efficiency
    - efficiency_uncertainty
  sensitivity_hooks:
    - zone_efficiency_scan
    - run_by_run_efficiency_test
```

### Environmental Background Drift

```yaml
environmental_background_drift:
  status: placeholder
  inputs_required:
    - timestamp
    - temperature
    - pressure
    - radon_level
    - electronics_state
  sensitivity_hooks:
    - environmental_regression
    - day_night_split
    - seasonal_split
```

### Covariance Incompleteness

```yaml
covariance_incompleteness:
  status: placeholder
  inputs_required:
    - covariance_matrix
    - covariance_source
    - missing_correlation_policy
  sensitivity_hooks:
    - diagonal_vs_correlated_comparison
    - conservative_correlation_envelope
```

### Timing Artifacts

```yaml
timing_artifacts:
  status: placeholder
  inputs_required:
    - exposure_start
    - exposure_end
    - extraction_time
    - counting_time
  sensitivity_hooks:
    - time_scramble
    - exposure_phase_split
```

### Orientation Artifacts

```yaml
orientation_artifacts:
  status: placeholder
  inputs_required:
    - detector_azimuth
    - detector_tilt
    - latitude
    - longitude
    - source_orientation
  sensitivity_hooks:
    - lab_frame_vs_celestial_frame_test
    - orientation_scramble
```

### Background Subtraction Uncertainty

```yaml
background_subtraction_uncertainty:
  status: placeholder
  inputs_required:
    - background_rate
    - background_uncertainty
    - background_model
    - background_run_id
  sensitivity_hooks:
    - background_scale_scan
    - background_only_validation
```

## 4. Required M4 Report Fields

Each M4 execution must output:

- included components;
- missing components;
- nuisance parameter count;
- covariance assumption;
- fit score;
- penalty-adjusted score;
- comparison vs M5/M6;
- whether M4 reproduces M6-level structures.

