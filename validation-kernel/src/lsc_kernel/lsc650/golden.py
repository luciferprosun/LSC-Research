"""Materialize and verify frozen LSC 6.5.0 golden vectors."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from lsc_kernel.lsc650.evaluator import LSC650Evaluator
from lsc_kernel.lsc650.errors import LSC650Error
from lsc_kernel.lsc650.reference import NaturalSplineReference650, reference_exact_prediction


def load_golden_spec(repository_root: Path | str) -> dict[str, Any]:
    return json.loads((Path(repository_root) / "spec/LSC_6_5_0_GOLDEN_VECTORS.json").read_text(encoding="utf-8"))


def _apply_override(payload: dict[str, Any], key: str, value: object) -> None:
    target: Any = payload
    parts = key.split(".")
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    final = parts[-1]
    if isinstance(target, list):
        target[int(final)] = value
    else:
        target[final] = value


def materialize_case(repository_root: Path | str, specification: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
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
    evaluator = LSC650Evaluator.from_repository(root)
    reference = NaturalSplineReference650.from_csv(root / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv")
    results: list[dict[str, object]] = []
    for case in specification["vectors"]:
        payload = materialize_case(root, specification, case)
        if "expected_error" in case:
            try:
                evaluator.predict(payload)
            except LSC650Error as exc:
                if exc.code != case["expected_error"]:
                    raise AssertionError(f"{case['id']}: unexpected error {exc.code}") from exc
                results.append({"id": case["id"], "status": "PASS", "error_code": exc.code})
                continue
            raise AssertionError(f"{case['id']}: expected fail-closed error was not raised")
        output = evaluator.predict(payload)
        reference_output = reference_exact_prediction(reference, payload["lines"], payload["alpha_0"])
        tolerance = float(case["tolerance"])
        for field in ("baseline_denominator", "exact_numerator", "R_pred"):
            if abs(float(output[field]) - float(case["expected"][field])) > tolerance:
                raise AssertionError(f"{case['id']}: {field} differs from its frozen golden value")
            if abs(float(output[field]) - float(reference_output[field])) > tolerance:
                raise AssertionError(f"{case['id']}: production/reference {field} disagreement")
        expected_k = case["expected"].get("per_line_K_m")
        if expected_k is not None:
            actual_k = [float(row["K_m"]) for row in output["per_line"]]
            reference_k = [float(row["K_m"]) for row in reference_output["per_line"]]
            if len(actual_k) != len(expected_k):
                raise AssertionError(f"{case['id']}: per-line count differs")
            for actual, frozen, independent in zip(actual_k, expected_k, reference_k, strict=True):
                if abs(actual - float(frozen)) > tolerance or abs(actual - independent) > tolerance:
                    raise AssertionError(f"{case['id']}: per-line kernel disagreement")
        results.append({"id": case["id"], "status": "PASS"})
    return {
        "model_version": "6.5.0",
        "scientific_freeze_sha256": evaluator.cross_section.identity.scientific_freeze_sha256,
        "vector_count": len(results),
        "passed": len(results),
        "failed": 0,
        "results": results,
    }
