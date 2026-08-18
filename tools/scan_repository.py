#!/usr/bin/env python3
"""Read-only current-tree scan for potential historical LSC objects."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tarfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from recovery_lib import (
    SERIALIZED_SUFFIXES,
    TEXT_SUFFIXES,
    extract_document_text,
    extract_notebook_text,
    inspect_serialized,
    iter_files,
    normalized_excerpt,
    safe_relative,
    sha256_file,
    stable_artifact_id,
    write_csv,
    write_json,
)


KEYWORDS = {
    "theta": r"(?<![A-Za-z])theta(?![A-Za-z])|(?:θ)",
    "lambda0": r"lambda[ _]?0|lambda_?\{?0\}?|(?:λ)\s*_?0",
    "lambdaA": r"lambda[ _]?A|lambda_?\{?A\}?|(?:λ)\s*_?A",
    "f0_a": r"f0_?a|f_?\{?0,?a\}?|f0\s*\(",
    "fA_a": r"fA_?a|f_?\{?A,?a\}?|fA\s*\(",
    "tensor": r"tensor|A_?a\^?\{?ij\}?|D_?(?:mu|μ)|traceless",
    "anisotropy": r"anisotrop|directional",
    "orientation": r"orientation|Euler|azimuth|declination|right ascension",
    "rotation_or_frame": r"rotation|reference frame|coordinate frame|lab frame|ICRS|R_lab",
    "parameter_vector": r"parameter vector|parameter ordering|theta vector|full vector",
    "fit_result": r"best[ _-]?fit|fit result|optimized parameters?|coefficients?",
    "checkpoint": r"checkpoint|state_dict|model checkpoint",
    "prediction": r"prediction table|predictions?\.csv|frozen prediction|pre[- ]data prediction",
    "evaluator": r"evaluator|evaluate\s*\(|class .*Evaluator|def .*predict",
    "equations_E1_E12": r"(?:^|[^A-Za-z0-9])E(?:1[0-2]|[1-9])(?:[^A-Za-z0-9]|$)",
    "lsc_6_3_0": r"LSC[ _-]?6\.3(?:\.0)?|6\.3\.0-pre-BEST2",
}

COMPILED = {name: re.compile(pattern, re.IGNORECASE | re.MULTILINE) for name, pattern in KEYWORDS.items()}
COMBINED = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in KEYWORDS.items()),
    re.IGNORECASE | re.MULTILINE,
)
P0_TERMS = {
    "theta",
    "lambda0",
    "lambdaA",
    "f0_a",
    "fA_a",
    "tensor",
    "orientation",
    "rotation_or_frame",
    "parameter_vector",
    "prediction",
    "evaluator",
    "equations_E1_E12",
    "lsc_6_3_0",
}
ARCHIVE_SUFFIXES = {".zip", ".tar"}
MAX_IN_MEMORY_TEXT_BYTES = 2 * 1024 * 1024
STREAM_CHUNK_BYTES = 8 * 1024 * 1024
STREAM_OVERLAP_BYTES = 1024
STREAM_NEEDLES = {
    "theta": (b"theta", "θ".encode("utf-8")),
    "lambda0": (b"lambda0", b"lambda_0", b"lambda 0", "λ0".encode("utf-8")),
    "lambdaA": (b"lambdaa", b"lambda_a", b"lambda a", "λa".encode("utf-8")),
    "f0_a": (b"f0_a", b"f_0a", b"f_{0,a}"),
    "fA_a": (b"fa_a", b"f_aa", b"f_{a,a}"),
    "tensor": (b"tensor", b"a_a^{ij}", b"d_mu", "d_μ".encode("utf-8"), b"traceless"),
    "anisotropy": (b"anisotrop", b"directional"),
    "orientation": (b"orientation", b"euler", b"azimuth", b"declination", b"right ascension"),
    "rotation_or_frame": (b"rotation", b"reference frame", b"coordinate frame", b"lab frame", b"icrs", b"r_lab"),
    "parameter_vector": (b"parameter vector", b"parameter ordering", b"theta vector", b"full vector"),
    "fit_result": (b"best fit", b"best-fit", b"fit result", b"optimized parameter", b"coefficients"),
    "checkpoint": (b"checkpoint", b"state_dict", b"model checkpoint"),
    "prediction": (b"prediction table", b"predictions.csv", b"frozen prediction", b"pre-data prediction"),
    "evaluator": (b"evaluator", b"def predict", b"def evaluate"),
    "equations_E1_E12": (b"e1.", b"e2.", b"e10.", b"e11.", b"e12."),
    "lsc_6_3_0": (b"lsc 6.3", b"lsc_6_3", b"lsc-6.3", b"6.3.0-pre-best2"),
}


def matched_terms(text: str) -> list[str]:
    return sorted({match.lastgroup for match in COMBINED.finditer(text) if match.lastgroup})


def first_matching_excerpt(text: str, terms: list[str]) -> str:
    if not terms:
        return ""
    match = COMBINED.search(text)
    if match is None:
        return ""
    start = max(0, match.start() - 100)
    end = min(len(text), match.end() + 140)
    return normalized_excerpt(text[start:end])


def scan_streaming_text(path: Path) -> tuple[list[str], str]:
    """Scan every byte of a large text file using bounded literal matching."""

    found: set[str] = set()
    excerpt = ""
    overlap = b""
    with path.open("rb") as handle:
        while True:
            block = handle.read(STREAM_CHUNK_BYTES)
            if not block:
                break
            payload = overlap + block
            lowered = payload.lower()
            for term, needles in STREAM_NEEDLES.items():
                if term in found:
                    continue
                positions = [(lowered.find(needle.lower()), needle) for needle in needles]
                positions = [(position, needle) for position, needle in positions if position >= 0]
                if not positions:
                    continue
                position, needle = min(positions, key=lambda item: item[0])
                found.add(term)
                if not excerpt:
                    start = max(0, position - 100)
                    end = min(len(payload), position + len(needle) + 140)
                    excerpt = normalized_excerpt(payload[start:end].decode("utf-8", errors="replace"))
            overlap = payload[-STREAM_OVERLAP_BYTES:]
    return sorted(found), excerpt


def inspect_archive_members(path: Path) -> tuple[int, str]:
    names: list[str] = []
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            names = sorted(item.filename for item in archive.infolist())
    elif path.suffix.lower() == ".tar":
        with tarfile.open(path, mode="r:*") as archive:
            names = sorted(item.name for item in archive.getmembers())
    return len(names), ";".join(names[:100])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    arguments = parser.parse_args()

    source = arguments.source.resolve()
    output = arguments.output_dir.resolve()
    if not source.is_dir():
        parser.error(f"source is not a directory: {source}")

    candidates: list[dict[str, object]] = []
    serialized_rows: list[dict[str, object]] = []
    notebook_rows: list[dict[str, object]] = []
    archive_rows: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []
    extension_counts: Counter[str] = Counter()
    hashes: dict[str, list[str]] = defaultdict(list)
    scanned = 0
    text_extracted = 0
    pdf_success = 0
    pdf_fail = 0
    large_text_streamed = 0

    for path in iter_files(source):
        scanned += 1
        relative = safe_relative(path, source)
        suffix = path.suffix.lower()
        extension_counts[suffix or "[none]"] += 1
        path_terms = matched_terms(relative)
        content_terms: list[str] = []
        extraction = "metadata_only"
        excerpt = ""
        digest = ""

        if suffix in SERIALIZED_SUFFIXES:
            metadata = inspect_serialized(path)
            serialized_rows.append(
                {
                    "artifact_id": stable_artifact_id(relative, metadata["sha256"], prefix="serialized"),
                    "source_path": relative,
                    **metadata,
                    "path_keyword_matches": ";".join(path_terms),
                }
            )
            digest = str(metadata["sha256"])
            hashes[digest].append(relative)

        if suffix in ARCHIVE_SUFFIXES:
            try:
                member_count, member_sample = inspect_archive_members(path)
                member_terms = matched_terms(member_sample)
                digest = digest or sha256_file(path)
                archive_rows.append(
                    {
                        "artifact_id": stable_artifact_id(relative, digest, prefix="archive"),
                        "source_path": relative,
                        "size_bytes": path.stat().st_size,
                        "sha256": digest,
                        "member_count": member_count,
                        "member_keyword_matches": ";".join(member_terms),
                        "member_name_sample": member_sample,
                    }
                )
                hashes[digest].append(relative)
                path_terms = sorted(set(path_terms) | set(member_terms))
            except (OSError, tarfile.TarError, zipfile.BadZipFile) as exc:
                errors.append({"source_path": relative, "stage": "archive_inventory", "error": f"{type(exc).__name__}: {exc}"})

        supported_text = suffix in TEXT_SUFFIXES or suffix in {".pdf", ".docx", ".odt", ".ipynb"}
        if supported_text:
            try:
                if suffix in TEXT_SUFFIXES and path.stat().st_size > MAX_IN_MEMORY_TEXT_BYTES:
                    content_terms, excerpt = scan_streaming_text(path)
                    extraction = "streaming_text_single_pass"
                    large_text_streamed += 1
                else:
                    text, extraction = extract_document_text(path)
                    content_terms = matched_terms(text)
                    excerpt = first_matching_excerpt(text, content_terms)
                    if suffix == ".ipynb":
                        _, notebook_counts = extract_notebook_text(path)
                        notebook_rows.append(
                            {
                                "artifact_id": stable_artifact_id(relative, prefix="notebook"),
                                "source_path": relative,
                                "size_bytes": path.stat().st_size,
                                "sha256": sha256_file(path),
                                "code_cells": notebook_counts["code_cells"],
                                "saved_output_blocks": notebook_counts["output_blocks"],
                                "keyword_matches": ";".join(content_terms),
                                "saved_outputs_scanned": "YES",
                            }
                        )
                text_extracted += 1
                if suffix == ".pdf":
                    pdf_success += 1
            except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired, zipfile.BadZipFile) as exc:
                if suffix == ".pdf":
                    pdf_fail += 1
                errors.append({"source_path": relative, "stage": "text_extraction", "error": f"{type(exc).__name__}: {exc}"})

        terms = sorted(set(path_terms) | set(content_terms))
        if terms:
            digest = digest or sha256_file(path)
            hashes[digest].append(relative)
            candidates.append(
                {
                    "artifact_id": stable_artifact_id(relative, digest, prefix="candidate"),
                    "priority": "P0" if set(terms) & P0_TERMS else "P1",
                    "source_path": relative,
                    "extension": suffix or "[none]",
                    "size_bytes": path.stat().st_size,
                    "sha256": digest,
                    "keyword_matches": ";".join(terms),
                    "extraction_method": extraction,
                    "first_match_excerpt": excerpt,
                }
            )

    candidate_columns = [
        "artifact_id",
        "priority",
        "source_path",
        "extension",
        "size_bytes",
        "sha256",
        "keyword_matches",
        "extraction_method",
        "first_match_excerpt",
    ]
    serialized_columns = [
        "artifact_id",
        "source_path",
        "format",
        "size_bytes",
        "sha256",
        "inspection",
        "safe_load_performed",
        "structure",
        "path_keyword_matches",
    ]
    notebook_columns = [
        "artifact_id",
        "source_path",
        "size_bytes",
        "sha256",
        "code_cells",
        "saved_output_blocks",
        "keyword_matches",
        "saved_outputs_scanned",
    ]
    archive_columns = [
        "artifact_id",
        "source_path",
        "size_bytes",
        "sha256",
        "member_count",
        "member_keyword_matches",
        "member_name_sample",
    ]
    candidates.sort(key=lambda row: (str(row["priority"]), str(row["source_path"])))
    serialized_rows.sort(key=lambda row: str(row["source_path"]))
    notebook_rows.sort(key=lambda row: str(row["source_path"]))
    archive_rows.sort(key=lambda row: str(row["source_path"]))
    errors.sort(key=lambda row: (str(row["source_path"]), str(row["stage"])))

    write_csv(output / "REPOSITORY_CANDIDATES.csv", candidates, candidate_columns)
    write_csv(output / "SERIALIZED_ARTIFACTS.csv", serialized_rows, serialized_columns)
    write_csv(output / "NOTEBOOK_OUTPUT_SCAN.csv", notebook_rows, notebook_columns)
    write_csv(output / "ARCHIVE_MEMBER_SCAN.csv", archive_rows, archive_columns)
    write_csv(output / "REPOSITORY_SCAN_ERRORS.csv", errors, ["source_path", "stage", "error"])
    duplicate_groups = [
        {"sha256": digest, "path_count": len(set(paths)), "paths": sorted(set(paths))}
        for digest, paths in sorted(hashes.items())
        if len(set(paths)) > 1
    ]
    write_json(output / "DUPLICATE_HASH_GROUPS.json", duplicate_groups)
    summary = {
        "archive_artifacts_scanned": len(archive_rows),
        "binary_serialized_artifacts_scanned": len(serialized_rows),
        "candidate_artifacts_found": len(candidates),
        "duplicate_hash_groups": len(duplicate_groups),
        "errors": len(errors),
        "extension_counts": dict(sorted(extension_counts.items())),
        "files_scanned": scanned,
        "large_text_files_streamed": large_text_streamed,
        "notebooks_scanned": len(notebook_rows),
        "pdf_extraction_failed": pdf_fail,
        "pdf_extraction_succeeded": pdf_success,
        "source_label": "LSC_6_3_0_VALIDATION",
        "text_documents_extracted": text_extracted,
    }
    write_json(output / "REPOSITORY_SCAN_SUMMARY.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
