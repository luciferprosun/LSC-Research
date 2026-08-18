"""Materialize and verify the frozen LSC 6.4.0 golden vectors."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from lsc_kernel.lsc640.evaluator import LSC640Evaluator
from lsc_kernel.lsc640.errors import LSC640Error
from lsc_kernel.lsc640.reference import NaturalSplineReference, reference_prediction


def load_golden_spec(repository_root: Path | str) -> dict[str, Any]:
    root = Path(repository_root)
    return json.loads((root / "spec/LSC_6_4_0_GOLDEN_VECTORS.json").read_text(encoding="utf-8"))


def _apply_override(payload: dict[str, Any], key: str, value: object) -> None:
    parts = key.split(".")
    target: Any = payload
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    final = parts[-1]
    if isinstance(target, list):
        target[int(final)] = value
    else:
        target[final] = value


def materialize_case(
    repository_root: Path | str,
    specification: dict[str, Any],
    case: dict[str, Any],
) -> dict[str, Any]:
    root = Path(repository_root)
    payload = copy.deepcopy(specification["templates"][case["template"]])
    source_ref = payload.pop("authoritative_line_source", None)
    factors = payload.pop("conventional_factors", None)
    if source_ref is not None:
        path_text, pointer = source_ref.split("#isotopes/", 1)
        lines_doc = json.loads((root / path_text).read_text(encoding="utf-8"))
        payload["lines"] = [{**row, **factors} for row in lines_doc["isotopes"][pointer]]
    for key, value in case.get("overrides", {}).items():
        _apply_override(payload, key, value)
    return payload


def verify_golden_vectors(repository_root: Path | str) -> dict[str, object]:
    root = Path(repository_root)
    specification = load_golden_spec(root)
    evaluator = LSC640Evaluator.from_repository(root)
    reference = NaturalSplineReference.from_csv(
        root / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv"
    )
    if specification["model_sha256"] != evaluator.cross_section.identity.model_sha256:
        raise AssertionError("Golden-vector model hash mismatch.")
    results: list[dict[str, object]] = []
    for case in specification["vectors"]:
        payload = materialize_case(root, specification, case)
        if "expected_error" in case:
            try:
                evaluator.predict(payload)
            except LSC640Error as exc:
                if exc.code != case["expected_error"]:
                    raise AssertionError(f"{case['id']}: unexpected error {exc.code}") from exc
                results.append({"id": case["id"], "status": "PASS", "error_code": exc.code})
                continue
            raise AssertionError(f"{case['id']}: expected fail-closed error was not raised")
        output = evaluator.predict(payload)
        tolerance = float(case["tolerance"])
        for field in ("mean_F_m", "R_pred"):
            if abs(float(output[field]) - float(case["expected"][field])) > tolerance:
                raise AssertionError(f"{case['id']}: {field} differs from golden value")
        mean_ref, prediction_ref = reference_prediction(reference, payload["lines"], payload["alpha_0"])
        if abs(float(output["mean_F_m"]) - mean_ref) > tolerance:
            raise AssertionError(f"{case['id']}: production/reference mean disagreement")
        if abs(float(output["R_pred"]) - prediction_ref) > tolerance:
            raise AssertionError(f"{case['id']}: production/reference prediction disagreement")
        results.append({"id": case["id"], "status": "PASS"})
    return {
        "model_sha256": specification["model_sha256"],
        "vector_count": len(results),
        "passed": len(results),
        "failed": 0,
        "results": results,
    }
