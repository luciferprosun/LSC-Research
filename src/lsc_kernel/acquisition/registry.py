"""Canonical Step 05 blocker registry and unlock-set definitions."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class BlockerRecord:
    blocker_id: str
    category: str
    priority: str
    object: str
    required_for: tuple[str, ...]
    current_status: str
    evidence: tuple[str, ...]
    source: tuple[str, ...]
    adjudication: str
    next_possible_action: str
    unlocks_tests: tuple[str, ...]
    human_contact_required: bool
    publication_dependency: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def canonical_blocker_records() -> tuple[BlockerRecord, ...]:
    return (
        BlockerRecord(
            "BLK-P0-FROZEN-BUNDLE", "FROZEN_MODEL", "P0", "complete authentic LSC 6.3.0 numerical bundle",
            ("LSC prediction", "T1-T11"),
            "STILL_MISSING",
            ("targeted Git/reflog/object/release scan complete", "Zenodo release contains no numerical bundle"),
            ("LSC-Research commit 75901c968c7dbde7a16ea4836b18b8163950befa", "Zenodo 10.5281/zenodo.20377427"),
            "AUTHENTIC_FROZEN_BUNDLE_INCOMPLETE",
            "Human provenance search in private historical media or author-held release workspace; do not reconstruct.",
            tuple(f"T{i}" for i in range(1, 12)),
            True, True,
        ),
        BlockerRecord(
            "BLK-P1-BEST-COV", "COLLABORATION_COVARIANCE", "P1", "BEST run/zone covariance and likelihood workspace",
            ("COV_COLLABORATION", "inferential T1/T2/T6/T11"),
            "NOT_LOCATED",
            ("published summary covariance prescription recovered", "full 20-row/run covariance not located"),
            ("arXiv:2109.11482", "arXiv:2201.07364"),
            "AUTHORITATIVE_COLLABORATION_RECOVERED_SUMMARY_ONLY",
            "Request the exact run/zone covariance or likelihood object and nuisance definitions from BEST.",
            ("T1", "T2", "T6", "T9", "T11"),
            True, False,
        ),
        BlockerRecord(
            "BLK-P1-SAGE-COV", "COLLABORATION_COVARIANCE", "P1", "SAGE 51Cr/37Ar run covariance and exact UTC metadata",
            ("COV_COLLABORATION", "run transfer", "directional readiness"),
            "NOT_LOCATED",
            ("published run tables and marginal/systematic uncertainties recovered",),
            ("SAGE 51Cr source paper", "SAGE 37Ar source paper"),
            "AUTHORITATIVE_SOURCE_TABLES_RECOVERED_COVARIANCE_MISSING",
            "Request run covariance, source-calibration correlations, UTC convention, and available orientation metadata.",
            ("T3", "T5", "T6", "T7", "T12"),
            True, False,
        ),
        BlockerRecord(
            "BLK-P1-GALLEX-COV", "COLLABORATION_COVARIANCE", "P1", "GALLEX Cr source covariance and exact UTC intervals",
            ("COV_COLLABORATION", "run transfer", "directional readiness"),
            "NOT_LOCATED",
            ("source-run tables and analysis method recovered", "solar reanalysis correlation is not source covariance"),
            ("arXiv:1001.2731",),
            "AUTHORITATIVE_SOURCE_TABLES_RECOVERED_COVARIANCE_MISSING",
            "Request source-run covariance/likelihood, correlation definitions, and exact interval timezone.",
            ("T3", "T5", "T6", "T7", "T12"),
            True, False,
        ),
        BlockerRecord(
            "BLK-P1-NUCLEAR-COV", "NUCLEAR_COVARIANCE", "P1", "joint 51Cr/37Ar transition-strength covariance",
            ("cross-isotope inference", "COV_COLLABORATION"),
            "STILL_MISSING",
            ("authoritative marginal uncertainties and common-systematic statement recovered",),
            ("arXiv:2303.13623", "arXiv:hep-ph/9710491"),
            "MARGINAL_ONLY",
            "Request the numerical joint covariance or posterior samples if distributable.",
            ("T5", "T8"),
            True, False,
        ),
        BlockerRecord(
            "BLK-P2-KATRIN-MAP", "EXTERNAL_MAPPING", "P2", "LSC-to-KATRIN observable/parameter mapping",
            ("KATRIN external veto",),
            "STILL_MISSING",
            ("KATRIN absolute chi-square grid validated", "LSC has no sterile-mass/mixing mapping equations"),
            ("Zenodo 10.5281/zenodo.19369714", "LSC E1-E12"),
            "MAPPING_NOT_JUSTIFIED",
            "A new theory-level mapping would require separate preregistration and provenance; do not infer it.",
            ("T10",),
            False, False,
        ),
        BlockerRecord(
            "BLK-P2-ICECUBE-MAP", "EXTERNAL_MAPPING", "P2", "LSC-to-IceCube observable/parameter mapping",
            ("IceCube external veto",),
            "STILL_MISSING",
            ("IceCube release objects validated", "LSC has no flavor/matter-propagation mapping equations"),
            ("arXiv:2407.01314", "LSC E1-E12"),
            "MAPPING_NOT_JUSTIFIED",
            "Any model-dependent translation must be developed and frozen as new theory before use.",
            ("T10",),
            False, False,
        ),
        BlockerRecord(
            "BLK-P3-M3-GEOMETRY", "GEOMETRY", "P3", "production M3 source/detector path-length distributions",
            ("exact sterile 3+1 baseline",),
            "STILL_MISSING",
            ("published average paths and Monte Carlo descriptions recovered", "no exact machine-readable volume models located"),
            ("BEST source paper", "SAGE source papers", "GALLEX reanalysis"),
            "PUBLISHED_AVERAGE_GEOMETRY",
            "Acquire collaboration geometry definitions/integration code or retain approximation label.",
            ("T10",),
            True, False,
        ),
        BlockerRecord(
            "BLK-P4-M4-HIERARCHY", "BASELINE_SPECIFICATION", "P4", "canonical hierarchical M4 probability model",
            ("M_HIERARCHICAL_EXPERIMENT execution",),
            "STILL_MISSING",
            ("authentic high-level M4 detector-systematics schema recovered", "hierarchy distributions/priors absent"),
            ("implementation/LSC_M4_IMPLEMENTATION_SCHEMA.md",),
            "SPECIFICATION_INCOMPLETE",
            "Keep canonical M4 hierarchical execution disabled; a new baseline needs a distinct identity.",
            ("T1", "T3", "T7", "T11"),
            False, False,
        ),
        BlockerRecord(
            "BLK-P5-T12", "DIRECTIONAL_DATA", "P5", "timing, orientation, geometry, tensor, frames, and units",
            ("T12",),
            "STILL_MISSING",
            ("exposure intervals are multi-day aggregates", "surveyed axes and active tensor unavailable"),
            ("BEST/SAGE/GALLEX source papers", "LSC frozen specification"),
            "BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT",
            "Acquire every T12 prerequisite; exposure midpoint remains prohibited.",
            ("T12",),
            True, False,
        ),
        BlockerRecord(
            "BLK-FUTURE-BEST2", "FUTURE_DATA", "P5", "BEST-2 as-built geometry/source/exposure freeze inputs",
            ("future blind BEST-2 prediction",),
            "NOT_PUBLIC",
            ("concept-level public information only",),
            ("BEST-2 future contract",),
            "FUTURE_ONLY",
            "Wait for authoritative as-built inputs, then freeze prediction before observed results.",
            (),
            True, True,
        ),
    )


def minimum_validation_unlock_set() -> dict[str, object]:
    return {
        "set_id": "MINIMUM_VALIDATION_UNLOCK_SET",
        "purpose": "First controlled preregistered scalar LSC test in Step 06 or later.",
        "required": [
            "AUTHENTIC_FROZEN_BUNDLE_COMPLETE",
            "target-dataset exposure classification recorded; non-clean historical tests never relabelled blind",
            "unambiguous parameter ordering, units, frames, active tensor semantics where required by E1-E12",
            "exact evaluator initialization/configuration and executable input mapping",
            "hash-verified provenance admission",
            "separate human-approved Step 06 execution authorization",
        ],
        "not_required_for_sensitivity_only_first_run": [
            "T12 directional inputs",
            "KATRIN/IceCube mapping",
            "full collaboration covariance if result is explicitly SENSITIVITY_ONLY",
        ],
        "complete": False,
        "blocking_ids": ["BLK-P0-FROZEN-BUNDLE"],
    }


def full_validation_unlock_set() -> dict[str, object]:
    return {
        "set_id": "FULL_VALIDATION_UNLOCK_SET",
        "purpose": "Inferential execution of the frozen primary sequence T11, T7, T3, T1, T10.",
        "required": [
            "MINIMUM_VALIDATION_UNLOCK_SET complete",
            "authenticated collaboration covariance/likelihood for every reached primary dataset",
            "cross-experiment and shared nuclear covariance treatment with authoritative provenance",
            "production M3 geometry for T10",
            "explicit authorized external mappings wherever a veto is invoked",
            "all test-specific prerequisites and unchanged frozen multiple-testing sequence",
        ],
        "directional_component": "T12 remains a separate blocked component and is not silently required for scalar tests.",
        "complete": False,
        "blocking_ids": [
            "BLK-P0-FROZEN-BUNDLE",
            "BLK-P1-BEST-COV",
            "BLK-P1-SAGE-COV",
            "BLK-P1-GALLEX-COV",
            "BLK-P1-NUCLEAR-COV",
            "BLK-P2-KATRIN-MAP",
            "BLK-P2-ICECUBE-MAP",
            "BLK-P3-M3-GEOMETRY",
        ],
    }


def blocker_registry() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "as_of": "2026-08-16",
        "policy": "RECOVER OR PROVE THE GAP - NEVER FILL THE GAP",
        "records": [record.as_dict() for record in canonical_blocker_records()],
        "minimum_validation_unlock_set": minimum_validation_unlock_set(),
        "full_validation_unlock_set": full_validation_unlock_set(),
        "prediction_authorized": False,
        "numerical_validation_authorized": False,
    }
