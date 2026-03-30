from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cybershield.headers import analyze_security_headers
from cybershield.integrity import create_baseline, hash_file, verify_baseline
from cybershield.log_scanner import scan_log_file
from cybershield.password_audit import audit_password


def handle_password(args: argparse.Namespace) -> int:
    result = audit_password(args.value)
    print(json.dumps(result, indent=2))
    return 0


def handle_hash(args: argparse.Namespace) -> int:
    digest = hash_file(Path(args.file), args.algorithm)
    print(json.dumps({
        "file": str(Path(args.file).resolve()),
        "algorithm": args.algorithm.lower(),
        "hash": digest,
    }, indent=2))
    return 0


def handle_baseline_create(args: argparse.Namespace) -> int:
    baseline = create_baseline(Path(args.path))
    output_path = Path(args.output)
    output_path.write_text(json.dumps(baseline, indent=2), encoding="utf-8")
    print(f"Baseline saved to {output_path.resolve()}")
    return 0


def handle_baseline_verify(args: argparse.Namespace) -> int:
    baseline_path = Path(args.baseline)
    baseline_data = json.loads(baseline_path.read_text(encoding="utf-8"))
    result = verify_baseline(Path(args.path), baseline_data)
    print(json.dumps(result, indent=2))
    return 0


def handle_headers(args: argparse.Namespace) -> int:
    result = analyze_security_headers(args.url, timeout=args.timeout)
    print(json.dumps(result, indent=2))
    return 0


def handle_logs_scan(args: argparse.Namespace) -> int:
    result = scan_log_file(Path(args.file))
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Report saved to {output_path.resolve()}")
    else:
        print(json.dumps(result, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CyberShield Toolkit - defensive cybersecurity portfolio project"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    password_parser = subparsers.add_parser("password", help="Audit password strength")
    password_parser.add_argument("--value", required=True, help="Password to analyze")
    password_parser.set_defaults(func=handle_password)

    hash_parser = subparsers.add_parser("hash", help="Hash a file")
    hash_parser.add_argument("--file", required=True, help="Path to file")
    hash_parser.add_argument(
        "--algorithm",
        default="sha256",
        choices=["sha256", "sha1", "md5"],
        help="Hash algorithm",
    )
    hash_parser.set_defaults(func=handle_hash)

    baseline_parser = subparsers.add_parser("baseline", help="Create or verify integrity baseline")
    baseline_subparsers = baseline_parser.add_subparsers(dest="baseline_command", required=True)

    baseline_create_parser = baseline_subparsers.add_parser("create", help="Create baseline")
    baseline_create_parser.add_argument("--path", required=True, help="Directory path to scan")
    baseline_create_parser.add_argument("--output", required=True, help="Output JSON file")
    baseline_create_parser.set_defaults(func=handle_baseline_create)

    baseline_verify_parser = baseline_subparsers.add_parser("verify", help="Verify baseline")
    baseline_verify_parser.add_argument("--path", required=True, help="Directory path to scan")
    baseline_verify_parser.add_argument("--baseline", required=True, help="Baseline JSON file")
    baseline_verify_parser.set_defaults(func=handle_baseline_verify)

    headers_parser = subparsers.add_parser("headers", help="Analyze HTTP security headers")
    headers_parser.add_argument("--url", required=True, help="Target URL")
    headers_parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    headers_parser.set_defaults(func=handle_headers)

    logs_parser = subparsers.add_parser("logs", help="Scan security logs")
    logs_subparsers = logs_parser.add_subparsers(dest="logs_command", required=True)

    logs_scan_parser = logs_subparsers.add_parser("scan", help="Scan log file")
    logs_scan_parser.add_argument("--file", required=True, help="Log file path")
    logs_scan_parser.add_argument("--output", help="Optional JSON report output path")
    logs_scan_parser.set_defaults(func=handle_logs_scan)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
