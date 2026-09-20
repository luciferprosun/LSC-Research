"""Frozen-before-evaluation methodology registries for Step 03."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from lsc_kernel.errors import DatasetContractError
from lsc_kernel.status import BlindnessLevel, DataExposureClassification, ValidationReadiness


@dataclass(frozen=True, slots=True)
class GalliumCrossSectionModel:
    model_id: str
    model_name: str
    year: int
    isotope: str
    ground_state_contribution: float | None
    excited_state_contribution: str
    total: float
    uncertainty_plus: float
    uncertainty_minus: float
    units: str
    covariance_availability: str
    source: str
    version: str
    status: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class GalliumCrossSectionModelRegistry:
    def __init__(self, models: Iterable[GalliumCrossSectionModel]) -> None:
        self.models = tuple(models)
        ids = [model.model_id for model in self.models]
        if len(ids) != len(set(ids)):
            raise DatasetContractError("Cross-section model IDs must be unique.")

    @classmethod
    def from_repository(cls, root: Path) -> "GalliumCrossSectionModelRegistry":
        path = root / "LSC_6_3_0_VALIDATION/05_GALLIUM_CROSS_SECTIONS/CROSS_SECTION_MODELS.csv"
        models = []
        with path.open(encoding="utf-8", newline="") as handle:
            for index, row in enumerate(csv.DictReader(handle), start=1):
                model_id = f"XS_{index:02d}_{row['model'].upper().replace(' ', '_').replace('-', '_')}_{row['source_isotope'].upper()}"
                ground_only = row["ground_state_only"].lower() == "true"
                models.append(
                    GalliumCrossSectionModel(
                        model_id=model_id,
                        model_name=row["model"],
                        year=int(row["year"]),
                        isotope=row["source_isotope"],
                        ground_state_contribution=(float(row["cross_section_1e_minus_45_cm2"]) if ground_only else None),
                        excited_state_contribution=(
                            "ZERO_BY_GROUND_STATE_ONLY_DEFINITION" if ground_only else row["excited_state_input"]
                        ),
                        total=float(row["cross_section_1e_minus_45_cm2"]),
                        uncertainty_plus=float(row["sigma_plus_1e_minus_45_cm2"]),
                        uncertainty_minus=float(row["sigma_minus_1e_minus_45_cm2"]),
                        units="1e-45 cm2",
                        covariance_availability="NOT_PUBLIC",
                        source=row["doi"] if row["doi"] != "NOT_PUBLIC" else row["local_source"],
                        version=str(row["year"]),
                        status=row["status"],
                    )
                )
        return cls(models)

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": "1.0.0",
            "default_model": None,
            "policy": "No cross-section model is declared correct or selected after observing a validation result.",
            "models": [model.as_dict() for model in self.models],
        }


@dataclass(frozen=True, slots=True)
class BaselineModelDefinition:
    model_id: str
    canonical_name: str
    hypothesis: str
    equations: tuple[str, ...]
    parameters: tuple[str, ...]
    free_parameters: tuple[str, ...]
    fixed_parameters: tuple[str, ...]
    fitting_allowed: bool
    training_data: str
    evaluation_data: str
    complexity_measure: tuple[str, ...]
    likelihood_requirements: tuple[str, ...]
    comparison_metrics: tuple[str, ...]
    provenance: str
    submodels: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def baseline_model_registry() -> dict[str, object]:
    models = (
        BaselineModelDefinition("M0", "null / published baseline", "Published no-transition expectation.",
            ("mu_i = mu_i,published",), (), (), ("published expectation",), False, "NONE", "held-out validation data",
            ("k=0",), ("dataset likelihood/covariance contract",), ("chi-square", "predictive log-likelihood", "residual diagnostics"),
            "FROZEN_PREDICTION_PROTOCOL.md model crosswalk"),
        BaselineModelDefinition("M1", "scalar normalization only", "One constant deficit shared over its declared scope.",
            ("mu_i = alpha * mu_i,published",), ("alpha",), ("alpha",), (), True, "preregistered calibration subset only",
            "preregistered hold-out only", ("k=1 per declared scope", "AIC", "BIC"), ("declared scope", "covariance scenario"),
            ("held-out predictive log-likelihood", "chi-square", "AIC", "BIC"), "FROZEN_PREDICTION_PROTOCOL.md model crosswalk"),
        BaselineModelDefinition("M2", "cross-section / source-systematics only", "Published cross-section/source alternatives explain rate shifts.",
            ("mu_i = mu_i,published(xs_model, source_nuisance)",), ("xs_model", "source_nuisance"), ("source_nuisance",),
            ("preregistered xs model choice/scan",), True, "calibration subset or published priors only", "held-out validation data",
            ("effective k declared per scenario", "AIC", "BIC"), ("cross-section registry", "shared nuclear treatment"),
            ("held-out predictive log-likelihood", "chi-square"), "FROZEN_PREDICTION_PROTOCOL.md model crosswalk"),
        BaselineModelDefinition("M3", "sterile-neutrino benchmark", "Standard 3+1 disappearance benchmark.",
            ("Pee(L,E)=1-sin^2(2theta_ee)*sin^2(1.267*Delta_m2*L/E)",), ("sin2_2theta_ee", "Delta_m2"),
            ("sin2_2theta_ee", "Delta_m2"), (), True, "preregistered calibration subset or external published surface",
            "held-out validation data", ("k=2 plus declared nuisance count", "AIC", "BIC"),
            ("baseline and energy integration", "dataset likelihood", "external confidence construction"),
            ("held-out predictive log-likelihood", "chi-square", "AIC", "BIC"), "FROZEN_PREDICTION_PROTOCOL.md model crosswalk"),
        BaselineModelDefinition("M4", "detector-systematics benchmark", "Detector/systematic shifts explain experiment variation.",
            ("mu_i = alpha_experiment * mu_i,published * detector_response_i",),
            ("experiment normalization", "detector nuisance", "hierarchical variance"),
            ("declared M4 submodel parameters",), (), True, "preregistered calibration subset only", "held-out validation data",
            ("exact nuisance/submodel count", "AIC", "BIC"), ("nuisance registry", "correlation scope", "dataset likelihood"),
            ("held-out predictive log-likelihood", "chi-square", "AIC", "BIC"), "FROZEN_PREDICTION_PROTOCOL.md model crosswalk",
            ("M_EXPERIMENT_NORMALIZATION", "M_DETECTOR_SYSTEMATIC", "M_HIERARCHICAL_EXPERIMENT")),
        BaselineModelDefinition("M5", "LSC trace-only", "Frozen LSC scalar/trace component.",
            ("Frozen E1-E12 subset as authenticated; no replacement equation.",), ("frozen LSC parameters",), (),
            ("all frozen LSC parameters",), False, "NONE", "held-out validation data only", ("frozen parameter count"),
            ("complete authentic frozen numerical bundle",), ("same preregistered metrics as baselines",),
            "FROZEN_PREDICTION_PROTOCOL.md model crosswalk; currently numerically blocked"),
        BaselineModelDefinition("M6", "LSC trace + traceless anisotropy", "Full frozen LSC 6.3.0 model.",
            ("Frozen E1-E12 as authenticated; no replacement equation.",), ("frozen LSC parameters and active tensor",), (),
            ("all frozen LSC parameters",), False, "NONE", "held-out validation data only", ("frozen parameter count"),
            ("complete authentic numerical bundle", "frames", "orientation", "timing for directional use"),
            ("same preregistered metrics as baselines",), "FROZEN_PREDICTION_PROTOCOL.md model crosswalk; currently numerically blocked"),
    )
    return {
        "schema_version": "1.0.0",
        "historical_models": [model.as_dict() for model in models],
        "aliases": {
            "M_NULL": "M0",
            "M_CONSTANT_DEFICIT": "M1",
            "M_CROSS_SECTION_VARIANT": "M2",
            "M_STERILE_3P1": "M3",
            "M_DETECTOR_SYSTEMATIC": "M4/M_DETECTOR_SYSTEMATIC",
            "M_EXPERIMENT_NORMALIZATION": "M4/M_EXPERIMENT_NORMALIZATION",
            "M_HIERARCHICAL_EXPERIMENT": "M4/M_HIERARCHICAL_EXPERIMENT",
        },
        "frozen_lsc_models_are_not_baseline_fit_targets": ["M5", "M6"],
    }


@dataclass(frozen=True, slots=True)
class ValidationTestDefinition:
    test_id: str
    canonical_name: str
    scientific_question: str
    hypothesis: str
    dataset_inputs: tuple[str, ...]
    train_calibration_subset: str
    holdout_subset: str
    prediction_target: str
    observable: str
    test_statistic: tuple[str, ...]
    baseline_models: tuple[str, ...]
    nuisance_treatment: tuple[str, ...]
    covariance_requirement: tuple[str, ...]
    cross_section_treatment: str
    timing_requirement: str
    geometry_requirement: str
    orientation_requirement: str
    readiness: ValidationReadiness
    blockers: tuple[str, ...]
    pass_criterion: str
    falsification_criterion: str
    reporting_requirements: tuple[str, ...]
    exposure_classification: DataExposureClassification
    blindness_level: BlindnessLevel
    specification_gaps: tuple[str, ...] = ()

    @property
    def executable(self) -> bool:
        return False  # Step 03 authorizes planning, never numerical LSC execution.

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["readiness"] = self.readiness.value
        result["exposure_classification"] = self.exposure_classification.value
        result["blindness_level"] = self.blindness_level.value
        result["prediction_authorized"] = False
        result["numerical_validation_authorized"] = False
        return result


def validation_test_registry() -> tuple[ValidationTestDefinition, ...]:
    common_blockers = ("MISSING_AUTHENTIC_FROZEN_NUMERICAL_BUNDLE",)
    common_reports = ("all preregistered splits", "all baseline metrics", "adverse/null outcomes", "exact provenance", "blockers")
    exposed = DataExposureClassification.MODEL_EXPOSED
    historical = BlindnessLevel.NON_BLIND_HISTORICAL
    tests = (
        ValidationTestDefinition("T1", "BEST inner to outer zone transfer", "Does an inner-derived frozen specification predict the outer zone without refit?",
            "A frozen model with genuine spatial structure should transfer from inner calibration to outer observations.", ("BEST",),
            "SPLIT_BEST_INNER_TO_OUTER: inner zone", "SPLIT_BEST_INNER_TO_OUTER: outer zone", "outer-zone rates by matched exposure",
            "production_rate or preregistered ratio", ("predictive log-likelihood", "chi-square", "residual diagnostics"),
            ("M0", "M1", "M3", "M4"), ("profile only preregistered nuisance parameters",),
            ("COV_COLLABORATION preferred", "all declared sensitivity scenarios otherwise"), "scan registered models; none selected post-result",
            "exposure-integrated timing only", "published two-zone average-path geometry", "not required for scalar test",
            ValidationReadiness.PARTIAL, common_blockers + ("BEST_JOINT_COVARIANCE_NOT_PUBLIC",),
            "PASS at test level only if frozen LSC held-out performance is better than every declared simpler baseline under the primary covariance source and does not reverse across credible sensitivity scenarios; no discovery claim.",
            "FAIL at test level if any equally/less complex declared baseline matches or improves held-out performance, or transfer residuals violate the preregistered calibration rule.", common_reports, exposed, historical),
        ValidationTestDefinition("T2", "BEST outer to inner zone transfer", "Is reverse zone transfer mathematically identified and predictive without refit?",
            "If the frozen mapping is identifiable from outer data, it should transfer to inner observations.", ("BEST",),
            "SPLIT_BEST_OUTER_TO_INNER: outer zone", "SPLIT_BEST_OUTER_TO_INNER: inner zone", "inner-zone rates by matched exposure",
            "production_rate or preregistered ratio", ("predictive log-likelihood", "chi-square", "residual diagnostics"),
            ("M0", "M1", "M3", "M4"), ("profile only preregistered nuisance parameters",),
            ("COV_COLLABORATION preferred", "all declared sensitivity scenarios otherwise"), "same registry fixed before evaluation",
            "exposure-integrated timing only", "published two-zone average-path geometry", "not required for scalar test",
            ValidationReadiness.PARTIAL, common_blockers + ("BEST_REVERSE_MAPPING_IDENTIFIABILITY_UNRESOLVED", "BEST_JOINT_COVARIANCE_NOT_PUBLIC"),
            "Same model-comparison rule as T1, conditional on a preregistered proof that reverse mapping is identified.",
            "FAIL if reverse mapping is identified and frozen transfer is no better than a simpler baseline; otherwise report BLOCKED, never PASS.", common_reports, exposed, historical),
        ValidationTestDefinition("T3", "BEST to GALLEX/SAGE transfer", "Does the frozen BEST specification transfer across independent gallium experiments without refit?",
            "Frozen LSC structure should predict GALLEX and both SAGE isotope datasets without changing LSC parameters.",
            ("BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"), "SPLIT_BEST_TO_GALLEX and SPLIT_BEST_TO_SAGE: BEST",
            "GALLEX Cr, SAGE 51Cr and SAGE 37Ar source observations", "cross-experiment rate/ratio", "published source rate/ratio",
            ("predictive log-likelihood", "chi-square", "leave-one-experiment-out score"), ("M0", "M1", "M2", "M3", "M4"),
            ("experiment normalization may be fitted only inside M4 baseline", "frozen LSC parameters never profiled"),
            ("COV_COLLABORATION preferred", "sensitivity scenarios reported separately"), "all registered models and shared-isotope treatment",
            "exact source time needed only for temporal variants", "experiment-published scalar geometry", "not required for scalar transfer",
            ValidationReadiness.PARTIAL, common_blockers + ("FROZEN_CROSS_EXPERIMENT_MAPPING_MISSING", "FULL_COVARIANCE_NOT_PUBLIC"),
            "PASS only if all specified hold-out experiment groups outperform declared simpler baselines under the frozen comparison rule.",
            "Component-level failure if transfer fails for a preregistered experiment/isotope or a simpler baseline matches/improves held-out score.", common_reports, exposed, historical),
        ValidationTestDefinition("T4", "GALLEX/SAGE to BEST transfer", "Does a non-BEST calibration transfer to BEST without refit?",
            "A cross-experiment frozen mapping should predict both BEST zones from GALLEX/SAGE calibration.",
            ("GALLEX_GNO", "SAGE_CR51", "SAGE_AR37", "BEST"), "SPLIT_GALLIUM_LEGACY_TO_BEST: GALLEX/SAGE",
            "SPLIT_GALLIUM_LEGACY_TO_BEST: BEST", "BEST inner and outer rates", "production rate or ratio",
            ("predictive log-likelihood", "chi-square"), ("M0", "M1", "M2", "M3", "M4"),
            ("baseline/nuisance fitting confined to calibration subset",), ("same declared scenario for calibration and hold-out",),
            "registered and frozen before evaluation", "scalar exposure timing", "published scalar geometry", "not required",
            ValidationReadiness.PARTIAL, common_blockers + ("FROZEN_CROSS_EXPERIMENT_MAPPING_MISSING", "FULL_COVARIANCE_NOT_PUBLIC"),
            "PASS only if both BEST zones satisfy the preregistered held-out comparison against simpler baselines.",
            "FAIL if transfer does not generalize to either preregistered BEST zone or a simpler baseline is equal/better.", common_reports, exposed, historical),
        ValidationTestDefinition("T5", "51Cr to 37Ar cross-isotope transfer", "Does frozen energy/isotope dependence transfer without refit?",
            "A frozen energy dependence should transfer from 51Cr datasets to SAGE 37Ar.",
            ("BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37", "GALLIUM_CROSS_SECTIONS"),
            "SPLIT_CR51_TO_AR37: all eligible 51Cr observations", "SPLIT_CR51_TO_AR37: SAGE 37Ar", "37Ar production rate/ratio",
            "isotope-specific production rate/ratio", ("predictive log-likelihood", "chi-square", "cross-section scenario stability"),
            ("M0", "M1", "M2", "M3", "M4"), ("shared nuclear nuisance explicitly represented",),
            ("cross-isotope covariance required for inference", "assumption scenarios sensitivity-only"), "all registered 51Cr/37Ar pairs; no default correct model",
            "not required for scalar transfer", "published experiment geometry", "not required",
            ValidationReadiness.SENSITIVITY_ONLY, common_blockers + ("FROZEN_ENERGY_MAPPING_MISSING", "CROSS_ISOTOPE_COVARIANCE_NOT_PUBLIC"),
            "No inferential PASS is authorized under assumption-only covariance; report stability or reversal across the full preregistered scan.",
            "Component-level falsification if a future collaboration-covariance run shows preregistered frozen isotope transfer is no better than simpler baselines.", common_reports, exposed, historical),
        ValidationTestDefinition("T6", "Leave-one-run-out", "Are predictions stable for every omitted source exposure?",
            "A frozen model should predict every omitted run without refitting its parameters.", ("BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"),
            "SPLIT_LORO_*: all but one eligible primary exposure", "each omitted primary exposure in deterministic source order", "omitted-run rate/ratio",
            "production rate/ratio", ("aggregate predictive log-likelihood", "per-run standardized residual", "influence diagnostics"),
            ("M0", "M1", "M2", "M3", "M4"), ("baseline/nuisance fitting inside each training fold only",),
            ("COV_COLLABORATION needed for inference", "diagonal/plausible scans sensitivity-only"), "registered before folds",
            "source interval sufficient for scalar LORO", "not required beyond scalar contract", "not required",
            ValidationReadiness.PARTIAL, common_blockers + ("RUN_COVARIANCE_NOT_PUBLIC",),
            "PASS only if every fold is disclosed and aggregate held-out performance beats declared simpler baselines under an inferentially valid covariance.",
            "FAIL if preregistered aggregate or influence criterion fails, or any omitted split is hidden.", common_reports + ("per-fold result",), exposed, historical),
        ValidationTestDefinition("T7", "Leave-one-experiment-out", "Does the frozen model generalize across experiment families?",
            "A frozen model should predict each held-out experiment family without parameter refit.",
            ("BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"), "SPLIT_LOEO_*: all non-held-out experiment families",
            "each experiment-family hold-out", "experiment-level combined rate/ratio", "combined source rate/ratio",
            ("aggregate predictive log-likelihood", "held-out chi-square", "residual diagnostics"), ("M0", "M1", "M2", "M3", "M4"),
            ("baseline/nuisance fitting inside training families only",), ("cross-experiment covariance or declared sensitivity policy",),
            "same registry over all folds", "scalar only", "published scalar geometry", "not required",
            ValidationReadiness.PARTIAL, common_blockers + ("CROSS_EXPERIMENT_COVARIANCE_INCOMPLETE",),
            "PASS only if every declared family hold-out is reported and frozen LSC is better than simpler baselines under the preregistered rule.",
            "FAIL if any preregistered family transfer fails or a simpler baseline is equal/better overall.", common_reports + ("per-family result",), exposed, historical),
        ValidationTestDefinition("T8", "Gallium cross-section sensitivity", "Are conclusions robust to published capture cross-section alternatives?",
            "A defensible result should not depend on post-result selection of one cross-section model.",
            ("GALLIUM_CROSS_SECTIONS", "BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"), "NONE", "all eligible scalar observations",
            "model-comparison stability across registered cross-section alternatives", "rates/ratios and model-comparison deltas",
            ("scenario spread", "rank stability", "predictive score"), ("M0", "M1", "M2", "M3", "M4"),
            ("shared nuclear nuisance per declared covariance scenario",), ("COV_PLAUSIBLE_SCAN", "COV_COLLABORATION if acquired"),
            "all registry entries; none declared correct", "not required", "not required", "not required",
            ValidationReadiness.SENSITIVITY_ONLY, common_blockers + ("CROSS_ISOTOPE_COVARIANCE_NOT_PUBLIC",),
            "SENSITIVITY_ONLY: report whether ordering/conclusion is stable; no discovery/exclusion/sigma/decisive language.",
            "Model support is weakened if its advantage disappears across credible registered alternatives.", common_reports + ("every cross-section alternative",), exposed, historical),
        ValidationTestDefinition("T9", "Systematics perturbation sensitivity", "Are comparisons robust to preregistered nuisance/correlation scenarios?",
            "A credible advantage should survive reasonable predeclared systematic treatments.",
            ("BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"), "NONE", "all eligible scalar observations",
            "model-comparison stability", "rates/ratios", ("scenario spread", "rank stability", "predictive score"),
            ("M0", "M1", "M2", "M3", "M4"), ("all nuisance registry categories applicable to each dataset",),
            ("COV_DIAGONAL", "COV_UNCORRELATED_SYSTEMATICS", "COV_FULLY_COMMON_SELECTED", "COV_PLAUSIBLE_SCAN"),
            "registered alternatives only", "not required", "not required", "not required",
            ValidationReadiness.SENSITIVITY_ONLY, common_blockers + ("COLLABORATION_COVARIANCE_NOT_PUBLIC",),
            "SENSITIVITY_ONLY: report complete scenario envelope without inferential significance language.",
            "Model support is weakened if advantage disappears across credible scenarios or requires one post-selected assumption.", common_reports + ("every covariance/nuisance scenario",), exposed, historical),
        ValidationTestDefinition("T10", "Sterile 3+1 baseline versus frozen LSC", "Does frozen LSC predict better than the standard sterile benchmark?",
            "Frozen LSC must outperform M3 out of sample after declared complexity treatment to claim an advantage.",
            ("BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37", "KATRIN", "ICECUBE", "DAYA_BAY", "PROSPECT", "STEREO", "MICROBOONE"),
            "preregistered gallium calibration split for M3 only", "preregistered gallium hold-outs", "held-out gallium rates plus separately mapped external constraints",
            "rates/ratios; external native observables after mapping", ("predictive log-likelihood", "chi-square", "AIC", "BIC"),
            ("M3", "M0", "M1", "M2", "M4"), ("M3 and baseline parameters only; frozen LSC never fit",),
            ("dataset-native covariance", "assumption sensitivity kept separate"), "registered gallium models",
            "scalar test does not require precise timing", "baseline/energy integration required", "not required for scalar comparison",
            ValidationReadiness.PARTIAL, common_blockers + ("STERILE_GEOMETRY_INTEGRATION_INCOMPLETE", "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING"),
            "PASS only if frozen LSC improves held-out prediction after declared complexity treatment and no valid mapped external constraint excludes its required region.",
            "Component/model support fails if M3 or a simpler baseline is equal/better, or a valid preregistered external mapping excludes the required region.", common_reports + ("external releases reported separately",), exposed, historical),
        ValidationTestDefinition("T11", "Null/baseline comparison versus frozen LSC", "Does frozen LSC add out-of-sample predictive value beyond simpler explanations?",
            "Frozen LSC must outperform M0/M1/M2/M4 without parameter refit.",
            ("BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"), "preregistered split-specific calibration for baselines only",
            "all preregistered hold-outs", "held-out rates/ratios", "rates/ratios", ("predictive log-likelihood", "chi-square", "AIC", "BIC", "residual diagnostics"),
            ("M0", "M1", "M2", "M4"), ("baseline/nuisance fitting only; frozen LSC never fit",),
            ("dataset-native preferred", "all sensitivity scenarios disclosed"), "registry fixed before evaluation",
            "not required for scalar comparison", "published scalar geometry", "not required",
            ValidationReadiness.PARTIAL, common_blockers + ("FULL_COVARIANCE_NOT_PUBLIC",),
            "PASS only at test level if frozen LSC strictly improves held-out prediction over every declared simpler baseline after complexity treatment.",
            "Model support fails if any simpler baseline is equal or better on preregistered held-out performance.", common_reports, exposed, historical),
        ValidationTestDefinition("T12", "Directional and sidereal test", "Can the frozen directional/tensor component predict time/orientation dependence?",
            "A complete authentic tensor and frame mapping must yield a preregistered directional/sidereal prediction.",
            ("BEST",), "UNAUTHORIZED", "UNAUTHORIZED", "direction/time-resolved rate modulation", "time- and frame-resolved observable",
            ("SPECIFICATION_INCOMPLETE",), ("M0", "M1", "M4", "M6"), ("UNAUTHORIZED",), ("adequate directional likelihood/covariance",),
            "frozen before access", "precise event/sub-run timing; exposure midpoint explicitly forbidden", "sufficient surveyed Earth-fixed detector/source geometry",
            "surveyed detector/source orientation plus complete active tensor and frame transforms",
            ValidationReadiness.BLOCKED,
            common_blockers + ("PRECISE_TIMING_MISSING", "SURVEYED_ORIENTATION_MISSING", "SUFFICIENT_GEOMETRY_MISSING", "ACTIVE_TENSOR_MISSING", "FRAME_TRANSFORMS_MISSING", "REQUIRED_UNITS_MISSING"),
            "No PASS criterion is executable until the historical scientific statistic and all directional inputs are frozen.",
            "Future component-level falsification follows only a preregistered adequately powered directional test; current absence of data is not a pass or fail.",
            common_reports + ("BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT",), exposed, historical,
            ("PASS/FAIL statistic and power criterion remain SPECIFICATION_INCOMPLETE.",)),
    )
    if [test.test_id for test in tests] != [f"T{i}" for i in range(1, 13)]:
        raise AssertionError("T1-T12 registry identity/order changed")
    return tests


def covariance_scenario_registry() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "policy": "Assumption-based covariance results are SENSITIVITY_ONLY and cannot support discovery/exclusion/sigma/decisive claims.",
        "scenarios": [
            {"scenario_id": "COV_DIAGONAL", "assumptions": ["Only explicitly available marginal variances; off-diagonal entries zero."], "allowed_use": "diagnostic sensitivity", "forbidden_claims": ["discovery", "exclusion", "sigma evidence", "decisive preference", "collaboration covariance"], "test_compatibility": [f"T{i}" for i in range(1, 12)], "provenance_status": "ASSUMPTION_BASED_SENSITIVITY_ONLY", "available": True},
            {"scenario_id": "COV_UNCORRELATED_SYSTEMATICS", "assumptions": ["Published systematic components treated independent across observations unless explicitly common."], "allowed_use": "bounded sensitivity only", "forbidden_claims": ["discovery", "exclusion", "sigma evidence", "decisive preference", "published correlation"], "test_compatibility": [f"T{i}" for i in range(1, 12)], "provenance_status": "ASSUMPTION_BASED_SENSITIVITY_ONLY", "available": True},
            {"scenario_id": "COV_FULLY_COMMON_SELECTED", "assumptions": ["Only named selected shared nuisances are 100% correlated over their preregistered scope."], "allowed_use": "bounded sensitivity where covariance remains valid/nonsingular", "forbidden_claims": ["discovery", "exclusion", "sigma evidence", "decisive preference", "all systematics common"], "test_compatibility": [f"T{i}" for i in range(1, 12)], "provenance_status": "ASSUMPTION_BASED_SENSITIVITY_ONLY", "available": True},
            {"scenario_id": "COV_PLAUSIBLE_SCAN", "assumptions": ["Correlation coefficients scanned over a predeclared grid/range; range is never chosen after results."], "allowed_use": "robustness envelope only", "forbidden_claims": ["discovery", "exclusion", "sigma evidence", "decisive preference", "data-estimated covariance"], "test_compatibility": [f"T{i}" for i in range(1, 12)], "provenance_status": "ASSUMPTION_BASED_SENSITIVITY_ONLY", "available": True},
            {"scenario_id": "COV_COLLABORATION", "assumptions": ["Exact authenticated collaboration covariance/likelihood object and nuisance definition required."], "allowed_use": "inference only after source acquisition, hash verification and contract validation", "forbidden_claims": ["availability before authenticated source"], "test_compatibility": [f"T{i}" for i in range(1, 13)], "provenance_status": "MISSING_AUTHENTIC_SOURCE", "available": False},
        ],
    }


def nuisance_parameter_registry() -> dict[str, object]:
    rows = (
        ("NUIS_SOURCE_ACTIVITY", "source activity", "run/source campaign", "source experiment", True, True, False, False, "NO_COMPLETE_MATRIX", ("fixed published", "profile with published prior", "covariance sensitivity")),
        ("NUIS_EXTRACTION_EFFICIENCY", "extraction efficiency", "run/extraction", "gallium", False, True, False, False, "NO_COMPLETE_MATRIX", ("profile with published uncertainty", "sensitivity")),
        ("NUIS_COUNTING_EFFICIENCY", "counting efficiency", "counter/run", "gallium", False, False, False, False, "NO_COMPLETE_MATRIX", ("profile with published uncertainty", "sensitivity")),
        ("NUIS_BACKGROUND_RADON", "background/radon", "counter/run", "gallium", False, False, False, False, "NO_COMPLETE_MATRIX", ("dataset-native likelihood only", "sensitivity")),
        ("NUIS_GEOMETRY", "geometry", "zone/detector", "all", True, True, False, False, "PARTIAL", ("fixed published geometry", "source-defined nuisance")),
        ("NUIS_DETECTOR_EFFICIENCY", "detector efficiency", "detector/run", "all", False, True, False, False, "DATASET_SPECIFIC", ("dataset-native treatment",)),
        ("NUIS_GA_CAPTURE_XS", "gallium capture cross section", "isotope/model", "gallium", True, True, True, True, "JOINT_MATRIX_NOT_PUBLIC", ("registered model scan", "shared nuisance sensitivity")),
        ("NUIS_ISOTOPE_TRANSITION", "isotope transition uncertainty", "isotope/model", "gallium", True, True, True, True, "JOINT_MATRIX_NOT_PUBLIC", ("registered model scan", "shared nuisance sensitivity")),
        ("NUIS_EXPERIMENT_NORMALIZATION", "experiment normalization", "experiment", "all", True, True, False, False, "MODEL_DEPENDENT", ("M4 fit in training subset only", "hierarchical baseline")),
        ("NUIS_SHARED_NUCLEAR", "shared nuclear uncertainty", "cross-isotope", "gallium", True, True, True, True, "NOT_PUBLIC", ("COV_FULLY_COMMON_SELECTED", "COV_PLAUSIBLE_SCAN", "COV_COLLABORATION")),
    )
    keys = ("nuisance_id", "category", "scope", "experiment", "correlated_across_runs", "correlated_across_zones", "correlated_across_experiments", "correlated_across_isotopes", "published_covariance", "treatment_scenarios")
    return {"schema_version": "1.0.0", "nuisances": [dict(zip(keys, row, strict=True)) for row in rows]}


def split_registry() -> dict[str, object]:
    historical = BlindnessLevel.NON_BLIND_HISTORICAL.value
    exposed = DataExposureClassification.MODEL_EXPOSED.value
    splits = [
        ("SPLIT_BEST_INNER_TO_OUTER", ["BEST:zone=inner"], ["BEST:zone=outer"], "T1"),
        ("SPLIT_BEST_OUTER_TO_INNER", ["BEST:zone=outer"], ["BEST:zone=inner"], "T2"),
        ("SPLIT_BEST_EARLY_TO_LATE", ["BEST:exposure_id=1..5"], ["BEST:exposure_id=6..10"], "T6"),
        ("SPLIT_BEST_LORO", ["BEST:all eligible primary rows except stable omitted run"], ["BEST:one omitted run"], "T6"),
        ("SPLIT_GALLEX_LORO", ["GALLEX_GNO:all eligible Cr source rows except stable omitted run"], ["GALLEX_GNO:one omitted Cr source run"], "T6"),
        ("SPLIT_SAGE_CR51_LORO", ["SAGE_CR51:all primary exposures except stable omitted run"], ["SAGE_CR51:one omitted primary run"], "T6"),
        ("SPLIT_SAGE_AR37_LORO", ["SAGE_AR37:all primary exposures except stable omitted run"], ["SAGE_AR37:one omitted primary run"], "T6"),
        ("SPLIT_LOEO_BEST", ["GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"], ["BEST"], "T7"),
        ("SPLIT_LOEO_GALLEX", ["BEST", "SAGE_CR51", "SAGE_AR37"], ["GALLEX_GNO"], "T7"),
        ("SPLIT_LOEO_SAGE_CR51", ["BEST", "GALLEX_GNO", "SAGE_AR37"], ["SAGE_CR51"], "T7"),
        ("SPLIT_LOEO_SAGE_AR37", ["BEST", "GALLEX_GNO", "SAGE_CR51"], ["SAGE_AR37"], "T7"),
        ("SPLIT_BEST_TO_GALLEX", ["BEST"], ["GALLEX_GNO:Cr source rows"], "T3"),
        ("SPLIT_BEST_TO_SAGE", ["BEST"], ["SAGE_CR51", "SAGE_AR37"], "T3"),
        ("SPLIT_GALLIUM_LEGACY_TO_BEST", ["GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"], ["BEST"], "T4"),
        ("SPLIT_CR51_TO_AR37", ["BEST", "GALLEX_GNO:Cr source rows", "SAGE_CR51"], ["SAGE_AR37"], "T5"),
        ("SPLIT_EXPERIMENT_FAMILY_HOLDOUT", ["all non-held-out registered gallium families"], ["one stable experiment family"], "T7"),
    ]
    return {
        "schema_version": "1.0.0",
        "selection_policy": "Split membership is stable, identifier-driven and frozen before outcomes; no result-adaptive split changes.",
        "splits": [
            {"split_id": split_id, "train": train, "holdout": holdout, "test_id": test_id,
             "ordering": "lexicographic canonical dataset/run ID", "exposure_classification": exposed,
             "blindness_level": historical, "holdout_is_clean_unexposed": False}
            for split_id, train, holdout, test_id in splits
        ],
    }


def metric_registry() -> dict[str, object]:
    rows = (
        ("CHI_SQUARE", "covariance or declared diagonal sensitivity", ("Gaussian residual interpretation limits apply",)),
        ("DELTA_CHI_SQUARE", "nested/comparable models and documented reference", ("not a confidence level without coverage construction",)),
        ("LIKELIHOOD_RATIO", "explicit likelihood plus nesting/regularity or calibrated null distribution", ("do not invoke Wilks automatically",)),
        ("PREDICTIVE_LOG_LIKELIHOOD", "held-out predictive distribution", ("primary out-of-sample comparison metric",)),
        ("RESIDUAL_DIAGNOSTICS", "defined residual/covariance transform", ("diagnostic, not standalone evidence",)),
        ("AIC", "valid likelihood and effective parameter count", ("in-sample information criterion",)),
        ("BIC", "valid likelihood, effective parameter count and sample-size definition", ("asymptotic approximation",)),
        ("CROSS_VALIDATION_SCORE", "predeclared folds and fold-local fitting", ("all folds reported",)),
        ("PREDICTIVE_CALIBRATION", "probabilistic prediction and calibration definition", ("requires adequate sample size",)),
        ("POSTERIOR_PREDICTIVE", "complete Bayesian generative model and frozen priors", ("unavailable without a valid Bayesian model",)),
    )
    return {"schema_version": "1.0.0", "metrics": [
        {"metric_id": item, "prerequisites": prerequisites, "applicable_models": ["M0", "M1", "M2", "M3", "M4", "M5", "M6"],
         "applicable_datasets": "contract-dependent", "assumptions": list(limits), "interpretation_limits": list(limits)}
        for item, prerequisites, limits in rows
    ]}


def falsification_registry() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "levels": ["test-level falsification", "component-level falsification", "model-level falsification"],
        "rules": [
            {"rule_id": "FALSIFY_OUT_OF_SAMPLE", "level": "test-level falsification", "condition": "Frozen out-of-sample prediction fails its preregistered test rule.", "scope": "the failed test unless an escalation rule is separately preregistered"},
            {"rule_id": "FALSIFY_COVARIANCE_FRAGILITY", "level": "component-level falsification", "condition": "Apparent advantage disappears across credible preregistered nuisance/covariance scenarios.", "scope": "the affected model component/claim"},
            {"rule_id": "FALSIFY_SIMPLER_BASELINE", "level": "model-level falsification", "condition": "An equally or less complex baseline predicts held-out data equally well or better under the frozen comparison rule.", "scope": "claimed LSC predictive advantage"},
            {"rule_id": "FALSIFY_EXTERNAL_MAPPING", "level": "component-level falsification", "condition": "A valid preregistered quantitative mapping shows an external constraint excludes the required region.", "scope": "mapped parameter/component only"},
            {"rule_id": "FALSIFY_TRANSFER", "level": "component-level falsification", "condition": "Required preregistered isotope or experiment transfer fails without refit.", "scope": "transfer/generalization component"},
            {"rule_id": "FALSIFY_DIRECTIONAL_FUTURE", "level": "component-level falsification", "condition": "Claimed directional effect fails an adequately powered future test with timing, surveyed orientation, frames and active tensor.", "scope": "directional/traceless component"},
        ],
        "aggregation_policy": "No single failure automatically becomes global model falsification unless an explicit preregistered escalation rule says so.",
    }


def multiple_testing_policy() -> dict[str, object]:
    # Imported lazily to avoid making Step 03 registry construction depend on
    # statistical engine import order.
    from lsc_kernel.statistics.multiple_testing import adjudicated_multiple_testing_policy

    return adjudicated_multiple_testing_policy()
