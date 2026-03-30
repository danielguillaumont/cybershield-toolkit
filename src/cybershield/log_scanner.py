from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

PATTERNS = {
    "failed_login": re.compile(r"failed password|authentication failed|login failed", re.IGNORECASE),
    "permission_denied": re.compile(r"permission denied|access denied", re.IGNORECASE),
    "http_401_403": re.compile(r"\b(401|403)\b"),
    "path_traversal": re.compile(r"\.\./|\.\.\\"),
    "sql_error": re.compile(r"sql syntax|mysql|postgres|sqlite|odbc|database error", re.IGNORECASE),
    "admin_login": re.compile(r"admin login|root login|sudo", re.IGNORECASE),
}

IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def scan_log_file(file_path: Path) -> dict[str, Any]:
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Log file not found: {file_path}")

    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    findings: dict[str, list[dict[str, Any]]] = {key: [] for key in PATTERNS}
    ip_counter: Counter[str] = Counter()

    for index, line in enumerate(lines, start=1):
        for category, pattern in PATTERNS.items():
            if pattern.search(line):
                findings[category].append({"line_number": index, "line": line.strip()})

        for ip_address in IP_PATTERN.findall(line):
            if PATTERNS["failed_login"].search(line) or PATTERNS["http_401_403"].search(line):
                ip_counter[ip_address] += 1

    potential_bruteforce = [
        {"ip": ip, "failed_events": count}
        for ip, count in ip_counter.items()
        if count >= 3
    ]

    severity = "Low"
    total_hits = sum(len(items) for items in findings.values())
    if potential_bruteforce or len(findings["path_traversal"]) >= 1 or len(findings["sql_error"]) >= 1:
        severity = "High"
    elif total_hits >= 5:
        severity = "Medium"

    return {
        "file": str(file_path.resolve()),
        "total_lines": len(lines),
        "severity": severity,
        "summary": {key: len(value) for key, value in findings.items()},
        "potential_bruteforce_sources": potential_bruteforce,
        "findings": findings,
    }


def findings_to_json(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2)
