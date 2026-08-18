#!/usr/bin/env python3
"""Read-only, deterministic reproduction of LSC 6.5.0 RC1."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "src"))

from scipy.optimize import brentq, minimize_scalar  # noqa: E402

from lsc_kernel.lsc650.cross_section import canonical_hash, sha256_file  # noqa: E402
from lsc_kernel.lsc650.golden import verify_golden_vectors  # noqa: E402
from lsc_kernel.lsc650.reference import NaturalSplineReference650, reference_exact_prediction  # noqa: E402


COMPONENT_PATHS = {
    "scientific_specification_sha256": "spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml",
    "scientific_freeze_sha256": "LSC_6_5_0_SCIENTIFIC_FREEZE.json",
    "owner_authorization_sha256": "OWNER_AUTHORIZATION_LSC_6_5_0.md",
    "cross_section_payload_sha256": "external_physics/gallium_capture/bahcall_1997_best_estimate.csv",
    "source_line_payload_sha256": "external_physics/gallium_capture/source_lines_prc108_035502.json",
    "parameter_bundle_sha256": "LSC_6_5_0_PARAMETER_BUNDLE.json",
    "parameter_bundle_schema_sha256": "spec/LSC_6_5_0_PARAMETER_BUNDLE.schema.json",
    "evaluator_source_sha256": "src/lsc_kernel/lsc650/evaluator.py",
    "cross_section_source_sha256": "src/lsc_kernel/lsc650/cross_section.py",
    "contracts_source_sha256": "src/lsc_kernel/lsc650/contracts.py",
    "prediction_input_schema_sha256": "spec/LSC_6_5_0_PREDICTION_INPUT.schema.json",
    "prediction_output_schema_sha256": "spec/LSC_6_5_0_PREDICTION_OUTPUT.schema.json",
    "golden_vectors_sha256": "spec/LSC_6_5_0_GOLDEN_VECTORS.json",
    "environment_lock_sha256": "LSC_6_5_0_ENVIRONMENT_LOCK.json",
}


def load_json(relative: str) -> dict[str, object]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def verify_identity() -> dict[str, object]:
    identity = load_json("LSC_6_5_0_MODEL_IDENTITY.json")
    actual = {key: sha256_file(ROOT / path) for key, path in COMPONENT_PATHS.items()}
    if actual != identity["components"]:
        raise AssertionError("Model-identity component mismatch.")
    model_hash = canonical_hash({"model_version": "6.5.0", "configuration": "EXACT_FINITE_A2/C/A", "components": actual})
    if model_hash != identity["model_sha256"] or (ROOT / "LSC_6_5_0_MODEL_SHA256").read_text().strip() != model_hash:
        raise AssertionError("Canonical model hash mismatch.")
    return {"model_sha256": model_hash, "parameter_bundle_sha256": actual["parameter_bundle_sha256"]}


def independent_parameter_reproduction() -> dict[str, object]:
    protocol = load_json("LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json")
    frozen = load_json("LSC_6_5_0_ALPHA_DETERMINATION_RESULT.json")
    bundle = load_json("LSC_6_5_0_PARAMETER_BUNDLE.json")
    lines_doc = load_json("external_physics/gallium_capture/source_lines_prc108_035502.json")
    factors = {"source_activity_bq": 1.0, "exposure_seconds": 1.0, "conventional_probability": 1.0, "geometry_factor": 1.0, "detector_efficiency": 1.0}
    lines = [{**row, **factors} for row in lines_doc["isotopes"]["Cr51"]]
    spline = NaturalSplineReference650.from_csv(ROOT / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv")
    observed = float(protocol["development_data"]["observed_values"][0])
    uncertainty = float(protocol["development_data"]["standard_uncertainties"][0])
    lower, upper = (float(value) for value in protocol["bounds"]["fit_bound"])

    def objective(alpha: float) -> float:
        predicted = float(reference_exact_prediction(spline, lines, alpha)["R_pred"])
        return ((observed - predicted) / uncertainty) ** 2

    options = protocol["optimizer"]
    fit = minimize_scalar(objective, bounds=(lower, upper), method="bounded", options={"xatol": float(options["xatol"]), "maxiter": int(options["maxiter"])})
    target = float(fit.fun) + 1.0
    interval = [
        float(brentq(lambda value: objective(value) - target, lower, float(fit.x), xtol=1e-13, rtol=1e-14, maxiter=1000)),
        float(brentq(lambda value: objective(value) - target, float(fit.x), upper, xtol=1e-13, rtol=1e-14, maxiter=1000)),
    ]
    if not fit.success or abs(float(fit.x) - float(frozen["alpha_0_estimate"])) > 5e-12:
        raise AssertionError("Independent alpha_0 estimate does not reproduce.")
    frozen_interval = [float(value) for value in frozen["certified_profile_delta_chi_square_1_interval"]]
    if any(abs(a - b) > 5e-12 for a, b in zip(interval, frozen_interval, strict=True)):
        raise AssertionError("Independent alpha_0 interval does not reproduce.")
    if float(bundle["parameter"]["value"]) != float(frozen["alpha_0_estimate"]) or bundle["no_refit"] is not True:
        raise AssertionError("Frozen parameter bundle does not match the completed determination.")
    return {
        "status": "PASS",
        "alpha_0": float(frozen["alpha_0_estimate"]),
        "interval": frozen_interval,
        "boundary_status": frozen["boundary_status"],
        "identifiability": frozen["identifiability"],
        "completed_determination_count": 1,
        "write_or_refit_performed": False,
    }


def verify_sha256s() -> str:
    sums = ROOT / "SHA256SUMS.txt"
    if not sums.is_file():
        return "NOT_APPLICABLE_REPOSITORY_PROFILE"
    for line in sums.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        if sha256_file(ROOT / relative) != expected:
            raise AssertionError(f"RC SHA-256 mismatch: {relative}")
    return "PASS"


def main() -> int:
    identity = verify_identity()
    golden = verify_golden_vectors(ROOT)
    determination = independent_parameter_reproduction()
    adverse = load_json("LSC_6_4_0_ADVERSE_RESULT_FREEZE.json")
    if adverse["status"] != "DEVELOPMENT_PARAMETER_DETERMINATION_FAILED_IMMUTABLE":
        raise AssertionError("LSC 6.4.0 adverse-result freeze is not preserved.")
    test_status = "NOT_INCLUDED_RELEASE_PROFILE"
    if (ROOT / "tests/test_step08_phase1_closure.py").is_file():
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "tests/test_step08_phase1_closure.py"],
            cwd=ROOT,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError("Dedicated LSC 6.5.0 software tests failed.")
        test_status = "PASS"
    receipt = {
        "status": "PASS",
        "model_sha256": identity["model_sha256"],
        "parameter_bundle_sha256": identity["parameter_bundle_sha256"],
        "cross_section_payload_sha256": sha256_file(ROOT / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv"),
        "golden_vectors": {"passed": golden["passed"], "failed": golden["failed"]},
        "independent_parameter_reproduction": determination,
        "dedicated_tests": test_status,
        "rc_sha256s": verify_sha256s(),
        "6_4_0_adverse_result": "PRESERVED",
        "BEST2_observed_data_accessed": False,
        "BEST2_prediction_generated": False,
        "publication_performed": False,
    }
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
