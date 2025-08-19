#!/usr/bin/env python3
"""
Security scanning script for KEI-Agent Python SDK.

Runs comprehensive security checks including:
- Safety vulnerability scanning
- pip-audit dependency scanning
- Bandit static analysis
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} passed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Main security scanning function."""
    parser = argparse.ArgumentParser(description="Run security scans")
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit with error code if any scan fails",
    )
    args = parser.parse_args()

    # Create reports directory
    reports_dir = Path("security-reports")
    reports_dir.mkdir(exist_ok=True)

    success = True

    # Run safety check
    safety_success = run_command(
        [
            "safety",
            "check",
            "--json",
            "--output",
            str(reports_dir / "safety-report.json"),
        ],
        "Safety vulnerability scan",
    )

    if not safety_success:
        success = False

    # Run pip-audit
    audit_success = run_command(
        [
            "pip-audit",
            "--format=json",
            "--output",
            str(reports_dir / "pip-audit-report.json"),
        ],
        "pip-audit dependency scan",
    )

    if not audit_success:
        success = False

    # Run bandit
    bandit_success = run_command(
        [
            "bandit",
            "-r",
            "kei_agent/",
            "--format",
            "json",
            "--output",
            str(reports_dir / "bandit-report.json"),
            "--severity-level",
            "medium",
            "--confidence-level",
            "medium",
        ],
        "Bandit static analysis",
    )

    if not bandit_success:
        success = False

    if not success and args.fail_on_error:
        print("❌ Security scans failed")
        sys.exit(1)
    elif success:
        print("✅ All security scans passed")
    else:
        print("⚠️ Some security scans failed but continuing")


if __name__ == "__main__":
    main()
