#!/usr/bin/env python3
"""Generate deterministic Step 05 acquisition and evidence artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from lsc_kernel.acquisition.evidence import build_evidence_freeze  # noqa: E402
from lsc_kernel.acquisition.registry import (  # noqa: E402
    blocker_registry,
    full_validation_unlock_set,
    minimum_validation_unlock_set,
)
from lsc_kernel.frozen.evaluator import FrozenLSCEvaluator  # noqa: E402
from lsc_kernel.io.manifests import write_json  # noqa: E402
from tools.generate_step04_artifacts import generate as generate_step04  # noqa: E402

ACQUISITION_TIMESTAMP = "2026-08-16T10:46:00+02:00"


def source_precedence_policy() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "policy": "NO POST-HOC RECONSTRUCTION",
        "tiers": [
            {"tier": 1, "name": "EXACT_FROZEN_RELEASE_MACHINE_CONFIG", "potentially_admissible": True},
            {"tier": 2, "name": "EXACT_FROZEN_COMMIT_CONFIG_OR_SOURCE", "potentially_admissible": True},
            {"tier": 3, "name": "EXACT_ARCHIVED_RELEASE_MACHINE_ARTIFACT", "potentially_admissible": True},
            {"tier": 4, "name": "VERSIONED_NUMERICAL_TABLE_TIED_TO_FREEZE", "potentially_admissible": True},
            {"tier": 5, "name": "NUMERICAL_APPENDIX_TIED_TO_RELEASE", "potentially_admissible": True},
            {"tier": 6, "name": "HISTORICAL_CANDIDATE", "potentially_admissible": False},
            {"tier": 7, "name": "INFERENCE_OR_DIGITISATION", "potentially_admissible": False},
        ],
        "frozen_authenticity_requirements": [
            "exact frozen lineage",
            "unambiguous ordering, units, frame, and tensor semantics",
            "no conflicts",
            "no historical composite",
        ],
        "clean_predictor_additional_requirements": [
            "PRE_DATA or PRE_TARGET_DATA exposure for the intended target",
            "historical non-blind tests retain their exposure label",
        ],
    }


def blocker_dependency_graph() -> dict[str, object]:
    nodes = [
        "FROZEN_NUMERICAL_BUNDLE",
        "STEP06_CERTIFICATION",
        "LSC_PREDICTION",
        "T11",
        "T7",
        "T3",
        "T1",
        "T10",
        "COLLABORATION_COVARIANCE",
        "INFERENTIAL_LIKELIHOOD",
        "KATRIN_MAPPING",
        "ICECUBE_MAPPING",
        "EXTERNAL_VETO",
        "M3_GEOMETRY",
        "M3_PRODUCTION",
        "TIMING_ORIENTATION_TENSOR_FRAMES",
        "T12",
        "BEST2_AS_BUILT_INPUTS",
        "BEST2_FUTURE_BLIND_PREDICTION",
    ]
    edges = [
        ("FROZEN_NUMERICAL_BUNDLE", "STEP06_CERTIFICATION"),
        ("STEP06_CERTIFICATION", "LSC_PREDICTION"),
        ("LSC_PREDICTION", "T11"),
        ("T11", "T7"),
        ("T7", "T3"),
        ("T3", "T1"),
        ("T1", "T10"),
        ("COLLABORATION_COVARIANCE", "INFERENTIAL_LIKELIHOOD"),
        ("KATRIN_MAPPING", "EXTERNAL_VETO"),
        ("ICECUBE_MAPPING", "EXTERNAL_VETO"),
        ("EXTERNAL_VETO", "T10"),
        ("M3_GEOMETRY", "M3_PRODUCTION"),
        ("M3_PRODUCTION", "T10"),
        ("TIMING_ORIENTATION_TENSOR_FRAMES", "T12"),
        ("BEST2_AS_BUILT_INPUTS", "BEST2_FUTURE_BLIND_PREDICTION"),
    ]
    return {
        "schema_version": "1.0.0",
        "nodes": nodes,
        "edges": [{"from": source, "to": target} for source, target in edges],
        "step05_execution_authorized": False,
    }


def blocker_dependency_dot() -> str:
    graph = blocker_dependency_graph()
    lines = ["digraph Step05Blockers {", "  rankdir=LR;"]
    for edge in graph["edges"]:
        lines.append(f'  "{edge["from"]}" -> "{edge["to"]}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def evidence_records() -> tuple[dict[str, object], ...]:
    root = "LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research"
    return (
        {
            "path": f"{root}/canonical/LSC_ACTIVE_EQUATION_SET.md",
            "object_id": "canonical-equations",
            "provenance_class": "AUTHENTIC_FROZEN",
            "source_identifier": "Git 75901c968c7dbde7a16ea4836b18b8163950befa",
            "adjudication": "SYMBOLIC_SPECIFICATION_ONLY",
        },
        {
            "path": f"{root}/canonical/LSC_CANONICAL_CORE.md",
            "object_id": "canonical-parameter-structures",
            "provenance_class": "AUTHENTIC_FROZEN",
            "source_identifier": "Git 75901c968c7dbde7a16ea4836b18b8163950befa",
            "adjudication": "SYMBOLIC_NAMES_AND_SEMANTICS_ONLY",
        },
        {
            "path": f"{root}/canonical/LSC_FREEZE_BOUNDARY.md",
            "object_id": "canonical-freeze-boundary",
            "provenance_class": "AUTHENTIC_FROZEN",
            "source_identifier": "Git 75901c968c7dbde7a16ea4836b18b8163950befa",
            "adjudication": "PRIMARY_NEGATIVE_EVIDENCE",
        },
        {
            "path": "LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/zenodo_record_20377427/files/zenodo25maj.zip",
            "object_id": "zenodo-release-archive",
            "provenance_class": "AUTHENTIC_FROZEN",
            "source_identifier": "10.5281/zenodo.20377427",
            "adjudication": "NO_NUMERICAL_BUNDLE_IN_ARCHIVE",
        },
        {
            "path": f"{root}/historical_archive/pre_step5_repository/LSC_core/arXiv last edition 13.05/source/outputs/model_parameters.csv",
            "object_id": "postdata-toy-c0-c1",
            "provenance_class": "HISTORICAL_POST_DATA",
            "source_identifier": "Git 700aa9262df66731f0fc180af44fbdea9897623d",
            "adjudication": "REJECTED_AS_FROZEN_INPUT",
        },
        {
            "path": "LSC_6_3_0_VALIDATION/02_BEST/Papers/arXiv_2201.07364/BEST_2201.07364_source.tar",
            "object_id": "best-detailed-paper-source",
            "provenance_class": "AUTHORITATIVE_COLLABORATION_RECOVERED",
            "source_identifier": "arXiv:2201.07364v3",
            "adjudication": "SUMMARY_COVARIANCE_AND_GEOMETRY_ONLY",
        },
        {
            "path": "LSC_6_3_0_VALIDATION/03_GALLEX_GNO/Papers/GALLEX_reanalysis_1001.2731_source.tar",
            "object_id": "gallex-reanalysis-source",
            "provenance_class": "AUTHORITATIVE_EXTERNAL_RECOVERED",
            "source_identifier": "arXiv:1001.2731",
            "adjudication": "SOURCE_TABLES_RECOVERED_COVARIANCE_MISSING",
        },
        {
            "path": "LSC_6_3_0_VALIDATION/04_SAGE/Papers/SAGE_Cr51_hep-ph_9803418_source.tar",
            "object_id": "sage-cr51-source",
            "provenance_class": "AUTHORITATIVE_EXTERNAL_RECOVERED",
            "source_identifier": "arXiv:hep-ph/9803418",
            "adjudication": "SOURCE_TABLES_RECOVERED_COVARIANCE_MISSING",
        },
        {
            "path": "LSC_6_3_0_VALIDATION/04_SAGE/Papers/SAGE_Ar37_nucl-ex_0512041_source.tar",
            "object_id": "sage-ar37-source",
            "provenance_class": "AUTHORITATIVE_EXTERNAL_RECOVERED",
            "source_identifier": "arXiv:nucl-ex/0512041",
            "adjudication": "SOURCE_TABLES_RECOVERED_COVARIANCE_MISSING",
        },
        {
            "path": "LSC_6_3_0_VALIDATION/05_GALLIUM_CROSS_SECTIONS/Papers/Elliott_Gavrin_Haxton_2303.13623_source.tar",
            "object_id": "nuclear-cross-section-source",
            "provenance_class": "AUTHORITATIVE_EXTERNAL_RECOVERED",
            "source_identifier": "arXiv:2303.13623",
            "adjudication": "MARGINAL_ONLY",
        },
        {
            "path": "LSC_6_3_0_VALIDATION/06_KATRIN/records/19369714/files/Main_result_KNM1to5_chi_square_map.json",
            "object_id": "katrin-grid",
            "provenance_class": "AUTHORITATIVE_EXTERNAL_RECOVERED",
            "source_identifier": "10.5281/zenodo.19369714",
            "adjudication": "NATIVE_GRID_VALID_LSC_MAPPING_NOT_JUSTIFIED",
        },
        {
            "path": "LSC_6_3_0_VALIDATION/07_ICECUBE/ICECUBE_FILE_INTEGRITY.csv",
            "object_id": "icecube-release-index",
            "provenance_class": "DERIVED_WITH_EXACT_PROVENANCE",
            "source_identifier": "archived IceCube releases",
            "adjudication": "NATIVE_RELEASE_VALID_LSC_MAPPING_NOT_JUSTIFIED",
        },
        {
            "path": f"{root}/implementation/LSC_M4_IMPLEMENTATION_SCHEMA.md",
            "object_id": "historical-m4-schema",
            "provenance_class": "AUTHENTIC_FROZEN",
            "source_identifier": "Git 75901c968c7dbde7a16ea4836b18b8163950befa",
            "adjudication": "HIGH_LEVEL_SCHEMA_HIERARCHY_INCOMPLETE",
        },
        {
            "path": "docs/acquisition/FROZEN_PARAMETER_ADJUDICATION.csv",
            "object_id": "step05-parameter-adjudication",
            "provenance_class": "DERIVED_WITH_EXACT_PROVENANCE",
            "source_identifier": "Step 05 targeted investigation",
            "adjudication": "AUTHENTIC_FROZEN_BUNDLE_INCOMPLETE",
        },
        {
            "path": "docs/acquisition/ACQUISITION_SEARCH_LOG.csv",
            "object_id": "step05-search-log",
            "provenance_class": "DERIVED_WITH_EXACT_PROVENANCE",
            "source_identifier": "Step 05 targeted investigation",
            "adjudication": "SEARCH_SCOPE_FROZEN",
        },
        {
            "path": "blocker_registry.json",
            "object_id": "step05-blocker-registry",
            "provenance_class": "DERIVED_WITH_EXACT_PROVENANCE",
            "source_identifier": "Step 05 code and adjudication",
            "adjudication": "BLOCKERS_FORMALIZED",
        },
    )


def generate(root: Path = ROOT) -> tuple[Path, ...]:
    outputs = list(generate_step04(root))

    def output(relative: str, value: object) -> Path:
        path = root / relative
        write_json(path, value)
        outputs.append(path)
        return path

    output("blocker_registry.json", blocker_registry())
    output("docs/acquisition/SOURCE_PRECEDENCE_POLICY.json", source_precedence_policy())
    output("docs/acquisition/blocker_dependency_graph.json", blocker_dependency_graph())
    dot_path = root / "docs/acquisition/blocker_dependency_graph.dot"
    dot_path.parent.mkdir(parents=True, exist_ok=True)
    dot_path.write_text(blocker_dependency_dot(), encoding="utf-8")
    outputs.append(dot_path)
    output(
        "docs/acquisition/validation_unlock_sets.json",
        {
            "minimum": minimum_validation_unlock_set(),
            "full": full_validation_unlock_set(),
        },
    )
    evaluator = FrozenLSCEvaluator.from_repository(root)
    output("frozen_core/manifests/kernel_status.json", evaluator.status.as_dict())
    output(
        "acquisition/step05_golden_status.json",
        {
            "frozen_identity": "VERIFIED",
            "frozen_specification": "READY",
            "validation_methodology": "READY",
            "statistical_engine": "READY",
            "frozen_numerical_bundle": evaluator.status.frozen_bundle_recovery_status,
            "best_collaboration_covariance": evaluator.status.best_covariance_status,
            "katrin_mapping": evaluator.status.katrin_mapping_status,
            "icecube_mapping": evaluator.status.icecube_mapping_status,
            "M3_geometry": evaluator.status.M3_geometry_status,
            "M4_hierarchical_specification": evaluator.status.M4_hierarchical_status,
            "T12_data": evaluator.status.T12_data_status,
            "minimum_validation_unlock_set": "INCOMPLETE",
            "LSC_prediction": "BLOCKED",
            "LSC_validation": "BLOCKED",
            "prediction_performed": False,
            "validation_performed": False,
            "BEST2_prediction_performed": False,
        },
    )
    output(
        "STEP_05_EVIDENCE_FREEZE.json",
        build_evidence_freeze(root, evidence_records(), acquisition_timestamp=ACQUISITION_TIMESTAMP),
    )
    return tuple(dict.fromkeys(outputs))


if __name__ == "__main__":
    for generated in generate():
        print(generated.relative_to(ROOT))
