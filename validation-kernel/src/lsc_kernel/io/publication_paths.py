"""Detect machine-local filesystem paths in newly produced artifacts."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


_POSIX_HOME = "/" + "home" + "/"
_MACOS_HOME = "/" + "Users" + "/"
_FILE_SCHEME = "file" + "://"
_WINDOWS_USER = re.compile(r"[A-Za-z]:[\\/]Users[\\/]", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class LocalPathFinding:
    path: str
    line: int
    pattern: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def scan_publication_paths(paths: Iterable[Path], *, root: Path) -> tuple[LocalPathFinding, ...]:
    findings: list[LocalPathFinding] = []
    for path in sorted(set(paths)):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            matches = (
                ("POSIX_HOME", _POSIX_HOME in line),
                ("MACOS_HOME", _MACOS_HOME in line),
                ("FILE_URI", _FILE_SCHEME in line),
                ("WINDOWS_USER", bool(_WINDOWS_USER.search(line))),
            )
            for pattern, matched in matches:
                if matched:
                    findings.append(
                        LocalPathFinding(path.as_posix().removeprefix(root.as_posix() + "/"), line_number, pattern)
                    )
    return tuple(findings)
