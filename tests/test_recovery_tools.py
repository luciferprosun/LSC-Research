from __future__ import annotations

import csv
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))

from recovery_lib import (  # noqa: E402
    REGISTRY_COLUMNS,
    build_registry,
    duplicate_hash_groups,
    sha256_file,
    validate_registry_rows,
)


def write_registry_source(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REGISTRY_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def row(**overrides: str) -> dict[str, str]:
    value = {column: "" for column in REGISTRY_COLUMNS}
    value.update(
        {
            "artifact_id": "candidate-1",
            "artifact_type": "fixture",
            "parameter_or_role": "fixture",
            "value_or_summary": "fixture",
            "units": "NOT_APPLICABLE",
            "source_path": "first/value.json",
            "git_commit": "fixture",
            "git_tag": "NOT_TAGGED",
            "timestamp_if_known": "UNKNOWN",
            "data_exposure_status": "UNKNOWN_EXPOSURE",
            "classification": "UNVERIFIED",
            "confidence": "LOW",
            "notes": "test fixture",
        }
    )
    value.update(overrides)
    return value


class RecoveryToolTests(unittest.TestCase):
    def test_sha256_is_correct(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "value.bin"
            path.write_bytes(b"abc")
            self.assertEqual(sha256_file(path), hashlib.sha256(b"abc").hexdigest())

    def test_registry_output_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = root / "archive"
            archive.mkdir()
            (archive / "first").mkdir()
            (archive / "first" / "value.json").write_text("one", encoding="utf-8")
            source = root / "source.csv"
            write_registry_source(source, [row()])
            first = root / "first.csv"
            second = root / "second.csv"
            build_registry(source, first, archive, root)
            build_registry(source, second, archive, root)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_duplicate_content_is_reported(self) -> None:
        digest = hashlib.sha256(b"same").hexdigest()
        rows = [row(artifact_id="a", sha256=digest), row(artifact_id="b", sha256=digest)]
        self.assertEqual(duplicate_hash_groups(rows), [["a", "b"]])

    def test_same_filename_with_different_hashes_is_not_merged(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = root / "archive"
            (archive / "first").mkdir(parents=True)
            (archive / "second").mkdir(parents=True)
            (archive / "first" / "value.json").write_text("one", encoding="utf-8")
            (archive / "second" / "value.json").write_text("two", encoding="utf-8")
            source = root / "source.csv"
            rows = [
                row(artifact_id="first"),
                row(artifact_id="second", source_path="second/value.json"),
            ]
            write_registry_source(source, rows)
            result = build_registry(source, root / "result.csv", archive, root)
            self.assertEqual(len(result), 2)
            self.assertEqual(len({item["sha256"] for item in result}), 2)

    def test_classification_must_be_one_of_five_official_values(self) -> None:
        invalid = row(classification="UNVERIFIED_CONFLICT")
        with self.assertRaises(ValueError):
            validate_registry_rows([invalid])

    def test_missing_is_never_replaced_by_similarly_named_file(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = root / "archive"
            archive.mkdir()
            (archive / "theta.json").write_text("candidate", encoding="utf-8")
            source = root / "source.csv"
            write_registry_source(
                source,
                [
                    row(
                        artifact_id="missing-theta",
                        classification="MISSING",
                        source_path="NOT_FOUND",
                        value_or_summary="NOT_RECOVERED",
                        sha256="NOT_APPLICABLE",
                    )
                ],
            )
            result = build_registry(source, root / "result.csv", archive, root)
            self.assertEqual(result[0]["classification"], "MISSING")
            self.assertEqual(result[0]["source_path"], "NOT_FOUND")
            self.assertEqual(result[0]["sha256"], "NOT_APPLICABLE")


if __name__ == "__main__":
    unittest.main()
