from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IGNORED_DIRS = {".git", "__pycache__", ".venv", "venv"}
IGNORED_FILES = {"baseline.json", "report.json"}


def hash_file(file_path: Path, algorithm: str = "sha256") -> str:
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    algorithm = algorithm.lower()
    if algorithm not in {"sha256", "sha1", "md5"}:
        raise ValueError("Unsupported algorithm. Choose sha256, sha1, or md5.")

    hasher = hashlib.new(algorithm)
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _iter_files(base_path: Path):
    for path in base_path.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file() and path.name not in IGNORED_FILES:
            yield path


def create_baseline(base_path: Path) -> dict[str, Any]:
    base_path = Path(base_path).resolve()
    if not base_path.is_dir():
        raise NotADirectoryError(f"Directory not found: {base_path}")

    files: dict[str, dict[str, Any]] = {}
    for file_path in _iter_files(base_path):
        rel_path = str(file_path.relative_to(base_path))
        files[rel_path] = {
            "sha256": hash_file(file_path, "sha256"),
            "size": file_path.stat().st_size,
        }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_path": str(base_path),
        "algorithm": "sha256",
        "file_count": len(files),
        "files": files,
    }


def verify_baseline(base_path: Path, baseline_data: dict[str, Any]) -> dict[str, Any]:
    base_path = Path(base_path).resolve()
    current = create_baseline(base_path)

    expected_files = baseline_data.get("files", {})
    current_files = current.get("files", {})

    expected_set = set(expected_files.keys())
    current_set = set(current_files.keys())

    added = sorted(current_set - expected_set)
    deleted = sorted(expected_set - current_set)
    modified = sorted(
        path
        for path in expected_set & current_set
        if expected_files[path].get("sha256") != current_files[path].get("sha256")
    )

    return {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "base_path": str(base_path),
        "is_clean": not (added or deleted or modified),
        "summary": {
            "added": len(added),
            "deleted": len(deleted),
            "modified": len(modified),
        },
        "added_files": added,
        "deleted_files": deleted,
        "modified_files": modified,
    }
