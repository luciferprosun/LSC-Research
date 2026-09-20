"""Minimal machine-readable CLI for the fail-closed kernel."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from lsc_kernel.errors import (
    FrozenFrameUnknown,
    FrozenIdentityMismatch,
    FrozenOrientationMissing,
    FrozenParameterMissing,
    FrozenParameterProvenanceError,
    FrozenSpecificationBlocker,
    FrozenTensorIncomplete,
    FrozenUnitUnknown,
    MalformedBundle,
    PostDataArtifactRejected,
    UnverifiedCandidateRejected,
)
from lsc_kernel.frozen.equations import equation_descriptors
from lsc_kernel.frozen.evaluator import FrozenLSCEvaluator
from lsc_kernel.frozen.identity import FrozenModelIdentity
from lsc_kernel.frozen.parameter_bundle import FrozenParameterBundle
from lsc_kernel.validation.execution import DryRunValidationHarness
from lsc_kernel.validation.policies import FROZEN_LSC_MODEL_IDS
from lsc_kernel.statistics.baselines import assert_baseline_execution_authorized


EXIT_SUCCESS = 0
EXIT_INCOMPLETE = 2
EXIT_PROVENANCE_REJECTION = 3
EXIT_MALFORMED_INPUT = 4


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _print_json(value: Any, *, stream: Any | None = None) -> None:
    print(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False), file=stream or sys.stdout)


def _error_exit(error: FrozenSpecificationBlocker) -> int:
    _print_json(error.as_dict(), stream=sys.stderr)
    if isinstance(error, (PostDataArtifactRejected, UnverifiedCandidateRejected, FrozenParameterProvenanceError)):
        return EXIT_PROVENANCE_REJECTION
    if isinstance(error, (MalformedBundle, FrozenIdentityMismatch, FrozenTensorIncomplete)):
        return EXIT_MALFORMED_INPUT
    if isinstance(error, (FrozenParameterMissing, FrozenUnitUnknown, FrozenFrameUnknown, FrozenOrientationMissing)):
        return EXIT_INCOMPLETE
    return EXIT_INCOMPLETE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lsc-kernel")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("identity", help="Print immutable frozen identity JSON")
    subparsers.add_parser("status", help="Print machine-readable kernel status")
    subparsers.add_parser("missing", help="List required missing frozen objects")
    subparsers.add_parser("equations", help="Print E1-E12 descriptors")
    validate = subparsers.add_parser("validate-bundle", help="Validate a FrozenParameterBundle JSON file")
    validate.add_argument("file", type=Path)
    subparsers.add_parser("can-predict", help="Report whether numerical LSC prediction is authorized")
    plan = subparsers.add_parser("plan-validation", help="Create a dry-run validation plan without prediction")
    plan.add_argument("test_id", choices=[f"T{i}" for i in range(1, 13)])
    plan.add_argument("--split-id")
    plan.add_argument("--covariance-scenario")
    run = subparsers.add_parser(
        "run-validation",
        help="Policy gate for a validation execution; frozen LSC remains blocked",
    )
    run.add_argument("test_id", choices=[f"T{i}" for i in range(1, 13)])
    run.add_argument("--model", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        evaluator = FrozenLSCEvaluator.from_repository(_repository_root())
        if args.command == "identity":
            _print_json(FrozenModelIdentity.canonical().as_dict())
            return EXIT_SUCCESS
        if args.command == "status":
            _print_json(evaluator.status.as_dict())
            return EXIT_SUCCESS
        if args.command == "missing":
            blockers = [definition.as_dict() for definition in evaluator.schema.numerical_blockers]
            _print_json({"count": len(blockers), "missing": blockers})
            return EXIT_SUCCESS
        if args.command == "equations":
            _print_json({"equations": [equation.as_dict() for equation in equation_descriptors()]})
            return EXIT_SUCCESS
        if args.command == "validate-bundle":
            bundle = evaluator.validate_bundle(FrozenParameterBundle.load(args.file))
            _print_json({"valid": True, "bundle_sha256": bundle.bundle_sha256})
            return EXIT_SUCCESS
        if args.command == "can-predict":
            authorized, blockers = evaluator.can_predict()
            _print_json(
                {
                    "can_predict": "YES" if authorized else "NO",
                    "prediction_authorized": authorized,
                    "blockers": list(blockers),
                }
            )
            return EXIT_SUCCESS if authorized else EXIT_INCOMPLETE
        if args.command == "plan-validation":
            harness = DryRunValidationHarness(_repository_root())
            _print_json(
                harness.plan(
                    args.test_id,
                    split_id=args.split_id,
                    covariance_scenario=args.covariance_scenario,
                )
            )
            return EXIT_SUCCESS
        if args.command == "run-validation":
            model = args.model.upper()
            if model in FROZEN_LSC_MODEL_IDS:
                evaluator.authorize_validation(args.test_id, context={}, bundle=None)
            canonical = assert_baseline_execution_authorized(model)
            _print_json(
                {
                    "test_id": args.test_id,
                    "model": canonical,
                    "LSC_used": False,
                    "authorization": "BASELINE_POLICY_ACCEPTED",
                    "execution": "NOT_RUN_INPUT_EXECUTION_MANIFEST_REQUIRED",
                    "note": "Use the programmatic baseline engine with a validated dataset and execution manifest.",
                }
            )
            return EXIT_SUCCESS
    except FrozenSpecificationBlocker as error:
        return _error_exit(error)
    return EXIT_MALFORMED_INPUT


if __name__ == "__main__":
    raise SystemExit(main())
