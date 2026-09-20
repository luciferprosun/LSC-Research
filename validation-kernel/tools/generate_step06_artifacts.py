#!/usr/bin/env python3
"""Generate deterministic Step 06 decision-boundary artifacts."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from lsc_kernel.decision.boundary import (  # noqa: E402
    STEP06_VERDICT,
    allowed_claim_records,
    publication_boundary,
    recoverability_decision,
    step07_input_contract,
)
from lsc_kernel.frozen.evaluator import FrozenLSCEvaluator  # noqa: E402
from lsc_kernel.io.hashes import sha256_file  # noqa: E402
from lsc_kernel.io.manifests import write_json  # noqa: E402
from tools.generate_step05_artifacts import generate as generate_step05  # noqa: E402


def _write_claims_csv(path: Path) -> None:
    rows = [record.as_dict() for record in allowed_claim_records()]
    fieldnames = ["claim", "status", "reason", "evidence", "allowed_in_publication"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})


def generate(root: Path = ROOT) -> tuple[Path, ...]:
    outputs = list(generate_step05(root))

    def output(relative: str, value: object) -> Path:
        path = root / relative
        write_json(path, value)
        outputs.append(path)
        return path

    boundary_path = output("publication_boundary.json", publication_boundary())
    output(
        "STEP_07_INPUT_CONTRACT.json",
        step07_input_contract(
            publication_boundary_sha256=sha256_file(boundary_path),
            parameter_bundle_schema_sha256=sha256_file(
                root / "frozen_core/parameters/frozen_parameter_bundle.schema.json"
            ),
        ),
    )
    claims_path = root / "docs/decision/LSC_6_3_0_ALLOWED_CLAIMS.csv"
    _write_claims_csv(claims_path)
    outputs.append(claims_path)

    evaluator = FrozenLSCEvaluator.from_repository(root)
    output("frozen_core/manifests/kernel_status.json", evaluator.status.as_dict())
    decision = recoverability_decision()
    output(
        "decision/step06_golden_status.json",
        {
            "frozen_6_3_0_identity": "PRESERVED",
            "identity_recoverability": decision["identity_recoverability"],
            "symbolic_recoverability": decision["symbolic_recoverability"],
            "numerical_recoverability": decision["numerical_recoverability"],
            "6_3_0_numerical_validation": "NOT_AUTHORIZED",
            "6_3_0_historical_record": "PRESERVED",
            "successor_boundary": "DEFINED",
            "6_3_1_executable_specification": "NOT_YET_CREATED",
            "historical_data": "RETROSPECTIVE_NON_BLIND",
            "BEST2": "FUTURE_BLIND",
            "publication": "NOT_AUTHORIZED",
            "decision_verdict": STEP06_VERDICT,
            "LSC_fit_performed": False,
            "LSC_prediction_performed": False,
            "LSC_validation_performed": False,
            "BEST2_prediction_performed": False,
        },
    )
    return tuple(dict.fromkeys(outputs))


if __name__ == "__main__":
    for generated in generate():
        print(generated.relative_to(ROOT))
