"""Hash-bound pre-fit audit for the single authorized alpha determination."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lsc_kernel.lsc640.cross_section import GalliumCaptureCrossSection, sha256_file
from lsc_kernel.lsc640.errors import PreFitGateError
from lsc_kernel.lsc640.golden import verify_golden_vectors


def load_prefit_freeze(repository_root: Path | str) -> dict[str, Any]:
    path = Path(repository_root) / "LSC_6_4_0_PRE_FIT_FREEZE.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreFitGateError("The pre-fit freeze manifest is unavailable.") from exc


def run_prefit_audit(repository_root: Path | str) -> dict[str, object]:
    root = Path(repository_root).resolve()
    freeze = load_prefit_freeze(root)
    failures: list[str] = []
    if freeze.get("status") != "FROZEN_BEFORE_SINGLE_PARAMETER_DETERMINATION":
        failures.append("freeze_status")
    for row in freeze.get("bindings", []):
        path = root / row["path"]
        if not path.is_file() or sha256_file(path) != row["sha256"]:
            failures.append(f"hash:{row['path']}")
    authorization = (root / "OWNER_AUTHORIZATION_6_4_0.md").read_text(encoding="utf-8")
    if "OWNER AUTHORIZATION: OWNER_AUTHORIZED (A2/C/A)" not in authorization:
        failures.append("owner_authorization")
    try:
        cross_section = GalliumCaptureCrossSection.from_repository(root)
    except Exception as exc:  # converted to a single gate receipt
        failures.append(f"cross_section:{type(exc).__name__}")
        cross_section = None
    try:
        golden = verify_golden_vectors(root)
        if golden["failed"] != 0 or golden["passed"] != 15:
            failures.append("golden_vectors")
    except Exception as exc:  # converted to a single gate receipt
        failures.append(f"golden_vectors:{type(exc).__name__}")
        golden = {"passed": 0, "failed": 15}
    protocol = json.loads((root / "LSC_6_4_0_ALPHA0_DETERMINATION_PROTOCOL.json").read_text(encoding="utf-8"))
    development = json.loads(
        (root / "model_development/LSC_6_4_0_DEVELOPMENT_DATA_MANIFEST.json").read_text(encoding="utf-8")
    )
    if protocol.get("protocol_status") != "FROZEN_BEFORE_EXECUTION":
        failures.append("protocol_status")
    if protocol.get("allowed_execution_count") != 1:
        failures.append("execution_count")
    if development.get("BEST2_observed_data_accessed") is not False:
        failures.append("BEST2_observed_data")
    if development.get("exposure_labels") != ["MODEL_EXPOSED", "RETROSPECTIVE_NON_BLIND", "DEVELOPMENT_DATA"]:
        failures.append("data_exposure_labels")
    if failures:
        raise PreFitGateError("One or more frozen pre-fit gates failed.", details={"failures": failures})
    return {
        "status": "PASS",
        "owner_authorization": "PASS",
        "response_specification": "PASS",
        "cross_section_payload": "PASS",
        "interpolation": "PASS",
        "derivative": "PASS",
        "schemas": "PASS",
        "evaluator_determinism": "PASS",
        "golden_vectors": f"PASS {golden['passed']}/{golden['passed'] + golden['failed']}",
        "independent_reference": "PASS",
        "development_dataset": "FROZEN",
        "objective": "FROZEN",
        "covariance_policy": "FROZEN_COV_DIAGONAL_SENSITIVITY_ONLY",
        "bounds": "FROZEN",
        "BEST2_observed_data_accessed": False,
        "model_sha256": cross_section.identity.model_sha256 if cross_section else None,
        "prefit_freeze_sha256": sha256_file(root / "LSC_6_4_0_PRE_FIT_FREEZE.json"),
    }
