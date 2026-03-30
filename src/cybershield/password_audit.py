from __future__ import annotations

import re
from typing import Any

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "123456789",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
    "abc123",
}

SEQUENTIAL_PATTERNS = [
    "1234",
    "2345",
    "3456",
    "4567",
    "5678",
    "6789",
    "abcd",
    "qwerty",
]


def _has_repeated_characters(password: str) -> bool:
    return bool(re.search(r"(.)\1\1", password))


def audit_password(password: str) -> dict[str, Any]:
    score = 0
    findings: list[str] = []
    suggestions: list[str] = []

    if not password:
        return {
            "score": 0,
            "rating": "Very Weak",
            "findings": ["Password is empty."],
            "suggestions": ["Use a password with at least 12-16 characters."],
        }

    length = len(password)
    lower = bool(re.search(r"[a-z]", password))
    upper = bool(re.search(r"[A-Z]", password))
    digit = bool(re.search(r"\d", password))
    special = bool(re.search(r"[^A-Za-z0-9]", password))

    if length >= 8:
        score += 10
    else:
        findings.append("Password is shorter than 8 characters.")
        suggestions.append("Increase the password length to at least 12 characters.")

    if length >= 12:
        score += 20
    if length >= 16:
        score += 15

    for label, present in {
        "lowercase": lower,
        "uppercase": upper,
        "digits": digit,
        "special characters": special,
    }.items():
        if present:
            score += 10
        else:
            findings.append(f"Missing {label}.")
            suggestions.append(f"Add {label} to improve complexity.")

    lowered = password.lower()
    if lowered in COMMON_PASSWORDS:
        findings.append("Password matches a very common password pattern.")
        suggestions.append("Avoid common passwords and use a unique passphrase.")
        score -= 40

    if any(pattern in lowered for pattern in SEQUENTIAL_PATTERNS):
        findings.append("Password contains a simple sequential pattern.")
        suggestions.append("Avoid predictable sequences like 1234 or abcd.")
        score -= 15

    if _has_repeated_characters(password):
        findings.append("Password contains repeated characters.")
        suggestions.append("Reduce repeated characters and use a less predictable pattern.")
        score -= 10

    if " " in password:
        findings.append("Password contains spaces.")
        suggestions.append("Consider using a clean passphrase without accidental spaces.")
        score -= 5

    score = max(0, min(score, 100))

    if score >= 85:
        rating = "Strong"
    elif score >= 60:
        rating = "Moderate"
    elif score >= 35:
        rating = "Weak"
    else:
        rating = "Very Weak"

    if not findings:
        findings.append("No major weaknesses detected by local rules.")
    if not suggestions:
        suggestions.append("Store the password in a password manager and enable MFA where possible.")

    return {
        "score": score,
        "rating": rating,
        "length": length,
        "has_lowercase": lower,
        "has_uppercase": upper,
        "has_digits": digit,
        "has_special_characters": special,
        "findings": sorted(set(findings)),
        "suggestions": sorted(set(suggestions)),
    }
