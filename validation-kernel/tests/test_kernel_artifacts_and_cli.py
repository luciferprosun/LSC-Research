from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from kernel_helpers import ROOT

from lsc_kernel.cli.main import (
    EXIT_INCOMPLETE,
    EXIT_MALFORMED_INPUT,
    EXIT_SUCCESS,
    main,
)
from lsc_kernel.io.hashes import sha256_file
from lsc_kernel.io.publication_paths import scan_publication_paths

import sys

sys.path.insert(0, str(ROOT / "tools"))
from generate_kernel_artifacts import generate  # noqa: E402
from generate_step03_artifacts import generate as generate_step03  # noqa: E402


class ArtifactTests(unittest.TestCase):
    def test_generated_artifacts_are_byte_deterministic(self) -> None:
        paths = generate(ROOT)
        first = {path.relative_to(ROOT).as_posix(): sha256_file(path) for path in paths}
        paths = generate(ROOT)
        second = {path.relative_to(ROOT).as_posix(): sha256_file(path) for path in paths}
        self.assertEqual(first, second)

    def test_kernel_status_manifest_matches_expected_boundary(self) -> None:
        status = json.loads((ROOT / "frozen_core/manifests/kernel_status.json").read_text(encoding="utf-8"))
        self.assertTrue(status["symbolic_model_ready"])
        self.assertFalse(status["numerical_model_ready"])
        self.assertFalse(status["prediction_authorized"])
        self.assertEqual(status["verdict"], "FROZEN_SPECIFICATION_KERNEL_READY_NUMERICAL_EXECUTION_BLOCKED")
        self.assertTrue(status["dataset_contracts_ready"])
        self.assertTrue(status["test_registry_ready"])
        self.assertTrue(status["preregistration_ready"])
        self.assertTrue(status["execution_harness_ready"])
        self.assertFalse(status["numerical_validation_authorized"])

    def test_step03_artifacts_are_byte_deterministic(self) -> None:
        paths = generate_step03(ROOT)
        first = {path.relative_to(ROOT).as_posix(): sha256_file(path) for path in paths}
        paths = generate_step03(ROOT)
        second = {path.relative_to(ROOT).as_posix(): sha256_file(path) for path in paths}
        self.assertEqual(first, second)

    def test_quarantine_contains_required_historical_and_conflict_objects(self) -> None:
        quarantine = json.loads(
            (ROOT / "frozen_core/manifests/HISTORICAL_ARTIFACT_QUARANTINE.json").read_text(encoding="utf-8")
        )
        ids = {item["artifact_id"] for item in quarantine["artifacts"]}
        required = {
            "postdata-toy-c0-c1",
            "postdata-lsc621-coefficients",
            "postdata-lsc55-inputs",
            "postdata-lsc55-optimized",
            "postdata-lsc60-toy",
            "postdata-lsc62-illustrative-delta",
            "postdata-lsc42-config",
            "unverified-c0-c1-to-lambda-mapping",
            "unverified-lsc55-D-to-active-A",
        }
        self.assertTrue(required <= ids)

    def test_new_step02_artifacts_contain_no_machine_local_paths(self) -> None:
        candidates = []
        for relative in ("src", "docs/kernel", "docs/policy", "docs/validation", "frozen_core", "preregistration"):
            candidates.extend(path for path in (ROOT / relative).rglob("*") if path.is_file())
        self.assertEqual(scan_publication_paths(candidates, root=ROOT), ())

    def test_path_scanner_detects_local_path_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.txt"
            path.write_text("/" + "home" + "/person/private/file\n", encoding="utf-8")
            findings = scan_publication_paths([path], root=Path(directory))
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].pattern, "POSIX_HOME")


class CliTests(unittest.TestCase):
    def test_identity_command_succeeds(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["identity"])
        self.assertEqual(code, EXIT_SUCCESS)
        self.assertEqual(json.loads(output.getvalue())["model_name"], "LSC")

    def test_can_predict_returns_incomplete_exit_code(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["can-predict"])
        self.assertEqual(code, EXIT_INCOMPLETE)
        self.assertEqual(json.loads(output.getvalue())["can_predict"], "NO")

    def test_plan_validation_is_dry_run_only(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["plan-validation", "T3"])
        result = json.loads(output.getvalue())
        self.assertEqual(code, EXIT_SUCCESS)
        self.assertTrue(result["dry_run"])
        self.assertFalse(result["LSC_prediction_performed"])
        self.assertFalse(result["validation_result_computed"])
        self.assertFalse(result["execution_manifest"]["prediction_authorized"])

    def test_malformed_bundle_returns_malformed_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("not json", encoding="utf-8")
            errors = io.StringIO()
            with contextlib.redirect_stderr(errors):
                code = main(["validate-bundle", str(path)])
            self.assertEqual(code, EXIT_MALFORMED_INPUT)
            self.assertEqual(json.loads(errors.getvalue())["error_code"], "MALFORMED_BUNDLE")


if __name__ == "__main__":
    unittest.main()
