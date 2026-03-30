# CyberShield Toolkit

A defensive cybersecurity toolkit built in Python for GitHub portfolios.

CyberShield Toolkit helps with:
- Password strength auditing
- File hashing and integrity monitoring
- Website security header checks
- Security log scanning

This project is designed for learning, demos, and basic blue-team style security workflows.

## Features

### 1) Password Audit
Analyze password strength using length, character diversity, common-pattern detection, repetition checks, and simple weak-password matching.

Example:
```bash
python main.py password --value "MySecurePass!2026"
```

### 2) File Hashing
Generate a hash for any file using SHA256, SHA1, or MD5.

Example:
```bash
python main.py hash --file README.md --algorithm sha256
```

### 3) Integrity Baseline
Create a baseline of file hashes for a folder and verify later if any files were added, deleted, or modified.

Create a baseline:
```bash
python main.py baseline create --path . --output baseline.json
```

Verify integrity later:
```bash
python main.py baseline verify --path . --baseline baseline.json
```

### 4) Website Security Header Check
Check whether a site returns common defensive HTTP security headers.

Example:
```bash
python main.py headers --url https://example.com
```

### 5) Log Scanner
Scan a log file for suspicious patterns such as failed logins, possible brute force activity, 401/403 spikes, path traversal strings, and SQL error indicators.

Example:
```bash
python main.py logs scan --file sample_logs/sample_auth.log --output report.json
```

## Project Structure

```text
cybershield-toolkit/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── sample_logs/
│   └── sample_auth.log
├── src/
│   └── cybershield/
│       ├── __init__.py
│       ├── headers.py
│       ├── integrity.py
│       ├── log_scanner.py
│       └── password_audit.py
├── tests/
│   ├── test_integrity.py
│   └── test_password_audit.py
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

## Setup

### Option 1: Run directly
```bash
python main.py --help
```

### Option 2: Create a virtual environment
```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

Then run:
```bash
pip install -r requirements.txt
python main.py --help
```

## Sample Commands

```bash
python main.py password --value "Password123!"
python main.py hash --file main.py --algorithm sha256
python main.py baseline create --path . --output baseline.json
python main.py baseline verify --path . --baseline baseline.json
python main.py headers --url https://example.com
python main.py logs scan --file sample_logs/sample_auth.log --output report.json
python -m unittest discover -s tests -v
```

## GitHub Upload Steps

```bash
git init
git add .
git commit -m "Initial commit - CyberShield Toolkit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cybershield-toolkit.git
git push -u origin main
```

## Why this is a good portfolio project

- It is clearly cybersecurity themed
- It is defensive and safe to showcase
- It includes multiple modules instead of a single script
- It has tests and GitHub Actions CI
- It is easy for recruiters and instructors to understand

## Disclaimer

This project is for defensive security education, basic monitoring, and portfolio demonstration. It is not intended for offensive exploitation or unauthorized security testing.

## License

MIT
