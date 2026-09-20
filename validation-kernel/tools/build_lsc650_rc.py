#!/usr/bin/env python3
"""Deterministically package the publication-safe LSC 6.5.0 RC1 directory."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "release_candidate/LSC-6.5.0-rc1"


FILES = [
    "OWNER_AUTHORIZATION_LSC_6_5_0.md",
    "LSC_6_5_0_IMPLEMENTATION_CONTRACT.json",
    "LSC_6_5_0_SCIENTIFIC_FREEZE.json",
    "LSC_6_5_0_PREFIT_FREEZE.json",
    "LSC_6_5_0_PREFIT_FREEZE_R1_ABORTED.json",
    "LSC_6_5_0_PREFIT_FREEZE_R2_ABORTED.json",
    "LSC_6_5_0_PREFIT_EXECUTION_INCIDENT.json",
    "LSC_6_5_0_PREFIT_EXECUTION_INCIDENT_R2.json",
    "LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json",
    "LSC_6_5_0_ALPHA_DETERMINATION_RESULT.json",
    "LSC_6_5_0_PARAMETER_BUNDLE.json",
    "LSC_6_5_0_MODEL_IDENTITY.json",
    "LSC_6_5_0_MODEL_SHA256",
    "LSC_6_5_0_RETROSPECTIVE_SMOKE_REPORT.json",
    "LSC_6_5_0_ENVIRONMENT_LOCK.json",
    "LSC_6_5_0_DEVELOPMENT_DISCLOSURE.md",
    "LSC_6_4_0_ADVERSE_RESULT_FREEZE.json",
    "docs/scientific/LSC_6_4_0_ADVERSE_RESULT_RECORD.md",
    "docs/model/LSC_6_5_0_NUMERICAL_STABILITY_REPORT.md",
    "docs/model/LSC_6_5_0_REPRODUCTION_INSTRUCTIONS.md",
    "docs/model/LSC_6_5_0_REPRODUCIBILITY_REPORT.md",
    "docs/model/LSC_6_5_0_ALLOWED_CLAIMS.csv",
    "spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml",
    "spec/LSC_6_5_0_PREDICTION_INPUT.schema.json",
    "spec/LSC_6_5_0_PREDICTION_OUTPUT.schema.json",
    "spec/LSC_6_5_0_PARAMETER_BUNDLE.schema.json",
    "spec/LSC_6_5_0_GOLDEN_VECTORS.json",
    "external_physics/gallium_capture/bahcall_1997_best_estimate.csv",
    "external_physics/gallium_capture/source_lines_prc108_035502.json",
    "external_physics/gallium_capture/INTERPOLATION_POLICY.md",
    "model_development/LSC_6_5_0_DEVELOPMENT_DATA_MANIFEST.json",
    "preregistration/splits.json",
    "preregistration/covariance_scenarios.json",
    "preregistration/nuisance_registry.json",
    "requirements-step07e.lock",
    "pyproject.toml",
    "src/lsc_kernel/lsc650/__init__.py",
    "src/lsc_kernel/lsc650/errors.py",
    "src/lsc_kernel/lsc650/cross_section.py",
    "src/lsc_kernel/lsc650/contracts.py",
    "src/lsc_kernel/lsc650/evaluator.py",
    "src/lsc_kernel/lsc650/reference.py",
    "src/lsc_kernel/lsc650/golden.py",
    "src/lsc_kernel/lsc650/prefit.py",
    "src/lsc_kernel/lsc650/determination.py",
    "tools/reproduce_lsc650.py",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=False, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8")


def write_manifests(target: Path) -> None:
    for stale in (target / "MANIFEST.json", target / "SHA256SUMS.txt"):
        if stale.exists():
            stale.unlink()
    manifest_rows = []
    for path in sorted(item for item in target.rglob("*") if item.is_file()):
        relative = path.relative_to(target).as_posix()
        manifest_rows.append({
            "path": relative,
            "role": "release execution/evidence",
            "sha256": digest(path),
            "size": path.stat().st_size,
            "source": "repository" if relative != "external_physics/gallium_capture/PROVENANCE_MANIFEST.json" else "generated publication-safe execution manifest",
            "generated": relative in {"external_physics/gallium_capture/PROVENANCE_MANIFEST.json", "src/lsc_kernel/__init__.py"},
            "required_for_execution": relative.startswith(("src/", "spec/", "external_physics/")) or relative in {"LSC_6_5_0_PARAMETER_BUNDLE.json", "LSC_6_5_0_MODEL_IDENTITY.json"},
        })
    write_json(target / "MANIFEST.json", {"schema_version": "1.0.0", "release_candidate": "LSC-6.5.0-rc1", "model_sha256": "c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8", "files": manifest_rows})
    checksum_paths = sorted(path for path in target.rglob("*") if path.is_file() and path.name != "SHA256SUMS.txt")
    (target / "SHA256SUMS.txt").write_text("".join(f"{digest(path)}  {path.relative_to(target).as_posix()}\n" for path in checksum_paths), encoding="utf-8")


def materialize(target: Path) -> None:
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite existing RC target: {target}")
    target.mkdir(parents=True)
    for relative in FILES:
        source = ROOT / relative
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    shutil.copyfile(ROOT / "docs/model/LSC_6_5_0_RC_README.md", target / "README.md")
    package_init = target / "src/lsc_kernel/__init__.py"
    package_init.parent.mkdir(parents=True, exist_ok=True)
    package_init.write_text(
        '\"\"\"Minimal LSC 6.5.0 RC package surface.\"\"\"\n\nfrom lsc_kernel.lsc650 import ExactGalliumCaptureCrossSection, LSC650Evaluator\n\n__all__ = [\"ExactGalliumCaptureCrossSection\", \"LSC650Evaluator\"]\n',
        encoding="utf-8",
    )

    original_manifest = json.loads((ROOT / "external_physics/gallium_capture/PROVENANCE_MANIFEST.json").read_text(encoding="utf-8"))
    evidence_path = target / "provenance/GALLIUM_CAPTURE_PROVENANCE_MANIFEST_FROZEN.json"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "external_physics/gallium_capture/PROVENANCE_MANIFEST.json", evidence_path)
    release_manifest = dict(original_manifest)
    release_manifest["document_kind"] = "GALLIUM_CAPTURE_CROSS_SECTION_RC_EXECUTION_MANIFEST"
    release_manifest["original_files"] = []
    release_manifest["release_candidate_source_policy"] = {
        "original_publications_redistributed": False,
        "frozen_original_hash_manifest": "provenance/GALLIUM_CAPTURE_PROVENANCE_MANIFEST_FROZEN.json",
        "source_retrieval": "Use cited DOI/official URLs; no independent relicensing is asserted.",
    }
    write_json(target / "external_physics/gallium_capture/PROVENANCE_MANIFEST.json", release_manifest)

    write_manifests(target)


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--refresh-manifests":
        write_manifests(TARGET)
        print(TARGET.relative_to(ROOT).as_posix())
        return 0
    materialize(TARGET)
    print(TARGET.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
