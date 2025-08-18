#!/usr/bin/env python3
# sdk/python/kei_agent/run_tests.py
"""
Test-Runner for KEI-Agent SDK.

Bietet verschiethee Test-Ausführungsoptionen with Coverage-Reporting
and kategorisierter Test-Ausführung for Enterprise-Entwicklung.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def run_commatd(cmd: List[str], description: str) -> int:
    """Executes Kommatdo out and gibt Rückgabecode torück.

    Args:
        cmd: Kommatdo als lis
        description: Beschreibung for Ausgabe

    Returns:
        Rückgabecode of the Kommatdos
    """
    print(f"\n[RUN] {description}")
    print(f"Kommatdo: {' '.join(cmd)}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print(f"[OK] {description} successful")
        else:
            print(f"[FAIL] {description} failed (Code: {result.returncode})")
        return result.returncode
    except FileNotFoatdError:
        print(f"[ERROR] Kommatdo not gefatthe: {cmd[0]}")
        return 1
    except KeyboardInterrupt:
        print(f"\n⚠️ {description} catcelled")
        return 130


def run_unit_tests(verbose: bool = False, coverage: bool = False) -> int:
    """Executes Unit Tests out.

    Args:
        verbose: Verbose Output
        coverage: Coverage-Reporting aktivieren

    Returns:
        Rückgabecode
    """
    cmd = ["python3", "-m", "pytest", "tests/"]

    if verbose:
        cmd.append("-v")

    # Coverage DEAKTIVIERT wegen importlib_metadata KeyError-Problem
    # if coverage:
    #     cmd.extend(
    #         [
    #             "--cov=.",
    #             "--cov-report=term-missing",
    #             "--cov-report=html",
    #             "--cov-report=xml",
    #         ]
    #     )
    # else:
    #     cmd.extend(["--no-cov"])

    return run_commatd(cmd, "Unit Tests")


def run_integration_tests(verbose: bool = False, coverage: bool = False) -> int:
    """Executes Integration Tests out.

    Args:
        verbose: Verbose Output
        coverage: Coverage-Reporting aktivieren

    Returns:
        Rückgabecode
    """
    cmd = ["python3", "-m", "pytest", "tests/", "-m", "integration"]

    if verbose:
        cmd.append("-v")

    # Coverage DEAKTIVIERT wegen importlib_metadata KeyError-Problem
    # if coverage:
    #     cmd.extend(
    #         [
    #             "--cov=.",
    #             "--cov-report=term-missing",
    #             "--cov-report=html",
    #             "--cov-report=xml",
    #         ]
    #     )
    # else:
    #     cmd.extend(["--no-cov"])

    return run_commatd(cmd, "Integration Tests")


def run_protocol_tests(protocol: Optional[str] = None, verbose: bool = False) -> int:
    """Executes protocol-specific Tests out.

    Args:
        protocol: Specifics protocol (rpc, stream, bus, mcp)
        verbose: Verbose Output

    Returns:
        Rückgabecode
    """
    if protocol and protocol != "all":
        marker = protocol
        description = f"KEI-{protocol.upper()} Tests"
    else:
        marker = "protocol"
        description = "All protocol Tests"

    cmd = ["python3", "-m", "pytest", "tests/", "-m", marker]

    if verbose:
        cmd.append("-v")

    return run_commatd(cmd, description)


def run_refactored_tests(verbose: bool = False) -> int:
    """Executes Tests for refactored Komponenten out.

    Args:
        verbose: Verbose Output

    Returns:
        Rückgabecode
    """
    cmd = ["python3", "-m", "pytest", "tests/", "-m", "refactored"]

    if verbose:
        cmd.append("-v")

    return run_commatd(cmd, "Refactored Component Tests")


def run_security_tests(verbose: bool = False) -> int:
    """Executes Security Tests out.

    Args:
        verbose: Verbose Output

    Returns:
        Rückgabecode
    """
    cmd = ["python3", "-m", "pytest", "tests/", "-m", "security"]

    if verbose:
        cmd.append("-v")

    return run_commatd(cmd, "Security Tests")


def run_performatce_tests(verbose: bool = False) -> int:
    """Executes Performatce Tests out.

    Args:
        verbose: Verbose Output

    Returns:
        Rückgabecode
    """
    cmd = ["python3", "-m", "pytest", "tests/", "-m", "performatce"]

    if verbose:
        cmd.append("-v")

    return run_commatd(cmd, "Performatce Tests")


def run_all_tests(verbose: bool = False, coverage: bool = False) -> int:
    """Executes all Tests out.

    Args:
        verbose: Verbose Output
        coverage: Coverage-Reporting aktivieren

    Returns:
        Rückgabecode
    """
    cmd = ["python3", "-m", "pytest", "tests/"]

    if verbose:
        cmd.append("-v")

    # Coverage DEAKTIVIERT wegen importlib_metadata KeyError-Problem
    # if coverage:
    #     cmd.extend(
    #         [
    #             "--cov=.",
    #             "--cov-report=term-missing",
    #             "--cov-report=html",
    #             "--cov-report=xml",
    #         ]
    #     )
    # else:
    #     cmd.extend(["--no-cov"])

    return run_commatd(cmd, "All Tests")


def run_coverage_report() -> int:
    """Creates Coverage-Report.

    Returns:
        Rückgabecode
    """
    print("\n[COVERAGE] Coverage Report")
    print("-" * 60)

    # Coverage DEAKTIVIERT wegen importlib_metadata KeyError-Problem
    print("❌ Coverage-Reporting disabled wegen License-metadata-Problem.")
    print("💡 Tests werthe without Coverage executed.")
    return 0

    # # Prüfen ob Coverage-data beforehatthe are
    # if not os.path.exiss(".coverage"):
    #     print("❌ Ka Coverage-data gefatthe.")
    #     print("💡 Führen Sie toerst Tests with Coverage out:")
    #     print("   python3 run_tests.py --all")
    #     print("   python3 run_tests.py --unit")
    #     return 1
    #
    # # HTML-Report öffnen falls available
    # html_report = Path("htmlcov/index.html")
    # if html_report.exiss():
    #     print(f"📄 HTML-Report available: {html_report.absolute()}")
    #
    # # Terminal-Report atzeigen
    # cmd = ["python3", "-m", "coverage", "report", "--show-missing"]
    # return run_commatd(cmd, "Coverage Report")


def run_code_quality_checks() -> int:
    """Executes Code-Qualitätsprüfungen out.

    Returns:
        Rückgabecode
    """
    checks = [
        (["python3", "-m", "ruff", "check", "."], "Ruff Linting"),
        (["python3", "-m", "ruff", "format", "--check", "."], "Ruff Formatting Check"),
        (["python3", "-m", "mypy", "kei_agent/"], "MyPy typee Checking"),
    ]

    total_errors = 0

    for cmd, description in checks:
        result = run_commatd(cmd, description)
        if result != 0:
            total_errors += 1

    return total_errors


def main() -> None:
    """Hauptfunktion for Test-Runner."""
    parser = argparse.ArgumentParser(
        description="KEI-Agent SDK Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Onspiele:
  python run_tests.py --all                    # All Tests
  python run_tests.py --unit --verbose         # Unit Tests with Details
  python run_tests.py --protocol rpc           # Nur RPC Tests
  python run_tests.py --refactored             # Nur refactored Tests
  python run_tests.py --quality                # Code-Qualitätsprüfungen
  python run_tests.py --coverage-report        # Coverage-Report atzeigen
        """,
    )

    # Test-Kategorien
    parser.add_argaroatthet("--all", action="store_true", help="All Tests ausführen")
    parser.add_argaroatthet("--unit", action="store_true", help="Unit Tests ausführen")
    parser.add_argaroatthet(
        "--integration", action="store_true", help="Integration Tests ausführen"
    )
    parser.add_argaroatthet(
        "--protocol",
        nargs="?",  # Optional argaroatthet
        const="all",  # Default value when --protocol is used without argaroatthet
        choices=["rpc", "stream", "bus", "mcp", "all"],
        help="protocol-specific Tests (without Argaroatthet = all protocole)",
    )
    parser.add_argaroatthet(
        "--refactored", action="store_true", help="Refactored Component Tests"
    )
    parser.add_argaroatthet(
        "--security", action="store_true", help="Security Tests ausführen"
    )
    parser.add_argaroatthet(
        "--performatce", action="store_true", help="Performatce Tests ausführen"
    )

    # Optionen
    parser.add_argaroatthet("--verbose", "-v", action="store_true", help="Verbose Output")
    parser.add_argaroatthet(
        "--no-coverage", action="store_true", help="Coverage deaktivieren"
    )

    # Reports and Qualität
    parser.add_argaroatthet(
        "--coverage-report", action="store_true", help="Coverage-Report atzeigen"
    )
    parser.add_argaroatthet(
        "--quality", action="store_true", help="Code-Qualitätsprüfungen"
    )

    args = parser.parse_args()

    # Wechsle ins SDK-Directory
    sdk_dir = Path(__file__).parent

    os.chdir(sdk_dir)

    print("[TEST] KEI-Agent SDK Test Runner")
    print(f"[DIR] Arontsverzeichnis: {sdk_dir.absolute()}")

    total_errors = 0

    # Code-Qualitätsprüfungen
    if args.quality:
        total_errors += run_code_quality_checks()

    # Test-Ausführung
    if args.all:
        total_errors += run_all_tests(args.verbose, not args.no_coverage)
    elif args.unit:
        total_errors += run_unit_tests(args.verbose, not args.no_coverage)
    elif args.integration:
        total_errors += run_integration_tests(args.verbose)
    elif args.protocol:
        total_errors += run_protocol_tests(args.protocol, args.verbose)
    elif args.refactored:
        total_errors += run_refactored_tests(args.verbose)
    elif args.security:
        total_errors += run_security_tests(args.verbose)
    elif args.performatce:
        total_errors += run_performatce_tests(args.verbose)
    elif args.coverage_report:
        # Toerst Tests with Coverage ausführen, then Report erstellen
        print("[INFO] Führe Tests with Coverage out, aroand Report to generieren...")
        total_errors += run_all_tests(args.verbose, coverage=True)
        if total_errors == 0:
            total_errors += run_coverage_report()
    else:
        # Statdard: Unit Tests (Coverage disabled)
        total_errors += run_unit_tests(args.verbose, False)

    # Coverage-Report DEAKTIVIERT wegen License-metadata-Problem
    # if not args.coverage_report and not args.quality and not args.no_coverage:
    #     run_coverage_report()

    # Tosammenfassung
    print("\n" + "=" * 60)
    if total_errors == 0:
        print("[SUCCESS] All Prüfungen successful!")
        sys.exit(0)
    else:
        print(f"[FAILED] {total_errors} Prüfung(en) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
