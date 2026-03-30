from __future__ import annotations

import ssl
import urllib.error
import urllib.request
from typing import Any

RECOMMENDED_HEADERS = {
    "strict-transport-security": "Helps enforce HTTPS.",
    "content-security-policy": "Reduces XSS and content injection risk.",
    "x-content-type-options": "Prevents MIME-type sniffing.",
    "x-frame-options": "Mitigates clickjacking.",
    "referrer-policy": "Controls referrer information leakage.",
    "permissions-policy": "Restricts powerful browser features.",
}


def analyze_security_headers(url: str, timeout: int = 10) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "CyberShield-Toolkit/1.0"},
    )

    context = ssl.create_default_context()

    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            raw_headers = {key.lower(): value for key, value in response.headers.items()}
            status = getattr(response, "status", None)
    except urllib.error.HTTPError as exc:
        raw_headers = {key.lower(): value for key, value in exc.headers.items()}
        status = exc.code
    except Exception as exc:
        return {
            "url": url,
            "reachable": False,
            "error": str(exc),
        }

    results = {}
    present_count = 0
    missing: list[str] = []

    for header, description in RECOMMENDED_HEADERS.items():
        value = raw_headers.get(header)
        present = value is not None
        if present:
            present_count += 1
        else:
            missing.append(header)
        results[header] = {
            "present": present,
            "value": value,
            "description": description,
        }

    score = round((present_count / len(RECOMMENDED_HEADERS)) * 100)

    if score >= 85:
        rating = "Strong"
    elif score >= 60:
        rating = "Fair"
    elif score >= 35:
        rating = "Weak"
    else:
        rating = "Poor"

    return {
        "url": url,
        "reachable": True,
        "status": status,
        "score": score,
        "rating": rating,
        "checked_headers": results,
        "missing_headers": missing,
    }
