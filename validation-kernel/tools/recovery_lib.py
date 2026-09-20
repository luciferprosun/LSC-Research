"""Deterministic, read-only helpers for Step 01 provenance recovery."""

from __future__ import annotations

import ast
import csv
import hashlib
import io
import json
import os
import re
import struct
import subprocess
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence


CLASSIFICATIONS = {
    "AUTHENTIC_FROZEN",
    "DERIVED_FROM_FROZEN",
    "HISTORICAL_POST_DATA",
    "UNVERIFIED",
    "MISSING",
}

EXPOSURES = {"PRE_DATA", "POST_DATA", "UNKNOWN_EXPOSURE"}

REGISTRY_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "parameter_or_role",
    "value_or_summary",
    "units",
    "source_path",
    "git_commit",
    "git_tag",
    "timestamp_if_known",
    "sha256",
    "data_exposure_status",
    "classification",
    "confidence",
    "notes",
]

TEXT_SUFFIXES = {
    "",
    ".aux",
    ".bbl",
    ".bib",
    ".cff",
    ".cls",
    ".csv",
    ".dat",
    ".flake8",
    ".gitignore",
    ".html",
    ".ini",
    ".json",
    ".lat",
    ".log",
    ".md",
    ".mjs",
    ".nb",
    ".out",
    ".py",
    ".rst",
    ".sh",
    ".svg",
    ".tex",
    ".toml",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

SERIALIZED_SUFFIXES = {
    ".feather",
    ".h5",
    ".hdf5",
    ".joblib",
    ".mat",
    ".npy",
    ".npz",
    ".parquet",
    ".pickle",
    ".pkl",
    ".pt",
    ".pth",
}


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 of a file without mutating it."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_artifact_id(*parts: str, prefix: str = "artifact") -> str:
    canonical = "\x1f".join(str(part) for part in parts)
    suffix = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{suffix}"


def normalized_excerpt(text: str, limit: int = 240) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:limit].rstrip()


