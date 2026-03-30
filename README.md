# CyberShield Toolkit

CyberShield Toolkit is a Python-based cybersecurity project that I built to practice defensive security concepts and create something useful for my GitHub portfolio.

The goal of this project was to combine a few common blue-team style tasks into one toolkit, including password auditing, file hashing, file integrity checking, HTTP security header inspection, and basic log analysis.

## What this project does

This toolkit includes the following features:

- Password strength auditing
- File hashing with common algorithms
- File integrity baseline creation and verification
- Website security header checks
- Security log scanning for suspicious activity

## Features

### 1. Password Audit

This feature checks the strength of a password based on things like length, character variety, repeated patterns, and weak/common password indicators.

**Example:**

```bash
python main.py password --value "MySecurePass!2026"
```
## 2. File Hashing

This feature generates a file hash using SHA256, SHA1, or MD5.

**Example:**

```bash
python main.py hash --file README.md --algorithm sha256
```

## 3. Integrity Baseline

This feature lets me create a baseline of file hashes for a folder and later verify whether any files were added, removed, or modified.

**Create a baseline:**

```bash
python main.py baseline create --path . --output baseline.json
```

**Verify the baseline:**

```bash
python main.py baseline verify --path . --baseline baseline.json
```

## 4. Website Security Header Check

This feature checks whether a website returns important HTTP security headers that help improve browser-side protection.

**Example:**

```bash
python main.py headers --url https://example.com
```

## 5. Log Scanner

This feature scans log files for suspicious patterns such as failed logins, possible brute-force attempts, 401/403 activity, path traversal strings, and SQL-related error patterns.

**Example:**

```bash
python main.py logs scan --file sample_logs/sample_auth.log --output report.json
```

## Why I Built This Project

I wanted to create a cybersecurity project that was practical, defensive in nature, and simple enough to understand and demonstrate on GitHub. Instead of making just one small script, I decided to build a toolkit with multiple security-related functions in one project.

This project also helped me practice:

- Python scripting
- Working with files and hashing
- Basic log analysis
- Organizing code into modules
- Writing unit tests
- Structuring a project for GitHub

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

### Run Directly

```bash
python main.py --help
```

### Optional: Create a Virtual Environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Then install dependencies:

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

## Future Improvements

Some improvements I would like to add in the future are:

- A simple web interface
- More advanced password analysis
- Better log parsing with severity levels
- Support for additional security headers and recommendations
- Exporting results in different formats

## Why This Project Is Useful for My Portfolio

I think this is a strong portfolio project because it shows:

- Interest in cybersecurity
- Practical Python skills
- Modular project structure
- Testing and CI usage
- A defensive and professional security focus
