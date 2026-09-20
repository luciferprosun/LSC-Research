"""Immutable validation-dataset contracts backed by the preserved archive."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import json
from pathlib import Path, PurePosixPath
from typing import Iterable

from lsc_kernel.errors import DatasetContractError
from lsc_kernel.io.hashes import sha256_file
from lsc_kernel.status import BlindnessLevel, DataExposureClassification


@dataclass(frozen=True, slots=True)
class DatasetContract:
    dataset_id: str
    schema_version: str
    raw_source_identity: str
    allowed_rows: tuple[str, ...]
    exclusions: tuple[str, ...]
    transformations: tuple[str, ...]
    units: tuple[tuple[str, str], ...]
    missing_value_policy: str
    derived_field_policy: str
    uncertainty_fields: tuple[str, ...]
    covariance_fields: tuple[str, ...]
    timing_fields: tuple[str, ...]
    geometry_fields: tuple[str, ...]
    provenance_fields: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["units"] = {key: value for key, value in self.units}
        return result


@dataclass(frozen=True, slots=True)
class ValidationDatasetRecord:
    dataset_id: str
    experiment: str
    source_dois: tuple[str, ...]
    source_reference: str
    local_path: str
    sha256: str
    version: str
    quality_grade: str
    raw_or_derived: str
    number_of_objects: int
    count_semantics: str
    available_observables: tuple[str, ...]
    uncertainties: tuple[str, ...]
    covariance_availability: str
    timing_resolution: str
    geometry_availability: str
    orientation_availability: str
    validation_role: str
    allowed_tests: tuple[str, ...]
    prohibited_tests: tuple[str, ...]
    known_limitations: tuple[str, ...]
    provenance_status: str
    exposure_classification: DataExposureClassification
    blindness_level: BlindnessLevel
    contract: DatasetContract

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["source_dois"] = list(self.source_dois)
        result["available_observables"] = list(self.available_observables)
        result["uncertainties"] = list(self.uncertainties)
        result["allowed_tests"] = list(self.allowed_tests)
        result["prohibited_tests"] = list(self.prohibited_tests)
        result["known_limitations"] = list(self.known_limitations)
        result["exposure_classification"] = self.exposure_classification.value
        result["blindness_level"] = self.blindness_level.value
        result["contract"] = self.contract.as_dict()
        return result


class ValidationDatasetRegistry:
    """The sole in-code registry used to emit and validate dataset manifests."""

    def __init__(self, records: Iterable[ValidationDatasetRecord]) -> None:
        self._records = tuple(records)
        ids = [record.dataset_id for record in self._records]
        if len(ids) != len(set(ids)):
            raise DatasetContractError("Dataset IDs must be unique.", details={"dataset_ids": ids})
        for record in self._records:
            self._validate_record(record)

    @staticmethod
    def _validate_record(record: ValidationDatasetRecord) -> None:
        if record.quality_grade not in {"A", "B", "C", "D", "E"}:
            raise DatasetContractError("Dataset quality grade must be A-E.")
        path = PurePosixPath(record.local_path)
        if path.is_absolute() or ".." in path.parts:
            raise DatasetContractError(
                "Dataset paths must be repository-relative.", details={"dataset_id": record.dataset_id}
            )
        if record.contract.dataset_id != record.dataset_id:
            raise DatasetContractError(
                "Dataset and contract IDs differ.", details={"dataset_id": record.dataset_id}
            )
        if len(record.sha256) != 64 or any(char not in "0123456789abcdef" for char in record.sha256):
            raise DatasetContractError("Dataset source SHA-256 is malformed.")
        if record.dataset_id == "BEST2_FUTURE" and record.blindness_level is not BlindnessLevel.FUTURE_BLIND:
            raise DatasetContractError("BEST-2 must remain FUTURE_BLIND.")

    @property
    def records(self) -> tuple[ValidationDatasetRecord, ...]:
        return self._records

    @property
    def by_id(self) -> dict[str, ValidationDatasetRecord]:
        return {record.dataset_id: record for record in self._records}

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": "1.0.0",
            "source_of_truth": "ValidationDatasetRegistry",
            "datasets": [record.as_dict() for record in self._records],
        }

    def verify_source_hashes(self, repository_root: Path) -> tuple[str, ...]:
        errors: list[str] = []
        for record in self._records:
            source = repository_root / record.local_path
            if not source.is_file():
                errors.append(f"{record.dataset_id}:MISSING_SOURCE")
            elif sha256_file(source) != record.sha256:
                errors.append(f"{record.dataset_id}:HASH_MISMATCH")
        return tuple(errors)

    def verify_source_structures(self, repository_root: Path) -> tuple[str, ...]:
        """Validate source row/grid structure without reading scientific outcomes."""

        errors: list[str] = []
        required_csv_fields = {
            "BEST": {"experiment", "run_id", "exposure_id", "target_zone", "source_isotope"},
            "GALLEX_GNO": {"experiment", "record_type", "run_id", "source_isotope"},
            "SAGE_CR51": {"experiment", "run_id", "record_role", "source_isotope"},
            "SAGE_AR37": {"experiment", "run_id", "record_role", "source_isotope"},
            "GALLIUM_CROSS_SECTIONS": {"model", "year", "source_isotope", "cross_section_1e_minus_45_cm2"},
        }
        for record in self._records:
            source = repository_root / record.local_path
            if record.dataset_id in required_csv_fields and source.is_file():
                with source.open(encoding="utf-8", newline="") as handle:
                    reader = csv.DictReader(handle)
                    rows = sum(1 for _ in reader)
                    fields = set(reader.fieldnames or ())
                if rows != record.number_of_objects:
                    errors.append(f"{record.dataset_id}:ROW_COUNT_{rows}_EXPECTED_{record.number_of_objects}")
                missing = sorted(required_csv_fields[record.dataset_id] - fields)
                if missing:
                    errors.append(f"{record.dataset_id}:MISSING_FIELDS:{','.join(missing)}")
            elif record.dataset_id == "KATRIN" and source.is_file():
                value = json.loads(source.read_text(encoding="utf-8"))
                matrix = value.get("chiSquareMatrix", [])
                shape_ok = len(matrix) == 50 and all(isinstance(row, list) and len(row) == 50 for row in matrix)
                if not shape_ok:
                    errors.append("KATRIN:GRID_SHAPE_NOT_50X50")
        return tuple(errors)


def _contract(
    dataset_id: str,
    raw_source_identity: str,
    *,
    allowed_rows: tuple[str, ...],
    exclusions: tuple[str, ...],
    transformations: tuple[str, ...],
    units: tuple[tuple[str, str], ...],
    uncertainty_fields: tuple[str, ...],
    covariance_fields: tuple[str, ...],
    timing_fields: tuple[str, ...],
    geometry_fields: tuple[str, ...],
) -> DatasetContract:
    return DatasetContract(
        dataset_id=dataset_id,
        schema_version="1.0.0",
        raw_source_identity=raw_source_identity,
        allowed_rows=allowed_rows,
        exclusions=exclusions,
        transformations=transformations,
        units=units,
        missing_value_policy="Preserve NOT_PUBLIC/UNRESOLVED; never impute a scientific value.",
        derived_field_policy="Only deterministic, documented derivations are allowed and must retain an INFERENCE label.",
        uncertainty_fields=uncertainty_fields,
        covariance_fields=covariance_fields,
        timing_fields=timing_fields,
        geometry_fields=geometry_fields,
        provenance_fields=("source", "source_locator", "value_status", "sha256"),
    )


def canonical_dataset_registry() -> ValidationDatasetRegistry:
    """Return the source-derived Step 03 dataset catalog; no data values are fitted."""

    exposed = DataExposureClassification.MODEL_EXPOSED
    historical = BlindnessLevel.NON_BLIND_HISTORICAL
    records = (
        ValidationDatasetRecord(
            "BEST", "BEST", ("10.1103/PhysRevLett.128.232501", "10.1103/PhysRevC.105.065502"),
            "https://arxiv.org/abs/2201.07364",
            "LSC_6_3_0_VALIDATION/18_VALIDATION_READY/BEST_RUN_LEVEL.csv",
            "9bc2607b18aad11f5cd602cd547c3fe0f2052181386385247d819469c2fb3832",
            "2201.07364v3 / archive 2026-08-16", "B", "DERIVED_WITH_SOURCE_PROVENANCE", 20,
            "10 exposures x 2 target zones",
            ("production_rate", "published_zone_prediction", "ratio_R", "target_mass", "activity", "efficiencies"),
            ("asymmetric statistical", "common systematic budget", "source activity", "target mass"),
            "Full 20x20 and inner/outer joint covariance NOT_PUBLIC.",
            "Exposure interval and extraction/counting-start timestamps; UTC conversion explicitly INFERENCE.",
            "Two-zone dimensions, masses and average path lengths; no complete CAD/mesh.",
            "Surveyed Earth-fixed detector/source orientation NOT_PUBLIC.",
            "PRIMARY_GALLIUM_VALIDATION", ("T1", "T2", "T3", "T4", "T6", "T7", "T8", "T9", "T10", "T11"),
            ("T12",),
            ("Outer candidate row sum is 1070 while combined source row is 1069; policy PRESERVE_SOURCE_DISCREPANCY.",
             "Candidate/sub-run timestamps and collaboration likelihood workspace are unavailable."),
            "SOURCE_DERIVED_AND_HASH_VERIFIED", exposed, historical,
            _contract("BEST", "BEST_RUN_LEVEL.csv@sha256:9bc2607b18aad11f5cd602cd547c3fe0f2052181386385247d819469c2fb3832",
                allowed_rows=("All 20 zone-exposure rows; zone and exposure IDs are immutable.",),
                exclusions=("Do not replace outer row sum 1070 with combined value 1069 or vice versa.", "No midpoint-as-event-time use."),
                transformations=("Published day-of-year to UTC only where tagged INFERENCE and UTC+3 source basis is retained.", "Ratios are measured_rate/published_zone_prediction and remain INFERENCE."),
                units=(("production_rate", "71Ge atoms/day"), ("target_mass", "tonne"), ("activity", "MCi")),
                uncertainty_fields=("production_rate_stat_sigma_plus/minus", "production_rate_sys_pct_plus/minus_common"),
                covariance_fields=("NOT_PUBLIC",), timing_fields=("source_exposure_start/end_utc_inferred", "extraction_datetime_utc_inferred"),
                geometry_fields=("target_zone", "source_target_mass_t", "published average path length")),
        ),
        ValidationDatasetRecord(
            "GALLEX_GNO", "GALLEX/GNO", ("10.1016/j.physletb.2010.01.030",),
            "https://arxiv.org/abs/1001.2731",
            "LSC_6_3_0_VALIDATION/18_VALIDATION_READY/GALLEX_RUN_LEVEL.csv",
            "8535f227a1ef544b07967ca73125948e46c32f8ff38165e21305826af671f0b4",
            "1001.2731 / archive 2026-08-16", "B", "DERIVED_WITH_SOURCE_PROVENANCE", 83,
            "65 solar rows plus 18 51Cr source rows grouped as Cr1/Cr2",
            ("production_rate", "background rates", "source activity", "counter efficiency", "carrier yield"),
            ("asymmetric statistical where published", "limited published systematics"), "Full run covariance NOT_PUBLIC.",
            "Start date/day resolution; exact exposure times NOT_PUBLIC.", "Target mass and named source grouping; detailed geometry incomplete.",
            "NOT_PUBLIC.", "PRIMARY_GALLIUM_TRANSFER", ("T3", "T4", "T6", "T7", "T8", "T9", "T10", "T11"),
            ("T1", "T2", "T12"), ("Exact Cr exposure bounds and full covariance are unavailable.",),
            "SOURCE_DERIVED_AND_HASH_VERIFIED", exposed, historical,
            _contract("GALLEX_GNO", "GALLEX_RUN_LEVEL.csv@sha256:8535f227a1ef544b07967ca73125948e46c32f8ff38165e21305826af671f0b4",
                allowed_rows=("All 83 published source/solar rows.", "Source rows must retain Cr1/Cr2 grouping."),
                exclusions=("Solar rows are not source-exposure hold-outs.", "Do not invent exact time-of-day."),
                transformations=("End dates inferred from published duration remain explicitly INFERENCE.",),
                units=(("production_rate", "SNU or atoms/day as row-defined"), ("source_activity", "row-defined published unit")),
                uncertainty_fields=("stat_sigma_plus/minus", "systematic_sigma"), covariance_fields=("NOT_PUBLIC",),
                timing_fields=("published_start_or_run_date", "timestamp_end_inferred"), geometry_fields=("target_mass_t",)),
        ),
        ValidationDatasetRecord(
            "SAGE_CR51", "SAGE", ("10.1103/PhysRevC.59.2246",), "https://arxiv.org/abs/hep-ph/9803418",
            "LSC_6_3_0_VALIDATION/18_VALIDATION_READY/SAGE_CR51_RUN_LEVEL.csv",
            "26e4ac90edc325eec0e4d3d7639b43d61aced5dd6f7f21edf281b01a6ec4fe82",
            "hep-ph/9803418 / archive 2026-08-16", "B", "DERIVED_WITH_SOURCE_PROVENANCE", 12,
            "8 primary 51Cr exposures plus 4 secondary extraction controls",
            ("production_rate", "activity", "efficiencies", "candidate and fitted event counts"),
            ("asymmetric statistical", "published systematic percentages"), "Full covariance NOT_PUBLIC.",
            "Local/unzoned exposure intervals; UTC offset NOT_PUBLIC.", "Target mass only; detailed geometry incomplete.", "NOT_PUBLIC.",
            "PRIMARY_GALLIUM_TRANSFER", ("T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11"),
            ("T1", "T2", "T12"), ("Controls/failures may not be promoted to independent primary exposures.", "51Cr and 37Ar remain distinct isotope contracts."),
            "SOURCE_DERIVED_AND_HASH_VERIFIED", exposed, historical,
            _contract("SAGE_CR51", "SAGE_CR51_RUN_LEVEL.csv@sha256:26e4ac90edc325eec0e4d3d7639b43d61aced5dd6f7f21edf281b01a6ec4fe82",
                allowed_rows=("8 primary_source_exposure rows.", "4 controls retained for QA only."),
                exclusions=("Secondary extractions and failed/control rows are not independent validation observations.",),
                transformations=("Combined predicted rate inferred from published R stays INFERENCE.",),
                units=(("production_rate", "atoms/day"), ("source_activity", "kCi")),
                uncertainty_fields=("stat_sigma_plus/minus", "systematic_pct_plus/minus"), covariance_fields=("NOT_PUBLIC",),
                timing_fields=("source_exposure_start/end_unzoned",), geometry_fields=("gallium_mass_t",)),
        ),
        ValidationDatasetRecord(
            "SAGE_AR37", "SAGE", ("10.1103/PhysRevC.73.045805",), "https://arxiv.org/abs/nucl-ex/0512041",
            "LSC_6_3_0_VALIDATION/18_VALIDATION_READY/SAGE_37AR_RUN_LEVEL.csv",
            "f1ce4c8f696f0e936a1c886a7f0bee04e9ee3370f75f6ae461c57d82ce60d590",
            "nucl-ex/0512041 / archive 2026-08-16", "B", "DERIVED_WITH_SOURCE_PROVENANCE", 11,
            "10 primary 37Ar exposures plus Ar3-2 control/secondary extraction",
            ("production_rate", "activity", "efficiencies", "candidate and fitted event counts"),
            ("asymmetric statistical", "published systematic percentages"), "Full covariance NOT_PUBLIC.",
            "Local/unzoned exposure intervals; UTC offset NOT_PUBLIC.", "Target mass only; detailed geometry incomplete.", "NOT_PUBLIC.",
            "PRIMARY_GALLIUM_TRANSFER", ("T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11"),
            ("T1", "T2", "T12"), ("Ar3-2 is excluded from the collaboration combined result and remains a control.", "51Cr and 37Ar remain distinct isotope contracts."),
            "SOURCE_DERIVED_AND_HASH_VERIFIED", exposed, historical,
            _contract("SAGE_AR37", "SAGE_37AR_RUN_LEVEL.csv@sha256:f1ce4c8f696f0e936a1c886a7f0bee04e9ee3370f75f6ae461c57d82ce60d590",
                allowed_rows=("10 primary_source_exposure rows.", "Ar3-2 retained as a control only."),
                exclusions=("Ar3-2 is not an independent primary exposure.",), transformations=(),
                units=(("production_rate", "atoms/day"), ("source_activity", "kCi")),
                uncertainty_fields=("stat_sigma_plus/minus", "systematic_pct_plus/minus"), covariance_fields=("NOT_PUBLIC",),
                timing_fields=("source_exposure_start/end_unzoned",), geometry_fields=("gallium_mass_t",)),
        ),
        ValidationDatasetRecord(
            "GALLIUM_CROSS_SECTIONS", "Gallium cross-section theory",
            ("10.1103/PhysRevC.56.3391", "10.1103/PhysRevC.108.035502", "10.1016/j.physletb.2019.06.057"),
            "https://arxiv.org/abs/2303.13623", "LSC_6_3_0_VALIDATION/05_GALLIUM_CROSS_SECTIONS/CROSS_SECTION_MODELS.csv",
            "b6e8318334698cb0725e9c508dd1b9e8a75d426a4083912e0bde2f7705db90b9",
            "archive 2026-08-16", "B", "DERIVED_WITH_SOURCE_PROVENANCE", 15, "Published model-isotope rows",
            ("total cross section", "ground-state contribution", "split-normal marginal uncertainty"),
            ("published asymmetric marginal uncertainty",), "Cross-isotope/model joint covariance NOT_PUBLIC.",
            "NOT_APPLICABLE.", "NOT_APPLICABLE.", "NOT_APPLICABLE.", "NUCLEAR_MODEL_SENSITIVITY",
            ("T5", "T8", "T10", "T11"), ("T12",),
            ("No model is designated correct or default.", "Krofcheck and Frekers alternatives must not be combined."),
            "SOURCE_DERIVED_AND_HASH_VERIFIED", exposed, historical,
            _contract("GALLIUM_CROSS_SECTIONS", "CROSS_SECTION_MODELS.csv@sha256:b6e8318334698cb0725e9c508dd1b9e8a75d426a4083912e0bde2f7705db90b9",
                allowed_rows=("All published model/isotope alternatives.",), exclusions=("Do not average models into an invented default.",),
                transformations=("Split-normal fields are source-derived marginal summaries only.",),
                units=(("cross_section", "1e-45 cm2"),), uncertainty_fields=("sigma_plus", "sigma_minus"),
                covariance_fields=("NOT_PUBLIC",), timing_fields=(), geometry_fields=()),
        ),
        ValidationDatasetRecord(
            "KATRIN", "KATRIN", ("10.5281/zenodo.15860994", "10.1038/s41586-025-09739-9"),
            "https://zenodo.org/records/19369714",
            "LSC_6_3_0_VALIDATION/06_KATRIN/records/19369714/files/Main_result_KNM1to5_chi_square_map.json",
            "64d968ff1ad6fcc231a12eec52ae64d657a1a23c6cec7fe3fe95789725b26336",
            "record 19369714 (2026-04-01)", "A", "RAW_PUBLIC_RELEASE", 2500, "50x50 absolute chi-square grid",
            ("mnu2sterile", "sin2thetaee", "absolute chi-square"), ("grid likelihood surface",),
            "Grid supplied; no gallium-LSC joint covariance.", "NOT_APPLICABLE.", "NOT_APPLICABLE.", "NOT_APPLICABLE.",
            "EXTERNAL_CONSTRAINT_ONLY", ("T10",), ("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T11", "T12"),
            ("An explicit frozen LSC-to-KATRIN mapping is absent.", "Grid is absolute chi-square, not delta chi-square; confidence construction is not inferred."),
            "PUBLIC_RELEASE_HASH_VERIFIED", exposed, historical,
            _contract("KATRIN", "record-19369714/Main_result_KNM1to5_chi_square_map.json",
                allowed_rows=("All 50x50 finite/capped grid cells.",), exclusions=("No confidence-level assignment without documented construction.",),
                transformations=("Finite-grid minimum may be subtracted only when explicitly requested and labelled.",),
                units=(("mnu2sterile", "eV2"), ("sin2thetaee", "dimensionless"), ("chi_square", "dimensionless")),
                uncertainty_fields=("chi_square grid",), covariance_fields=(), timing_fields=(), geometry_fields=()),
        ),
        ValidationDatasetRecord(
            "ICECUBE", "IceCube", ("10.7910/DVN/QKL28Z", "10.7910/DVN/OSPLDG", "10.7910/DVN/MMIIZA"),
            "https://icecube.wisc.edu/science/data-releases/",
            "LSC_6_3_0_VALIDATION/07_ICECUBE/ICECUBE_FILE_INTEGRITY.csv",
            "e2a93f7af91671bc60714c16a2e84b858b7969d9a5297690245490324ba48548",
            "archive 2026-08-16", "C", "RAW_AND_RELEASE_INDEX", 52, "Current Dataverse file integrity records",
            ("sterile contours", "likelihood-metric differences", "events/uptime/response by release"),
            ("release-specific statistical products",), "Release-specific; no LSC mapping or joint covariance.",
            "Event-level only for IceTracks; other releases vary.", "Response metadata by release.", "Directional quantities only where release-specific, not BEST orientation.",
            "EXTERNAL_CONSTRAINT_ONLY", ("T10",), ("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T11", "T12"),
            ("DeepCore is Grade C for independent reanalysis; aggregate grade is conservative.", "Explicit frozen mapping and confidence construction are required."),
            "PUBLIC_RELEASE_INDEX_HASH_VERIFIED", exposed, historical,
            _contract("ICECUBE", "ICECUBE_FILE_INTEGRITY.csv@sha256:e2a93f7af91671bc60714c16a2e84b858b7969d9a5297690245490324ba48548",
                allowed_rows=("Only release files whose identity/integrity status is recorded.",), exclusions=("No cross-release likelihood multiplication.",),
                transformations=("Release-native test statistics and confidence construction must be preserved.",),
                units=(("release_defined", "release-defined"),), uncertainty_fields=("release-defined"), covariance_fields=("release-defined"),
                timing_fields=("release-defined"), geometry_fields=("release-defined")),
        ),
        ValidationDatasetRecord(
            "BOREXINO", "Borexino", ("NOT_RECORDED_IN_ARCHIVE; see arXiv:1701.07970, 2204.07029, 2205.15975, 2307.14636",),
            "https://bxopen.lngs.infn.it/", "LSC_6_3_0_VALIDATION/08_BOREXINO/BOREXINO_RESOURCE_MATRIX.csv",
            "98378dc8e2e51e0e3c0150c228a7d5ce666aa649dac82e748de1d763314cf106",
            "archive 2026-08-16", "B", "RAW_RELEASE_INDEX", 6, "Retained open-data resource groups",
            ("7Be time series", "orbital time series/periodograms", "CNO spectrum/correlation/likelihood"),
            ("binned rate errors", "14x14 published CNO correlation"), "Available only for CNO spectral package; not full time-bin covariance.",
            "30.4-day/7-day and 30-day/8-hour bins; explicit UTC origin for orbital release.", "Experiment-specific; no BEST geometry mapping.",
            "No surveyed BEST-compatible orientation.", "METHODOLOGY_CONTROL", (), tuple(f"T{i}" for i in range(1, 13)),
            ("Temporal-methodology control, not direct gallium evidence.", "No frozen LSC-to-Borexino observable mapping."),
            "PUBLIC_RELEASE_INDEX_HASH_VERIFIED", exposed, historical,
            _contract("BOREXINO", "BOREXINO_RESOURCE_MATRIX.csv@sha256:98378dc8e2e51e0e3c0150c228a7d5ce666aa649dac82e748de1d763314cf106",
                allowed_rows=("Archived public time-series and CNO resources only.",), exclusions=("No direct gallium-LSC inference.",),
                transformations=("Preserve published binning and UTC origin.",), units=(("rate", "source-defined"),),
                uncertainty_fields=("published bin errors", "CNO correlation/likelihood"), covariance_fields=("CNO 14x14 only",),
                timing_fields=("source-defined binned time",), geometry_fields=()),
        ),
        ValidationDatasetRecord(
            "DAYA_BAY", "Daya Bay", ("10.5281/zenodo.17587229",), "https://zenodo.org/records/17587229",
            "LSC_6_3_0_VALIDATION/09_OTHER_NEUTRINO_CONSTRAINTS/DayaBay/data/dayabay_analysis_dataset_tsv_1-0-0.zip",
            "fbbc75791315a7c75c7a0d89dc7629aae33649e7e7901ab317f97a2d69fa4f5b", "1.0.0", "A", "RAW_PUBLIC_RELEASE", 213,
            "Compact TSV archive members", ("spectra", "detector performance", "backgrounds", "efficiencies", "responses", "reactor rates", "baselines"),
            ("published model uncertainties",), "Release-specific matrices/inputs.", "Daily performance and run coverage.", "Published reactor-detector baselines.",
            "NOT_APPLICABLE to gallium orientation.", "EXTERNAL_CONVENTIONAL_CONTROL", ("T10",), tuple(f"T{i}" for i in range(1, 10)) + ("T11", "T12"),
            ("Not a gallium source dataset; no automatic LSC likelihood combination."), "PUBLIC_RELEASE_HASH_VERIFIED", exposed, historical,
            _contract("DAYA_BAY", "dayabay_analysis_dataset_tsv_1-0-0.zip@sha256:fbbc75791315a7c75c7a0d89dc7629aae33649e7e7901ab317f97a2d69fa4f5b",
                allowed_rows=("All compact analysis package members covered by its release identity.",), exclusions=("No ordinary three-flavor release reinterpretation as sterile constraint without a declared likelihood.",),
                transformations=("Preserve release-native response/correction definitions.",), units=(("release_defined", "release-defined"),),
                uncertainty_fields=("release-defined"), covariance_fields=("release-defined"), timing_fields=("daily detector performance"), geometry_fields=("reactor-detector baselines",)),
        ),
        ValidationDatasetRecord(
            "PROSPECT", "PROSPECT", ("10.1103/PhysRevLett.134.151802",), "https://arxiv.org/abs/2406.10408",
            "LSC_6_3_0_VALIDATION/09_OTHER_NEUTRINO_CONSTRAINTS/PROSPECT/Papers/PROSPECT_Final_2406.10408_source.tar",
            "0e8a7a4314a1405df00000d54249b54ae9031726ee716ed3336df34f255ab7f0", "2406.10408 source", "A", "RAW_PUBLIC_RELEASE", 76,
            "Ancillary numerical analysis files", ("spectra", "baseline distributions", "response matrices", "covariance", "delta-chi-square", "CLs contours"),
            ("statistical/background/systematic covariance",), "Published covariance matrices available.", "Release-defined periods.", "Six baseline bins and response matrices.", "NOT_APPLICABLE.",
            "EXTERNAL_STERILE_BASELINE_CONTROL", ("T10",), tuple(f"T{i}" for i in range(1, 10)) + ("T11", "T12"),
            ("Preserve collaboration CLs/statistical construction.", "Not direct LSC validation."), "PUBLIC_RELEASE_HASH_VERIFIED", exposed, historical,
            _contract("PROSPECT", "PROSPECT source tar@sha256:0e8a7a4314a1405df00000d54249b54ae9031726ee716ed3336df34f255ab7f0",
                allowed_rows=("All 76 ancillary files under Source/anc/data.",), exclusions=("No Gaussian reinterpretation of CLs grids.",),
                transformations=("Use collaboration parsing and response conventions.",), units=(("release_defined", "release-defined"),),
                uncertainty_fields=("published covariance products",), covariance_fields=("statistical", "background", "systematic"), timing_fields=("period identifiers"), geometry_fields=("baseline distributions",)),
        ),
        ValidationDatasetRecord(
            "STEREO", "STEREO", ("10.1038/s41586-022-05568-2", "10.17182/hepdata.132368.v2"),
            "https://www.hepdata.net/record/132368", "LSC_6_3_0_VALIDATION/09_OTHER_NEUTRINO_CONSTRAINTS/STEREO/metadata/hepdata_132368_v2.json",
            "c0d3f00e46bf5c8f23883ef7000fc205e32da840ea8897b89e51cbbd221d52e4", "HEPData v2", "A", "RAW_PUBLIC_METADATA", 6,
            "Core acquired HEPData tables", ("cell spectra", "covariance", "response", "delta-chi-square", "critical map", "contours"),
            ("prompt-spectrum covariance",), "Published selected covariance available.", "Release-defined.", "Detector-cell structure/response.", "NOT_APPLICABLE.",
            "EXTERNAL_STERILE_BASELINE_CONTROL", ("T10",), tuple(f"T{i}" for i in range(1, 10)) + ("T11", "T12"),
            ("Do not treat test-statistic grids as Gaussian likelihoods.", "Not direct LSC validation."), "PUBLIC_RELEASE_HASH_VERIFIED", exposed, historical,
            _contract("STEREO", "hepdata_132368_v2.json@sha256:c0d3f00e46bf5c8f23883ef7000fc205e32da840ea8897b89e51cbbd221d52e4",
                allowed_rows=("Six acquired core tables; other indexed tables require separate acquisition identity.",), exclusions=("No automatic likelihood multiplication.",),
                transformations=("Preserve HEPData schema and collaboration confidence construction.",), units=(("release_defined", "release-defined"),),
                uncertainty_fields=("prompt-spectrum covariance",), covariance_fields=("published selected covariance",), timing_fields=(), geometry_fields=("detector cell",)),
        ),
        ValidationDatasetRecord(
            "MICROBOONE", "MicroBooNE", ("10.1038/s41586-025-09757-7", "10.17182/hepdata.166435.v1"),
            "https://www.hepdata.net/record/166435", "LSC_6_3_0_VALIDATION/09_OTHER_NEUTRINO_CONSTRAINTS/MicroBooNE/metadata/hepdata_166435.json",
            "a206472feb62992cb3402360a906e3971388e6d18d89e190f1120f1ebc474dd6", "HEPData v1", "A", "RAW_PUBLIC_METADATA", 4,
            "Core acquired numerical products", ("14-channel spectra", "constrained channels", "364x364 systematic covariance", "3D delta-chi-square map"),
            ("systematic covariance; data statistical treatment is release-specific",), "364x364 systematic covariance available.", "Release-defined.", "Beam/detector analysis geometry only.", "NOT_APPLICABLE.",
            "EXTERNAL_STERILE_BASELINE_CONTROL", ("T10",), tuple(f"T{i}" for i in range(1, 10)) + ("T11", "T12"),
            ("Preserve Combined Neyman-Pearson treatment.", "Not direct LSC validation."), "PUBLIC_RELEASE_HASH_VERIFIED", exposed, historical,
            _contract("MICROBOONE", "hepdata_166435.json@sha256:a206472feb62992cb3402360a906e3971388e6d18d89e190f1120f1ebc474dd6",
                allowed_rows=("Four acquired core products with their release metadata.",), exclusions=("No direct gallium inference or automatic likelihood multiplication.",),
                transformations=("Preserve release channel ordering and confidence construction.",), units=(("release_defined", "release-defined"),),
                uncertainty_fields=("systematic covariance",), covariance_fields=("364x364 systematic covariance",), timing_fields=(), geometry_fields=("release-defined",)),
        ),
        ValidationDatasetRecord(
            "BEST2_FUTURE", "BEST-2", ("10.1134/S106377881901006X", "10.31857/S0044451025030058", "10.1134/S1063779624702411"),
            "https://arxiv.org/abs/2501.08127", "LSC_6_3_0_VALIDATION/10_BEST2_FUTURE/BEST2_PREDICTION_TARGET.md",
            "135472df388da8d532a9d98c7f00a75833d4e460c26c16f8cb661f6585a89ba3", "proposal archive 2026-08-16", "E", "PROPOSAL_ONLY", 0,
            "No observed measurement objects", ("planned three-zone 58Co observables only",), ("proposal estimates only",), "Not available.",
            "Proposed 10 x 16-day exposures; actual calendar unavailable.", "Proposal geometry, not as-built survey.", "Not available.",
            "FUTURE_BLIND_PREDICTION_TARGET", (), tuple(f"T{i}" for i in range(1, 13)),
            ("No observed results, source certificate, as-built geometry or final schedule.", "No numerical prediction may be generated in Step 03."),
            "PROPOSAL_HASH_VERIFIED", DataExposureClassification.MODEL_PREEXISTING, BlindnessLevel.FUTURE_BLIND,
            _contract("BEST2_FUTURE", "BEST2_PREDICTION_TARGET.md@sha256:135472df388da8d532a9d98c7f00a75833d4e460c26c16f8cb661f6585a89ba3",
                allowed_rows=("Proposal metadata only; zero observation rows.",), exclusions=("All future observed values until a timestamped prediction freeze is sealed.",),
                transformations=(), units=(("proposal_fields", "source-defined"),), uncertainty_fields=("proposal-only",), covariance_fields=("MISSING",),
                timing_fields=("proposed schedule only",), geometry_fields=("proposal geometry only",)),
        ),
    )
    return ValidationDatasetRegistry(records)