def write_csv(path: str | Path, rows: Iterable[Mapping[str, object]], columns: Sequence[str]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_json(path: str | Path, payload: object) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_registry_rows(rows: Sequence[Mapping[str, str]]) -> None:
    identifiers: set[str] = set()
    for index, row in enumerate(rows, start=2):
        missing_columns = [column for column in REGISTRY_COLUMNS if column not in row]
        if missing_columns:
            raise ValueError(f"row {index}: missing columns {missing_columns}")
        artifact_id = row["artifact_id"].strip()
        if not artifact_id:
            raise ValueError(f"row {index}: artifact_id is empty")
        if artifact_id in identifiers:
            raise ValueError(f"row {index}: duplicate artifact_id {artifact_id}")
        identifiers.add(artifact_id)
        classification = row["classification"].strip()
        if classification not in CLASSIFICATIONS:
            raise ValueError(f"row {index}: invalid classification {classification}")
        exposure = row["data_exposure_status"].strip()
        if exposure not in EXPOSURES:
            raise ValueError(f"row {index}: invalid exposure {exposure}")
        if classification == "MISSING":
            if row["source_path"].strip() not in {"", "NOT_FOUND"}:
                raise ValueError(f"row {index}: MISSING row must not point to an artifact")
            if row["sha256"].strip() not in {"", "NOT_APPLICABLE"}:
                raise ValueError(f"row {index}: MISSING row must not have an artifact hash")


def duplicate_hash_groups(rows: Sequence[Mapping[str, str]]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        digest = row.get("sha256", "").strip().lower()
        if re.fullmatch(r"[0-9a-f]{64}", digest):
            groups[digest].append(row.get("artifact_id", ""))
    return sorted(
        [sorted(identifiers) for identifiers in groups.values() if len(identifiers) > 1],
        key=lambda group: tuple(group),
    )


def build_registry(
    source_csv: str | Path,
    output_csv: str | Path,
    archive_root: str | Path,
    kernel_root: str | Path,
) -> list[dict[str, str]]:
    """Validate, hash, sort, and write the adjudicated registry.

    A source path beginning with ``kernel:`` is resolved below ``kernel_root``.
    Every other non-placeholder source path is resolved below ``archive_root``.
    MISSING rows are preserved and never replaced by similarly named files.
    """

    archive = Path(archive_root).resolve()
    kernel = Path(kernel_root).resolve()
    rows = read_csv(source_csv)
    for row in rows:
        source_path = row.get("source_path", "").strip()
        classification = row.get("classification", "").strip()
        if classification == "MISSING":
            row["source_path"] = "NOT_FOUND"
            row["sha256"] = "NOT_APPLICABLE"
            continue
        if not source_path:
            raise ValueError(f"{row.get('artifact_id')}: non-MISSING row has no source_path")
        if source_path.startswith("kernel:"):
            resolved = kernel / source_path.removeprefix("kernel:")
        else:
            resolved = archive / source_path
        if not resolved.is_file():
            raise FileNotFoundError(f"{row.get('artifact_id')}: source not found: {source_path}")
        actual = sha256_file(resolved)
        supplied = row.get("sha256", "").strip().lower()
        if supplied and supplied != actual:
            raise ValueError(f"{row.get('artifact_id')}: SHA-256 mismatch")
        row["sha256"] = actual
    validate_registry_rows(rows)
    rows.sort(key=lambda item: (item["classification"], item["artifact_id"]))
    write_csv(output_csv, rows, REGISTRY_COLUMNS)
    return rows


def _read_npy_header(handle: io.BufferedIOBase) -> dict[str, object]:
    magic = handle.read(6)
    if magic != b"\x93NUMPY":
        raise ValueError("invalid NPY magic")
    version = tuple(handle.read(2))
    if version[0] == 1:
        header_len = struct.unpack("<H", handle.read(2))[0]
    elif version[0] in {2, 3}:
        header_len = struct.unpack("<I", handle.read(4))[0]
    else:
        raise ValueError(f"unsupported NPY version {version}")
    if header_len > 1024 * 1024:
        raise ValueError("NPY header exceeds safety limit")
    header = handle.read(header_len).decode("latin1")
    parsed = ast.literal_eval(header.strip())
    if not isinstance(parsed, dict):
        raise ValueError("NPY header is not a dictionary")
    return {
        "version": ".".join(str(part) for part in version),
        "dtype": str(parsed.get("descr")),
        "fortran_order": bool(parsed.get("fortran_order")),
        "shape": list(parsed.get("shape", ())),
    }


def inspect_serialized(path: str | Path) -> dict[str, object]:
    """Inspect headers/containers only; never deserialize executable objects."""

    candidate = Path(path)
    suffix = candidate.suffix.lower()
    result: dict[str, object] = {
        "format": suffix.removeprefix(".") or "unknown",
        "size_bytes": candidate.stat().st_size,
        "sha256": sha256_file(candidate),
        "inspection": "metadata_only",
        "safe_load_performed": "NO",
        "structure": "",
    }
    try:
        if suffix == ".npy":
            with candidate.open("rb") as handle:
                result["structure"] = json.dumps(_read_npy_header(handle), sort_keys=True)
            result["inspection"] = "npy_header_only"
        elif suffix == ".npz":
            members: list[dict[str, object]] = []
            with zipfile.ZipFile(candidate) as archive:
                for info in sorted(archive.infolist(), key=lambda item: item.filename):
                    member: dict[str, object] = {
                        "name": info.filename,
                        "size": info.file_size,
                        "compressed_size": info.compress_size,
                    }
                    if info.filename.lower().endswith(".npy") and info.file_size <= 1024 * 1024 * 1024:
                        with archive.open(info) as handle:
                            member.update(_read_npy_header(handle))
                    members.append(member)
            result["structure"] = json.dumps(members, sort_keys=True)
            result["inspection"] = "zip_directory_and_npy_headers_only"
        elif suffix in {".h5", ".hdf5"}:
            with candidate.open("rb") as handle:
                magic = handle.read(8)
            result["structure"] = "valid_hdf5_magic" if magic == b"\x89HDF\r\n\x1a\n" else "unrecognized_magic"
            result["inspection"] = "magic_only_h5dump_unavailable"
        elif suffix in {".pkl", ".pickle", ".joblib", ".pt", ".pth"}:
            with candidate.open("rb") as handle:
                prefix = handle.read(16).hex()
            result["structure"] = f"prefix_hex={prefix}"
            result["inspection"] = "opaque_header_only_no_deserialization"
        elif suffix == ".mat":
            with candidate.open("rb") as handle:
                header = handle.read(128)
            result["structure"] = normalized_excerpt(header.decode("latin1", errors="replace"), 120)
            result["inspection"] = "mat_header_only"
        elif suffix in {".parquet", ".feather"}:
            with candidate.open("rb") as handle:
                prefix = handle.read(8).hex()
                handle.seek(max(0, candidate.stat().st_size - 8))
                suffix_bytes = handle.read(8).hex()
            result["structure"] = f"prefix_hex={prefix};suffix_hex={suffix_bytes}"
            result["inspection"] = "container_magic_only"
    except (OSError, ValueError, zipfile.BadZipFile, SyntaxError, struct.error) as exc:
        result["inspection"] = "metadata_error"
        result["structure"] = f"{type(exc).__name__}: {exc}"
    return result


def extract_notebook_text(path: str | Path) -> tuple[str, dict[str, int]]:
    notebook = json.loads(Path(path).read_text(encoding="utf-8"))
    pieces: list[str] = []
    code_cells = 0
    output_blocks = 0
    for cell in notebook.get("cells", []):
        cell_type = str(cell.get("cell_type", ""))
        if cell_type == "code":
            code_cells += 1
        source = cell.get("source", [])
        pieces.append("".join(source) if isinstance(source, list) else str(source))
        for output in cell.get("outputs", []):
            output_blocks += 1
            text = output.get("text", "")
            pieces.append("".join(text) if isinstance(text, list) else str(text))
            data = output.get("data", {})
            for mime, value in sorted(data.items()):
                if mime.startswith("text/") or mime == "application/json":
                    pieces.append("".join(value) if isinstance(value, list) else str(value))
    return "\n".join(pieces), {"code_cells": code_cells, "output_blocks": output_blocks}


def extract_document_text(path: str | Path, pdf_timeout: int = 60) -> tuple[str, str]:
    candidate = Path(path)
    suffix = candidate.suffix.lower()
    if suffix == ".ipynb":
        text, _ = extract_notebook_text(candidate)
        return text, "notebook_json_code_and_saved_outputs"
    if suffix == ".pdf":
        completed = subprocess.run(
            ["pdftotext", "-layout", str(candidate), "-"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=pdf_timeout,
        )
        if completed.returncode != 0:
            error = normalized_excerpt(completed.stderr.decode("utf-8", errors="replace"), 180)
            raise ValueError(f"pdftotext failed: {error}")
        return completed.stdout.decode("utf-8", errors="replace"), "pdftotext_layout"
    if suffix in {".docx", ".odt"}:
        member = "word/document.xml" if suffix == ".docx" else "content.xml"
        with zipfile.ZipFile(candidate) as archive:
            xml = archive.read(member).decode("utf-8", errors="replace")
        return re.sub(r"<[^>]+>", " ", xml), "office_container_xml"
    if suffix in TEXT_SUFFIXES:
        raw = candidate.read_bytes()
        if b"\x00" in raw[:8192]:
            raise ValueError("NUL bytes indicate a binary file")
        return raw.decode("utf-8", errors="replace"), "decoded_text"
    raise ValueError("unsupported text extraction format")


def git_output(repo: str | Path, *arguments: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if binary:
        return completed.stdout
    return completed.stdout.decode("utf-8", errors="replace")


def safe_relative(path: str | Path, root: str | Path) -> str:
    return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()


def iter_files(source: str | Path) -> Iterable[Path]:
    root = Path(source)
    for current, directories, files in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in {".git", "__pycache__"})
        for name in sorted(files):
            yield Path(current) / name
