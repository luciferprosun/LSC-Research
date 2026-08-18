"""External constraint loaders and mandatory mapping contracts."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping

import numpy as np

from lsc_kernel.errors import ExternalVetoBlockedMappingMissing
from lsc_kernel.io.hashes import sha256_file


@dataclass(frozen=True, slots=True)
class ExternalConstraintMapping:
    constraint_id: str
    lsc_parameter_or_observable: str | None
    external_parameter_space: tuple[str, ...]
    mapping_equations: tuple[str, ...]
    mapping_provenance: str | None
    confidence_construction: str
    authorized: bool = False

    def assert_authorized(self) -> None:
        if not self.authorized or not self.lsc_parameter_or_observable or not self.mapping_equations or not self.mapping_provenance:
            raise ExternalVetoBlockedMappingMissing(
                "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING",
                details={"constraint_id": self.constraint_id},
            )

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["readiness_state"] = "READY_EXTERNAL" if self.authorized else "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING"
        return result


def canonical_external_mappings() -> tuple[ExternalConstraintMapping, ...]:
    return (
        ExternalConstraintMapping(
            "KATRIN", None, ("mnu2sterile", "sin2thetaee"), (), None,
            "Release-native absolute chi-square grid; no inferred Wilks coverage.", False,
        ),
        ExternalConstraintMapping(
            "ICECUBE", None, ("release-defined sterile parameter space",), (), None,
            "Release-native confidence/metric construction must be retained.", False,
        ),
    )


def load_and_validate_katrin_grid(root: Path) -> dict[str, object]:
    path = root / "LSC_6_3_0_VALIDATION/06_KATRIN/records/19369714/files/Main_result_KNM1to5_chi_square_map.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    masses = value.get("mnu2sterile")
    mixing = value.get("sin2thetaee")
    matrix = value.get("chiSquareMatrix")
    valid = (
        isinstance(masses, list) and len(masses) == 50
        and isinstance(mixing, list) and len(mixing) == 50
        and isinstance(matrix, list) and len(matrix) == 50
        and all(isinstance(row, list) and len(row) == 50 for row in matrix)
        and all(math.isfinite(float(cell)) for row in matrix for cell in row)
    )
    if not valid:
        raise ValueError("KATRIN public grid does not satisfy the frozen 50x50 contract.")
    return {
        "constraint_id": "KATRIN",
        "shape": [50, 50],
        "grid_kind": "ABSOLUTE_CHI_SQUARE",
        "finite_minimum": min(float(cell) for row in matrix for cell in row),
        "mapping_state": "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING",
    }


def load_and_validate_icecube_release_index(root: Path) -> dict[str, object]:
    path = root / "LSC_6_3_0_VALIDATION/07_ICECUBE/ICECUBE_FILE_INTEGRITY.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))
    if len(rows) != 52:
        raise ValueError("IceCube release index row count differs from the archived contract.")
    required = {
        "dataset", "doi", "local_path", "local_size_bytes", "size_status",
        "sha256_local", "license", "retrieval_status",
    }
    if any(not required <= set(row) for row in rows):
        raise ValueError("IceCube release index is missing required provenance columns.")
    archive_root = (root / "LSC_6_3_0_VALIDATION").resolve()
    indexed_paths: dict[str, tuple[Path, dict[str, str]]] = {}
    for row in rows:
        relative = str(row["local_path"])
        candidate = (archive_root / relative).resolve()
        if not candidate.is_relative_to(archive_root) or not candidate.is_file():
            raise ValueError(f"IceCube indexed path is missing or escapes the archive: {relative}")
        if candidate.stat().st_size != int(row["local_size_bytes"]) or row["size_status"] != "PASS":
            raise ValueError(f"IceCube size contract failed for {relative}")
        digest = row["sha256_local"].lower()
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise ValueError(f"IceCube SHA-256 field is malformed for {relative}")
        indexed_paths[relative] = (candidate, row)

    numerical_contracts = {
        "07_ICECUBE/DeepCore_7p5y_sterile/data/oscnext_sterile_sensitivity_90pct.csv": (59, 2, 1),
        "07_ICECUBE/DeepCore_7p5y_sterile/data/marginalized_umu4_sq.csv": (500, 2, 1),
        "07_ICECUBE/DeepCore_7p5y_sterile/data/marginalized_utau4_sq.csv": (500, 2, 1),
        "07_ICECUBE/DeepCore_7p5y_sterile/data/real_data_wilks_contours_reprod_mar_2025_metric_diff.csv": (420, 3, 1),
        "07_ICECUBE/DeepCore_7p5y_sterile/data/wilks_contour_90pct.csv": (54, 2, 1),
        "07_ICECUBE/Upgrade_oscillation_potential/data/modchi2map_icecube.csv": (121, 3, 0),
        "07_ICECUBE/Upgrade_oscillation_potential/data/modchi2map_nufitwSK.csv": (121, 3, 0),
        "07_ICECUBE/Upgrade_oscillation_potential/data/modchi2map_nufitwoSK.csv": (121, 3, 0),
    }
    numerical_objects: dict[str, object] = {}
    for relative, (rows_expected, columns_expected, skip_header) in numerical_contracts.items():
        if relative not in indexed_paths:
            raise ValueError(f"IceCube numerical object is absent from the integrity index: {relative}")
        candidate, row = indexed_paths[relative]
        digest = sha256_file(candidate)
        if digest != row["sha256_local"]:
            raise ValueError(f"IceCube local SHA-256 mismatch for {relative}")
        values = np.loadtxt(candidate, delimiter=",", comments="#", skiprows=skip_header, dtype=np.float64)
        if values.shape != (rows_expected, columns_expected) or not np.isfinite(values).all():
            raise ValueError(f"IceCube numerical object failed shape/finite contract: {relative}")
        numerical_objects[relative] = {
            "shape": [rows_expected, columns_expected],
            "finite": True,
            "sha256": digest,
        }

    releases = sorted({row["dataset"] for row in rows})
    dois_by_release = {
        release: sorted({row["doi"] for row in rows if row["dataset"] == release})
        for release in releases
    }
    if any(len(dois) != 1 or not dois[0].startswith("10.7910/DVN/") for dois in dois_by_release.values()):
        raise ValueError("IceCube release-to-DOI mapping is inconsistent.")
    return {
        "constraint_id": "ICECUBE",
        "classification": "STATISTICAL_ENGINE_CONTROL",
        "index_sha256": sha256_file(path),
        "file_records": len(rows),
        "release_identities": releases,
        "dois_by_release": dois_by_release,
        "all_indexed_files_exist": True,
        "all_indexed_sizes_match": True,
        "numerical_objects": numerical_objects,
        "numerical_objects_validated": len(numerical_objects),
        "release_loading_ready": True,
        "mapping_state": "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING",
    }


def assert_external_veto_authorized(constraint_id: str, mappings: Mapping[str, ExternalConstraintMapping] | None = None) -> None:
    mapping_by_id = mappings or {item.constraint_id: item for item in canonical_external_mappings()}
    if constraint_id not in mapping_by_id:
        raise ExternalVetoBlockedMappingMissing("Unknown external constraint mapping.", details={"constraint_id": constraint_id})
    mapping_by_id[constraint_id].assert_authorized()
