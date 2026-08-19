from __future__ import annotations

import hashlib
import json
import math
import zipfile
from decimal import Decimal
from pathlib import Path

import pytest

from kernel_helpers import ROOT
from lsc_kernel.lsc650 import ExactGalliumCaptureCrossSection, LSC650Evaluator
from lsc_kernel.lsc650.errors import ParameterBundleError, UnsupportedDomainError
from tools.audit_lsc650_third_path import (
    ThirdPathDomainError,
    alpha_domain,
    exact_ratio,
    load_source_lines,
    load_spline,
    run_audit,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authorized_payload(alpha: float) -> dict[str, object]:
    source = json.loads(
        (ROOT / "external_physics/gallium_capture/source_lines_prc108_035502.json")
        .read_text(encoding="utf-8")
    )
    factors = {
        "source_activity_bq": 1.0,
        "exposure_seconds": 1.0,
        "conventional_probability": 1.0,
        "geometry_factor": 1.0,
        "detector_efficiency": 1.0,
    }
    return {
        "schema_version": "1.0.0",
        "model_version": "6.5.0",
        "model_profile": "EXACT_FINITE_A2/C/A",
        "response_variant": "EXACT_CAPTURE_ARGUMENT_DILATION",
        "cross_section_scenario_id": "BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE",
        "source_line_payload_sha256": "ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e",
        "input_classification": "AUTHORIZED_SOURCE_INPUT",
        "experiment_id": "STEP08_AUDIT",
        "observation_id": "NO_OUTCOME_PREDICTION_ONLY",
        "source_isotope": "Cr51",
        "alpha_0": alpha,
        "parameter_source": {
            "kind": "FROZEN_PARAMETER_BUNDLE",
            "bundle_sha256": sha256(ROOT / "LSC_6_5_0_PARAMETER_BUNDLE.json"),
        },
        "lines": [{**row, **factors} for row in source["isotopes"]["Cr51"]],
        "analysis_context": {
            "role": "PREDICTION_ONLY",
            "covariance_scenario_id": "NONE_PREDICTION_ONLY",
            "nuisance_policy_id": "NONE_PREDICTION_ONLY",
            "observed_outcomes_included": False,
            "BEST2_observed_data_accessed": False,
        },
    }


def publication_packages() -> tuple[Path, ...]:
    return (
        ROOT / "publication/github",
        ROOT / "publication/zenodo/LSC-6.5.0",
        ROOT / "publication/zenodo/LSC-Validation-Kernel",
    )


class TestStep08ScientificAudit:
    def test_immutable_scientific_hashes(self) -> None:
        expected = {
            "spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml": "114e8398a45e6a6c8fb4a105e994ca695805b06b9ed8608b86288ea0791ef948",
            "external_physics/gallium_capture/bahcall_1997_best_estimate.csv": "55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5",
            "external_physics/gallium_capture/source_lines_prc108_035502.json": "ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e",
            "LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json": "bf05812385439b0c82a53ed9bf52a26b65b6b8925903fab4f04e6d4d5a67a56c",
            "LSC_6_5_0_PREFIT_FREEZE.json": "7a0fdacd8fcff134386e4864228554454237ddc8da3df2429effa4b3f23403e0",
            "LSC_6_5_0_PARAMETER_BUNDLE.json": "617d72a303a947e8e7467efb3c745f7e44dc1c07eab7d830a90dbfd179da5c18",
        }
        for relative, digest in expected.items():
            assert sha256(ROOT / relative) == digest
        assert (
            ROOT / "LSC_6_5_0_MODEL_SHA256"
        ).read_text(encoding="utf-8").strip() == "c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8"

    def test_third_path_complete_receipt(self) -> None:
        receipt = run_audit(ROOT)
        assert receipt["status"] == "PASS"
        assert receipt["golden_success_vectors"]["passed"] == 20
        assert receipt["all_source_line_grid_checks"] == 90
        assert receipt["first_order_bridge"]["status"] == "PASS"
        assert receipt["parameter_root_reconstruction"]["status"] == "PASS"

    def test_third_path_matches_production_for_all_lines_and_grid_points(self) -> None:
        third = load_spline(ROOT)
        source = load_source_lines(ROOT)
        rows = [row for isotope in ("Cr51", "Ar37") for row in source[isotope]]
        domain = alpha_domain(third, rows)
        grid = (
            domain[0] + Decimal("1e-10"),
            Decimal("-0.3"),
            Decimal("-0.19024973740805776"),
            Decimal("-0.14388795521516184"),
            Decimal("-0.10233891434687088"),
            Decimal("-0.000001"),
            Decimal(0),
            Decimal("0.000001"),
            Decimal("0.3"),
            domain[1] - Decimal("1e-10"),
        )
        production = ExactGalliumCaptureCrossSection.from_repository(ROOT)
        differences = []
        for alpha in grid:
            for row in rows:
                energy = Decimal(str(row["energy_mev"]))
                independent = float(exact_ratio(third, energy, alpha))
                expected = production.exact_ratio(float(energy), float(alpha))[0]
                differences.append(abs(independent - expected))
        assert len(differences) == 90
        assert max(differences) <= 5e-11

    def test_exact_domain_boundary_and_outside_fail_closed(self) -> None:
        third = load_spline(ROOT)
        source = load_source_lines(ROOT)
        rows = [row for isotope in ("Cr51", "Ar37") for row in source[isotope]]
        lower, upper = alpha_domain(third, rows)
        production = ExactGalliumCaptureCrossSection.from_repository(ROOT)
        assert max(abs(float(a) - b) for a, b in zip((lower, upper), (-0.5747389495096434, 3.607238025076703), strict=True)) < 5e-15
        for alpha in (lower, lower + Decimal("1e-12"), upper - Decimal("1e-12"), upper):
            for row in rows:
                assert exact_ratio(third, Decimal(str(row["energy_mev"])), alpha) > 0
        for alpha in (lower - Decimal("1e-12"), upper + Decimal("1e-12")):
            with pytest.raises(ThirdPathDomainError):
                for row in rows:
                    exact_ratio(third, Decimal(str(row["energy_mev"])), alpha)
            with pytest.raises(UnsupportedDomainError):
                production.validate_alpha(float(alpha), (float(row["energy_mev"]) for row in rows))

    def test_frozen_bundle_rejects_silent_alpha_override(self) -> None:
        evaluator = LSC650Evaluator.from_repository(ROOT)
        frozen = -0.14388795521516184
        assert evaluator.predict(authorized_payload(frozen))["alpha_0"] == frozen
        with pytest.raises(ParameterBundleError):
            evaluator.predict(authorized_payload(frozen + 1e-6))

    def test_aborted_source_revisions_reconstruct_exactly(self) -> None:
        current = (ROOT / "src/lsc_kernel/lsc650/determination.py").read_text(encoding="utf-8")
        first_two = (
            '"unconstrained_diagnostic_predeclared": False,',
            '"unconstrained_diagnostic_performed": False,',
        )
        last_three = (
            '"refit_authorized": False,',
            '"BEST2_observed_data_accessed": False,',
            '"BEST2_prediction_generated": False,',
        )

        def lower_literals(text: str, targets: tuple[str, ...]) -> str:
            for target in targets:
                position = text.rfind(target)
                assert position >= 0
                text = (
                    text[:position]
                    + target.replace("False", "false")
                    + text[position + len(target):]
                )
            return text

        r2 = lower_literals(current, last_three)
        r1 = lower_literals(r2, first_two)
        assert hashlib.sha256(r1.encode()).hexdigest() == "86070aded79a0c9c5e959d441414bed83f5598d8f4a9d69a65a741c3e94bc02b"
        assert hashlib.sha256(r2.encode()).hexdigest() == "86c0bd75072da14f6260eeca9b82ed3c8a95b6148022f25054beadf8ffaa86b3"
        assert hashlib.sha256(current.encode()).hexdigest() == "fc8b7e1517b98995e6a140aa190d264fa2f19c1899d20927996558bcf9818879"

    def test_objective_dof_interpretation_is_explicit(self) -> None:
        protocol = json.loads((ROOT / "LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json").read_text())
        result = json.loads((ROOT / "LSC_6_5_0_ALPHA_DETERMINATION_RESULT.json").read_text())
        assert len(protocol["development_data"]["observations"]) == 1
        assert result["profiled_nuisance_parameters"] == []
        assert math.isclose(result["objective_value"], 2.169792942258529e-20, rel_tol=0, abs_tol=1e-32)
        report = (ROOT / "docs/audit/LSC_6_5_0_OBJECTIVE_DOF_AUDIT.md").read_text()
        assert "effective residual degrees of freedom: `1 - 1 - 0 = 0`" in report
        assert "The near-zero objective is expected from the construction and is not evidence" in report


class TestStep08ReleasePreparation:
    def test_required_step08_documents_exist(self) -> None:
        required = (
            "docs/audit/LSC_6_5_0_CROSS_SECTION_ACCOUNTING_AUDIT.md",
            "docs/audit/LSC_6_5_0_THIRD_PATH_NUMERICAL_AUDIT.md",
            "docs/audit/LSC_6_5_0_OBJECTIVE_DOF_AUDIT.md",
            "docs/audit/STEP_07E_ABORTED_RUN_FORENSICS.md",
            "docs/audit/PACKAGE_VS_MODEL_VERSIONING_DECISION.md",
            "RELEASE_NOTES_LSC_6_5_0.md",
            "PHASE_2_VALIDATION_HANDOFF.md",
            "BEST2_PROSPECTIVE_HANDOFF.md",
        )
        for relative in required:
            assert (ROOT / relative).is_file(), relative

    def test_zenodo_metadata_is_separate_and_owner_upload_ready(self) -> None:
        model_source = ROOT / "docs/release/ZENODO_LSC_6_5_0_METADATA.json"
        kernel_source = ROOT / "docs/release/ZENODO_VALIDATION_KERNEL_METADATA.json"
        model = json.loads(model_source.read_text(encoding="utf-8"))
        kernel = json.loads(kernel_source.read_text(encoding="utf-8"))
        kernel_creators = [
            {"name": "LuciferSun", "affiliation": "Independent Research"},
            {"name": "flAmeBorn", "affiliation": "Independent Research"},
        ]
        model_creators = [*kernel_creators, {"name": "LINZ HOSS"}]
        assert model["title"] == "LSC 6.5.0 exact finite-dilation scientific model"
        assert model["version"] == "6.5.0"
        assert kernel["title"] == "LSC Validation Kernel reproducibility companion"
        assert kernel["version"] == "0.6.0"
        assert model["creators"] == model_creators
        assert kernel["creators"] == kernel_creators
        assert model["deposit_status"] == "PUBLISHED"
        assert model["owner_upload_ready"] is False
        assert model["upload_performed"] is True
        assert model["doi_minted"] is True
        assert model["new_version_doi"] == "10.5281/zenodo.22007108"
        assert kernel["deposit_status"] == "BLOCKED_PENDING_COAUTHOR_CONFIRMATION"
        assert kernel["coauthor_status"] == "KERNEL_COAUTHOR_CONFIRMATION_REQUIRED"
        assert kernel["owner_upload_ready"] is False
        assert kernel["upload_performed"] is False
        assert kernel["doi_minted"] is False
        assert kernel["related_model_version_doi"] == "10.5281/zenodo.22007108"
        for metadata in (model, kernel):
            assert metadata["upload_type"] == "software"
            assert metadata["access_right"] == "open"
            assert metadata["license"] == "mit"
        assert all(item["identifier"] for item in metadata["related_identifiers"])
        assert model["validation_kernel_companion_doi"] is None
        assert kernel["companion_doi"] is None

        kernel_citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        model_citation = (ROOT / "docs/release/LSC_6_5_0_CITATION.cff").read_text(
            encoding="utf-8"
        )
        assert 'title: "LSC Validation Kernel reproducibility companion"' in kernel_citation
        assert 'version: "0.6.0"' in kernel_citation
        assert 'title: "LSC 6.5.0 exact finite-dilation scientific model"' in model_citation
        assert 'version: "6.5.0"' in model_citation
        assert 'family-names: "LINZ HOSS"' in model_citation
        assert 'family-names: "LINZ HOSS"' not in kernel_citation

        packages = publication_packages()
        if not all(package.is_dir() for package in packages):
            return
        github, model_package, kernel_package = packages
        deposit_fields = {
            "title",
            "upload_type",
            "version",
            "description",
            "creators",
            "access_right",
            "license",
            "keywords",
            "related_identifiers",
            "language",
        }
        for package, source_metadata, source_citation in (
            (github, kernel, kernel_citation),
            (model_package, model, model_citation),
            (kernel_package, kernel, kernel_citation),
        ):
            packaged_metadata = json.loads((package / "ZENODO_METADATA.json").read_text())
            if package == model_package:
                assert packaged_metadata["deposit_status"] == "READY_FOR_OWNER_UPLOAD"
                assert packaged_metadata["upload_performed"] is False
                assert packaged_metadata["doi_minted"] is False
                assert packaged_metadata["new_version_doi"] is None
            else:
                assert packaged_metadata == source_metadata
            deposit = json.loads((package / ".zenodo.json").read_text())
            assert set(deposit) == deposit_fields
            for field in deposit_fields:
                assert deposit[field] == source_metadata[field]
            packaged_citation = (package / "CITATION.cff").read_text(encoding="utf-8")
            if package == model_package:
                assert 'title: "LSC 6.5.0 exact finite-dilation scientific model"' in packaged_citation
                assert 'version: "6.5.0"' in packaged_citation
                assert 'family-names: "LINZ HOSS"' in packaged_citation
            else:
                assert packaged_citation == source_citation

    def test_publication_state_records_model_publication_only(self) -> None:
        state = json.loads((ROOT / "PUBLICATION_STATE.json").read_text())
        assert state["publication_ready"] is True
        assert state["publication_performed"] is True
        assert state["public_push_performed"] is True
        assert state["zenodo_upload_performed"] is True
        assert state["doi_minted"] is True
        assert state["zenodo_version_doi"] == "10.5281/zenodo.22007108"
        assert state["zenodo_concept_doi"] == "10.5281/zenodo.19780615"
        for field in (
            "github_release_created",
            "best2_observed_data_accessed",
            "best2_prediction_generated",
            "phase_2_validation_performed",
        ):
            assert state[field] is False

    def test_public_package_checksums_and_payload_policy_if_built(self) -> None:
        packages = publication_packages()
        if not all(package.is_dir() for package in packages):
            return
        forbidden_parts = {".git", ".codex", "__pycache__", ".pytest_cache"}
        for package in packages:
            assert not (package / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv").exists()
            for path in package.rglob("*"):
                assert not forbidden_parts.intersection(path.relative_to(package).parts)
                assert not path.is_symlink()
            for line in (package / "SHA256SUMS.txt").read_text().splitlines():
                expected, relative = line.split("  ", 1)
                assert sha256(package / relative) == expected

    def test_deterministic_zip_metadata_and_top_level_checksums_if_built(self) -> None:
        sums = ROOT / "publication/zenodo/SHA256SUMS.txt"
        if not sums.is_file():
            return
        for line in sums.read_text().splitlines():
            expected, name = line.split("  ", 1)
            archive = sums.parent / name
            assert sha256(archive) == expected
            with zipfile.ZipFile(archive) as handle:
                names = handle.namelist()
                assert names == sorted(names)
                assert all(info.date_time == (2026, 8, 18, 0, 0, 0) for info in handle.infolist())

    def test_public_facing_claims_keep_validation_boundary(self) -> None:
        files = (
            ROOT / "RELEASE_NOTES_LSC_6_5_0.md",
            ROOT / "MODEL_CARD_LSC_6_5_0.md",
            ROOT / "docs/release/LSC_6_5_0_PUBLICATION_README.md",
            ROOT / "docs/release/GITHUB_PUBLICATION_README.md",
            ROOT / "docs/release/VALIDATION_KERNEL_PUBLICATION_README.md",
        )
        for path in files:
            text = path.read_text(encoding="utf-8").lower()
            assert "not" in text and "validat" in text
            assert "best-2" in text or "best2" in text
