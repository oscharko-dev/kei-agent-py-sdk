#!/usr/bin/env python3
# build_and_publish.py
"""
Build and Publish Script for KEI-Agent Python SDK.

Automatisiert the Build-Prozess and bereitet PyPI-Veröffentlichung before.
Executes Qualitätsprüfungen through and creates Distribution-Packages.
"""

import sys
import subprocess
import shutil
import argparse
from pathlib import Path
from typing import List
import json
import time

# Basis-Directory
BASE_DIR = Path(__file__).parent
DIST_DIR = BASE_DIR / "dist"
BUILD_DIR = BASE_DIR / "build"


def run_command(cmd: List[str], description: str) -> subprocess.CompletedProcess:
    """Executes Command out and gibt detaillierte Ausgabe zurück.

    Args:
        cmd: Command als list
        description: Beschreibung for Ausgabe

    Returns:
        CompletedProcess-Objekt
    """
    print(f"\n[RUN] {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=300,  # 5 Minuten Timeout
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr and result.returncode != 0:
            print(f"STDERR: {result.stderr}")

        if result.returncode == 0:
            print(f"[OK] {description} successful")
        else:
            print(f"[FAIL] {description} failed (Code: {result.returncode})")

        return result

    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        raise
    except FileNotFoundError:
        print(f"❌ Command not gefunden: {cmd[0]}")
        raise


def clean_build_artifacts():
    """Räumt Build-Artefakte auf."""
    print("\n🧹 Räume Build-Artefakte auf...")

    # Patterns for Cleanup
    cleanup_patterns = [
        "build",
        "dist",
        "*.egg-info",
        "htmlcov",
        ".coverage",
        "coverage.xml",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "__pycache__",
    ]

    for pattern in cleanup_patterns:
        pattern_path = BASE_DIR / pattern
        if "*" in pattern:
            # Glob-Pattern
            for path in BASE_DIR.glob(pattern):
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                    print(f"  Deleted: {path}")
        else:
            # Direkter Path
            if pattern_path.exists():
                if pattern_path.is_dir():
                    shutil.rmtree(pattern_path, ignore_errors=True)
                else:
                    pattern_path.unlink()
                print(f"  Deleted: {pattern_path}")

    # Python Cache Files
    for py_cache in BASE_DIR.rglob("__pycache__"):
        shutil.rmtree(py_cache, ignore_errors=True)
        print(f"  Deleted: {py_cache}")

    for pyc_file in BASE_DIR.rglob("*.pyc"):
        pyc_file.unlink()

    for pyo_file in BASE_DIR.rglob("*.pyo"):
        pyo_file.unlink()

    print("✅ Build-Artefakte aufgeräumt")


def run_quality_checks() -> int:
    """Executes Code-Qualitätsprüfungen out.

    Returns:
        Anzahl failed Prüfungen
    """
    print("\n🔍 Führe Code-Qualitätsprüfungen out...")

    checks = [
        (["python3", "-m", "ruff", "check", "kei_agent/"], "Ruff Linting"),
        (
            ["python3", "-m", "mypy", "kei_agent/", "--no-error-summary"],
            "MyPy Type Checking",
        ),
    ]

    total_errors = 0

    for cmd, description in checks:
        result = run_command(cmd, description)
        if result.returncode != 0:
            total_errors += 1

    return total_errors


def run_tests() -> int:
    """Executes Tests out.

    Returns:
        Test-Rückgabecode
    """
    print("\n🧪 Führe Tests out...")

    cmd = ["python3", "-m", "pytest", "tests/", "-v", "--tb=short"]
    result = run_command(cmd, "Unit Tests")

    return result.returncode


def validate_package_metadata():
    """Validates Package-metadata."""
    print("\n📋 Validate Package-metadata...")

    # pyproject.toml prüfen
    pyproject_file = BASE_DIR / "pyproject.toml"
    if not pyproject_file.exists():
        raise FileNotFoundError("pyproject.toml not gefunden")

    # README.md prüfen
    readme_file = BASE_DIR / "README.md"
    if not readme_file.exists():
        raise FileNotFoundError("README.md not gefunden")

    # LICENSE prüfen
    license_file = BASE_DIR / "LICENSE"
    if not license_file.exists():
        print("⚠️ LICENSE-File not gefunden")

    # MANIFEST.in prüfen
    manifest_file = BASE_DIR / "MANIFEST.in"
    if not manifest_file.exists():
        print("⚠️ MANIFEST.in not gefunden")

    # Version out pyproject.toml extrahieren
    try:
        try:
            import tomllib  # type: ignore
        except ImportError:
            import tomli as tomllib  # type: ignore

        with open(pyproject_file, "rb") as f:
            pyproject_data = tomllib.load(f)

        version = pyproject_data.get("project", {}).get("version")
        if not version:
            raise ValueError("Version not in pyproject.toml gefunden")

        print(f"📦 Package Version: {version}")

    except Exception as e:
        print(f"⚠️ Error during Version-Extraktion: {e}")

    print("✅ Package-metadata validated")


def build_package():
    """Creates Distribution-Packages."""
    print("\n🔨 Erstelle Distribution-Packages...")

    # Build-Directory erstellen
    DIST_DIR.mkdir(exist_ok=True)

    # Build ausführen
    result = run_command(["python3", "-m", "build"], "Package Build")

    if result.returncode == 0:
        print("✅ Package Build successful")

        # Created Files auflisten
        if DIST_DIR.exists():
            print("\n📦 Created Files:")
            for file in DIST_DIR.iterdir():
                if file.is_file():
                    size = file.stat().st_size
                    print(f"  {file.name} ({size:,} bytes)")
    else:
        print("❌ Package Build failed")
        sys.exit(1)


def create_build_report() -> dict:
    """Creates detaillierten Build-Report.

    Returns:
        Build-Report als Dictionary
    """
    print("\n📊 Erstelle Build-Report...")

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "build_status": "success",
        "files": [],
        "metadata": {},
    }

    # Package-Info sammeln
    try:
        try:
            import tomllib  # type: ignore
        except ImportError:
            import tomli as tomllib  # type: ignore

        pyproject_file = BASE_DIR / "pyproject.toml"
        with open(pyproject_file, "rb") as f:
            pyproject_data = tomllib.load(f)

        project_info = pyproject_data.get("project", {})
        report["metadata"] = {
            "name": project_info.get("name"),
            "version": project_info.get("version"),
            "description": project_info.get("description"),
            "authors": project_info.get("authors", []),
        }
    except Exception as e:
        print(f"⚠️ Error during Lesen the Package-Info: {e}")

    # Created Dateien
    if DIST_DIR.exists():
        for file in DIST_DIR.glob("*"):
            report["files"].append(
                {
                    "name": file.name,
                    "size": file.stat().st_size,
                    "path": str(file.relative_to(BASE_DIR)),
                }
            )

    # Report speichern
    report_file = BASE_DIR / "build-report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"✅ Build-Report created: {report_file}")
    return report


