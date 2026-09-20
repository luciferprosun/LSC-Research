"""Deterministic evidence-freeze construction and verification."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

from lsc_kernel.io.hashes import sha256_file


def build_evidence_freeze(
    root: Path,
    records: Iterable[Mapping[str, object]],
    *,
    acquisition_timestamp: str,
) -> dict[str, object]:
    frozen: list[dict[str, object]] = []
    for record in sorted(records, key=lambda item: (str(item["object_id"]), str(item["path"]))):
        relative = Path(str(record["path"]))
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f"Evidence path is missing or escapes repository: {relative}")
        frozen.append(
            {
                "path": relative.as_posix(),
                "object_id": str(record["object_id"]),
                "sha256": sha256_file(path),
                "provenance_class": str(record["provenance_class"]),
                "source_identifier": str(record["source_identifier"]),
                "acquisition_timestamp": acquisition_timestamp,
                "adjudication": str(record["adjudication"]),
            }
        )
    return {
        "schema_version": "1.0.0",
        "policy": "Hash snapshot only; inclusion does not promote evidence to frozen numerical input.",
        "records": frozen,
    }


def verify_evidence_freeze(root: Path, freeze: Mapping[str, object]) -> bool:
    records = freeze.get("records")
    if not isinstance(records, list):
        return False
    for record in records:
        if not isinstance(record, Mapping):
            return False
        path = (root / str(record.get("path", ""))).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            return False
        if sha256_file(path) != record.get("sha256"):
            return False
    return True
