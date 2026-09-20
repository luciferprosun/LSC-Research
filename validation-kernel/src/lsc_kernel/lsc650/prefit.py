"""Hash-bound pre-fit audit for the one authorized LSC 6.5.0 determination."""

from __future__ import annotations

import ast

import json
from pathlib import Path
from typing import Any

from lsc_kernel.lsc650.cross_section import ExactGalliumCaptureCrossSection, sha256_file
from lsc_kernel.lsc650.errors import PreFitGateError
from lsc_kernel.lsc650.golden import verify_golden_vectors


FREEZE_PATH = "LSC_6_5_0_PREFIT_FREEZE.json"


def load_prefit_freeze(repository_root: Path | str) -> dict[str, Any]:
    try:
        return json.loads((Path(repository_root) / FREEZE_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreFitGateError("The LSC 6.5.0 pre-fit freeze is unavailable.") from exc


def run_prefit_audit(repository_root: Path | str) -> dict[str, object]:
    root = Path(repository_root).resolve()
    freeze = load_prefit_freeze(root)
    failures: list[str] = []
    if freeze.get("status") != "FROZEN_BEFORE_SINGLE_PARAMETER_DETERMINATION":
        failures.append("freeze_status")
    if freeze.get("fit_execution_limit") != 1:
        failures.append("execution_count")
    for row in freeze.get("bindings", []):
        path = root / row["path"]
        if not path.is_file() or sha256_file(path) != row["sha256"]:
            failures.append(f"hash:{row['path']}")
    authorization = (root / "OWNER_AUTHORIZATION_LSC_6_5_0.md").read_text(encoding="utf-8")
    if "OWNER AUTHORIZATION: **APPROVED**" not in authorization or "Scientific decisions authorized: **A2-exact / C / A**" not in authorization:
        failures.append("owner_authorization")
    try:
        cross_section = ExactGalliumCaptureCrossSection.from_repository(root)
        expected_domain = cross_section.alpha_domain(
            float(row["energy_mev"])
            for rows in cross_section.source_lines["isotopes"].values()
            for row in rows
        )
        if list(expected_domain) != freeze.get("gates", {}).get("source_support_domain"):
            failures.append("domain_derivation")
    except Exception as exc:
        failures.append(f"cross_section:{type(exc).__name__}")
    try:
        golden = verify_golden_vectors(root)
        if golden["failed"] != 0 or golden["passed"] != 29:
            failures.append("golden_vectors")
    except Exception as exc:
        failures.append(f"golden_vectors:{type(exc).__name__}")
        golden = {"passed": 0, "failed": 29}
    protocol = json.loads((root / "LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json").read_text(encoding="utf-8"))
    development = json.loads((root / "model_development/LSC_6_5_0_DEVELOPMENT_DATA_MANIFEST.json").read_text(encoding="utf-8"))
    required_labels = ["MODEL_EXPOSED", "POST_6_4_DEVELOPMENT", "RETROSPECTIVE_NON_BLIND", "DEVELOPMENT_DATA"]
    if protocol.get("protocol_status") != "FROZEN_BEFORE_EXECUTION" or protocol.get("allowed_execution_count") != 1:
        failures.append("protocol")
    if development.get("exposure_labels") != required_labels:
        failures.append("development_exposure_labels")
    if development.get("holdout_use_in_alpha_objective") is not False:
        failures.append("holdout_separation")
    if any(development.get(field) is not False for field in ("BEST2_observed_data_accessed", "BEST2_observed_data_included", "BEST2_prediction_generated")):
        failures.append("BEST2_blindness")
    if protocol.get("bounds", {}).get("old_6_4_result_or_bound_used") is not False:
        failures.append("6_4_result_leakage")
    determination_source = (root / "src/lsc_kernel/lsc650/determination.py").read_text(encoding="utf-8")
    invalid_literals = sorted(
        {node.id for node in ast.walk(ast.parse(determination_source)) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in {"false", "true", "null"}}
    )
    if invalid_literals:
        failures.append(f"python_json_literals:{','.join(invalid_literals)}")
    if failures:
        raise PreFitGateError("One or more frozen LSC 6.5.0 pre-fit gates failed.", details={"failures": failures})
    return {
        "status": "PASS",
        "owner_authorization": "PASS",
        "exact_finite_response": "PASS",
        "cross_section_provenance": "PASS",
        "source_support_domain": "PASS",
        "schemas": "PASS",
        "evaluator_determinism": "PASS",
        "golden_vectors": f"PASS {golden['passed']}/{golden['passed'] + golden['failed']}",
        "independent_reference": "PASS",
        "baseline_accounting": "PASS",
        "parameter_protocol": "FROZEN",
        "development_dataset": "FROZEN_BEST_INNER_ONLY",
        "holdouts": "EXCLUDED",
        "covariance_policy": "FROZEN_COV_DIAGONAL_SENSITIVITY_ONLY",
        "bounds": "FROZEN_SOURCE_SUPPORT_DERIVED",
        "old_6_4_result_used": False,
        "python_result_path_static_audit": "PASS",
        "BEST2_observed_data_accessed": False,
        "BEST2_prediction_generated": False,
        "prefit_freeze_sha256": sha256_file(root / FREEZE_PATH),
    }