def main():
    """Main Function."""
    parser = argparse.ArgumentParser(
        description="Build and Publish Script for KEI-Agent Python SDK"
    )

    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Nur Build ausführen, ohne Tests and Qualitätsprüfungen",
    )
    parser.add_argument("--skip-tests", action="store_true", help="Tests überspringen")
    parser.add_argument(
        "--skip-quality", action="store_true", help="Qualitätsprüfungen überspringen"
    )
    parser.add_argument(
        "--clean-only", action="store_true", help="Nur Cleanup ausführen"
    )

    args = parser.parse_args()

    print("🏗️ KEI-Agent Python SDK Build Script")
    print("=" * 50)

    try:
        # Cleanup
        clean_build_artifacts()

        if args.clean_only:
            print("✅ Cleanup completed")
            return

        # Package-metadata validieren
        validate_package_metadata()

        if not args.build_only:
            # Qualitätsprüfungen
            if not args.skip_quality:
                quality_errors = run_quality_checks()
                if quality_errors > 0:
                    print(f"❌ {quality_errors} Qualitätsprüfung(en) failed")
                    sys.exit(1)

            # Tests
            if not args.skip_tests:
                test_result = run_tests()
                if test_result != 0:
                    print("❌ Tests failed")
                    sys.exit(1)

        # Package Build
        build_package()

        # Build-Report
        create_build_report()

        print("\n🎉 Build successful completed!")

    except KeyboardInterrupt:
        print("\n❌ Build abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
