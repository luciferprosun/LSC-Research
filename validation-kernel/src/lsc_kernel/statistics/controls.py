"""Large public covariance controls for software diagnostics, not LSC inference."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from lsc_kernel.io.hashes import sha256_file
from lsc_kernel.validation.external import load_and_validate_icecube_release_index


def _matrix_diagnostics(matrix: NDArray[np.float64], *, symmetry_tolerance: float = 1e-10) -> dict[str, object]:
    square = matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]
    finite = bool(np.isfinite(matrix).all())
    symmetric = bool(square and finite and np.allclose(matrix, matrix.T, rtol=0.0, atol=symmetry_tolerance))
    result: dict[str, object] = {
        "shape": list(matrix.shape),
        "square": square,
        "finite": finite,
        "symmetric": symmetric,
        "symmetry_tolerance": symmetry_tolerance,
    }
    if square and finite and symmetric:
        eigenvalues = np.linalg.eigvalsh(matrix)
        absolute_eigenvalues = np.abs(eigenvalues)
        scale = max(float(np.max(absolute_eigenvalues)), np.finfo(np.float64).tiny)
        tolerance = float(matrix.shape[0] * np.finfo(np.float64).eps * scale)
        positive = eigenvalues[eigenvalues > tolerance]
        nonzero = absolute_eigenvalues[absolute_eigenvalues > tolerance]
        rank = int(nonzero.size)
        result.update(
            {
                "minimum_eigenvalue": float(eigenvalues[0]),
                "maximum_eigenvalue": float(eigenvalues[-1]),
                "rank": rank,
                "rank_tolerance": tolerance,
                "positive_eigenvalue_count": int(np.sum(eigenvalues > tolerance)),
                "negative_eigenvalue_count": int(np.sum(eigenvalues < -tolerance)),
                "near_zero_eigenvalue_count": int(np.sum(absolute_eigenvalues <= tolerance)),
                "condition_number_nonzero_spectrum": (
                    float(scale / np.min(nonzero)) if nonzero.size else None
                ),
                "condition_number_positive_subspace": (
                    float(eigenvalues[-1] / positive[0]) if positive.size and eigenvalues[-1] > 0 else None
                ),
                "positive_semidefinite_within_tolerance": bool(eigenvalues[0] >= -tolerance),
                "singular_within_tolerance": bool(rank < matrix.shape[0]),
            }
        )
    return result


def _hepdata_matrix(path: Path, dimension: int) -> NDArray[np.float64]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    values = payload.get("values", [])
    if len(values) != dimension * dimension:
        raise ValueError(f"{path.name} does not contain {dimension}x{dimension} entries.")
    matrix = np.empty((dimension, dimension), dtype=np.float64)
    seen: set[tuple[int, int]] = set()
    for row in values:
        coordinates = tuple(int(float(item["value"])) for item in row["x"][:2])
        if coordinates in seen or len(coordinates) != 2:
            raise ValueError(f"{path.name} has duplicate/malformed matrix coordinates.")
        seen.add(coordinates)
        matrix[coordinates] = float(row["y"][0]["value"])
    return matrix


def _stereo_controls(root: Path) -> dict[str, object]:
    directory = root / "LSC_6_3_0_VALIDATION/09_OTHER_NEUTRINO_CONSTRAINTS/STEREO/HEPData"
    covariance_path = directory / "prompt_spectra_covariance.json"
    response_path = directory / "detector_response_matrix.json"
    measured_path = directory / "measured_spectra_each_cell.json"
    covariance = json.loads(covariance_path.read_text(encoding="utf-8"))
    response = json.loads(response_path.read_text(encoding="utf-8"))
    measured = json.loads(measured_path.read_text(encoding="utf-8"))

    def axes(payload: dict[str, Any]) -> tuple[tuple[str, ...], tuple[str, ...]]:
        first = tuple(dict.fromkeys(item["x"][0]["value"] for item in payload["values"]))
        second = tuple(dict.fromkeys(item["x"][1]["value"] for item in payload["values"]))
        return first, second

    covariance_axes = axes(covariance)
    response_axes = axes(response)
    covariance_values = np.asarray(
        [float(item["y"][0]["value"]) for item in covariance["values"]], dtype=np.float64
    ).reshape(44, 44)
    response_finite = all(
        math.isfinite(float(y["value"])) for item in response["values"] for y in item["y"]
    )
    return {
        "covariance_path": covariance_path.relative_to(root).as_posix(),
        "covariance_sha256": sha256_file(covariance_path),
        "covariance": _matrix_diagnostics(covariance_values),
        "covariance_energy_axes": [len(covariance_axes[0]), len(covariance_axes[1])],
        "response_path": response_path.relative_to(root).as_posix(),
        "response_sha256": sha256_file(response_path),
        "response_entry_shape": [len(response_axes[0]), len(response_axes[1])],
        "response_groups": sorted(
            {int(y["group"]) for item in response["values"] for y in item["y"]}
        ),
        "response_finite": response_finite,
        "measured_energy_bins": len(measured["values"]),
        "covariance_prompt_axis_matches_response_prompt_axis": covariance_axes[0] == response_axes[0],
        "compatibility_note": (
            "The covariance is 44x44 over two concatenated prompt spectra; the response stores a 22-bin prompt axis "
            "and a distinct 22-bin neutrino-energy axis in two y groups. Compatibility is therefore checked on the "
            "shared prompt-energy axis, not by falsely equating prompt and neutrino axes."
        ),
    }


def run_statistical_control_diagnostics(root: Path) -> dict[str, object]:
    microboone_path = root / (
        "LSC_6_3_0_VALIDATION/09_OTHER_NEUTRINO_CONSTRAINTS/"
        "MicroBooNE/HEPData/covariance_14_channels.json"
    )
    microboone = _hepdata_matrix(microboone_path, 364)
    prospect_directory = root / (
        "LSC_6_3_0_VALIDATION/09_OTHER_NEUTRINO_CONSTRAINTS/"
        "PROSPECT/Source/anc/data/CovarianceMatrices"
    )
    prospect = {}
    for name in ("BackgroundCovMatrix.txt", "StatisticalCovMatrix.txt", "SystematicCovMatrix.txt"):
        path = prospect_directory / name
        matrix = np.loadtxt(path, comments="#", dtype=np.float64)
        prospect[name] = {
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256_file(path),
            "diagnostics": _matrix_diagnostics(matrix),
        }
    microboone_diagnostics = _matrix_diagnostics(microboone)
    stereo = _stereo_controls(root)
    icecube = load_and_validate_icecube_release_index(root)
    passed = (
        microboone_diagnostics["shape"] == [364, 364]
        and microboone_diagnostics["finite"]
        and microboone_diagnostics["symmetric"]
        and all(
            item["diagnostics"]["shape"] == [990, 990]
            and item["diagnostics"]["finite"]
            and item["diagnostics"]["symmetric"]
            for item in prospect.values()
        )
        and stereo["covariance_prompt_axis_matches_response_prompt_axis"]
        and stereo["response_finite"]
        and icecube["file_records"] == 52
        and icecube["numerical_objects_validated"] == 8
        and icecube["release_loading_ready"]
        and icecube["mapping_state"] == "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING"
    )
    return {
        "schema_version": "1.0.0",
        "classification": "STATISTICAL_ENGINE_CONTROL",
        "physical_LSC_interpretation_authorized": False,
        "MicroBooNE": {
            "path": microboone_path.relative_to(root).as_posix(),
            "sha256": sha256_file(microboone_path),
            "diagnostics": microboone_diagnostics,
        },
        "PROSPECT": prospect,
        "STEREO": stereo,
        "IceCube": icecube,
        "passed": bool(passed),
    }
