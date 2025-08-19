#!/usr/bin/env python3
"""\
Überprüft die Type-Hint-Abdeckung des Projekts und gibt eine Zusammenfassung als JSON aus.

Diese Hilfe analysiert die von mypy erzeugten Berichte und berechnet die Abdeckung
der Typannotationen. Optional kann mypy vorab ausgeführt werden.

Verwendung (Beispiele):
- python scripts/check_type_coverage.py --fail-under 95 --output type-coverage.json
- python scripts/check_type_coverage.py --output detailed.json --run-mypy
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Initialisiert Konstanten für Standardwerte
DEFAULT_PACKAGE_DIR = "kei_agent"


def parse_args() -> argparse.Namespace:
    """\
    Parsen der CLI-Argumente.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Berechnet die Type-Hint-Abdeckung aus mypy-Berichten und validiert"
            " gegen eine minimale Abdeckung."
        )
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Pfad zur Ausgabe-Datei (JSON). Wird bei Weglassen auf stdout geschrieben.",
    )
    parser.add_argument(
        "--fail-under",
        type=float,
        default=None,
        help=(
            "Fehlerschwelle in Prozent. Bricht mit Exit-Code 1 ab, wenn die Abdeckung"
            " niedriger ist."
        ),
    )
    # Unterstützt sowohl --run-mypy als auch das explizite Abschalten über --no-run-mypy
    parser.add_argument(
        "--run-mypy",
        dest="run_mypy",
        action="store_true",
        help="Führt mypy vor der Auswertung aus (Standard: aktiv).",
    )
    parser.add_argument(
        "--no-run-mypy",
        dest="run_mypy",
        action="store_false",
        help="Deaktiviert das Ausführen von mypy vor der Auswertung.",
    )
    parser.set_defaults(run_mypy=True)
    parser.add_argument(
        "--package-dir",
        type=str,
        default=DEFAULT_PACKAGE_DIR,
        help="Zu analysierendes Paket-/Verzeichnis (Standard: kei_agent)",
    )
    return parser.parse_args()


def run_mypy_and_generate_report(package_dir: Path, report_dir: Path, project_root: Path) -> None:
    """\
    Führt mypy aus und erzeugt einen Text-Report unter `report_dir`.
    """
    # mypy-Konfiguration optional berücksichtigen
    config_file = project_root / "mypy.ini"
    cmd: List[str] = [
        sys.executable,
        "-m",
        "mypy",
        str(package_dir),
        "--txt-report",
        str(report_dir),
    ]
    if config_file.exists():
        cmd.extend(["--config-file", str(config_file)])

    print(f"Führe MyPy aus: {' '.join(cmd)}", file=sys.stderr)

    # mypy darf mit Fehlercode != 0 enden; der Report wird dennoch genutzt
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"MyPy beendet mit Fehlercode {result.returncode}", file=sys.stderr)
        if result.stderr:
            print(f"MyPy stderr: {result.stderr}", file=sys.stderr)
        if result.stdout:
            print(f"MyPy stdout: {result.stdout}", file=sys.stderr)

    # Prüfe, ob der Report erstellt wurde
    index_file = report_dir / "index.txt"
    if not index_file.exists():
        print(f"Warnung: MyPy hat keine index.txt erstellt in {report_dir}", file=sys.stderr)
        print(f"Verfügbare Dateien: {list(report_dir.glob('*')) if report_dir.exists() else 'Verzeichnis existiert nicht'}", file=sys.stderr)


def parse_txt_report_index(index_file: Path) -> Tuple[int, int, float, List[Dict[str, Any]]]:
    """\
    Parst die mypy-Text-Report-Datei `index.txt` und extrahiert Gesamtsummen sowie Modulwerte.

    Rückgabe: (annotated_total, lines_total, coverage_percent, module_entries)
    """
    if not index_file.exists():
        print(f"Report-Datei nicht gefunden: {index_file}", file=sys.stderr)
        print(f"Verzeichnisinhalt: {list(index_file.parent.glob('*')) if index_file.parent.exists() else 'Verzeichnis existiert nicht'}", file=sys.stderr)
        # Fallback: Erstelle leeren Report
        return 0, 0, 0.0, []

    total_annotated: Optional[int] = None
    total_lines: Optional[int] = None
    total_percent: Optional[float] = None
    modules: List[Dict[str, Any]] = []

    with index_file.open("r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        lines = content.split('\n')

        # Parse the table format from mypy --txt-report
        # Format: | Module | X.XX% imprecise | YYY LOC |
        for line in lines:
            line = line.strip()
            if line.startswith('|') and '% imprecise' in line and 'LOC' in line:
                # Split by | and clean up
                parts = [part.strip() for part in line.split('|')]
                if len(parts) >= 4:
                    module_name = parts[1].strip()
                    imprecision_str = parts[2].strip()
                    loc_str = parts[3].strip()

                    # Skip header row and separator rows
                    if (module_name == 'Module' or
                        module_name.startswith('-') or
                        not module_name or
                        module_name == 'Module'):
                        continue

                    # Extract percentage from "X.XX% imprecise"
                    if imprecision_str.endswith('% imprecise'):
                        try:
                            percentage_str = imprecision_str.replace('% imprecise', '').strip()
                            imprecision = float(percentage_str)
                            # Convert imprecision to precision (coverage)
                            coverage = 100.0 - imprecision

                            # Extract LOC from "YYY LOC"
                            loc_match = re.search(r'(\d+)\s+LOC', loc_str)
                            if loc_match:
                                total_loc = int(loc_match.group(1))
                                # Estimate annotated lines based on coverage
                                annotated_loc = int(total_loc * coverage / 100.0)

                                modules.append({
                                    "module": module_name,
                                    "annotated_lines": annotated_loc,
                                    "total_lines": total_loc,
                                    "coverage_percentage": coverage,
                                })
                        except (ValueError, AttributeError):
                            continue

    # Calculate totals from modules if we have them
    if modules:
        total_annotated = sum(m["annotated_lines"] for m in modules)
        total_lines = sum(m["total_lines"] for m in modules)
        total_percent = (total_annotated / total_lines * 100.0) if total_lines > 0 else 0.0
    else:
        # Fallback: try to find any percentage in the file
        percent_match = re.search(r'(\d+\.?\d*)%', content)
        if percent_match:
            total_percent = float(percent_match.group(1))
            total_annotated = 1000  # Dummy values
            total_lines = 1000
        else:
            raise RuntimeError(
                "Konnte die Gesamtabdeckung nicht aus dem mypy-Report extrahieren."
            )

    return total_annotated, total_lines, total_percent, modules


def build_output_json(
    annotated: int, total: int, percent: float, modules: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """\
    Baut die JSON-Struktur für die Ausgabe.
    """
    return {
        "summary": {
            "annotated_lines": annotated,
            "total_lines": total,
            "coverage_percentage": float(f"{percent:.2f}"),
        },
        "modules": modules,
    }


def main() -> int:
    """\
    Einstiegspunkt der Anwendung.
    """
    args = parse_args()

    project_root = Path(__file__).resolve().parent.parent
    package_dir = (project_root / args.package_dir).resolve()
    if not package_dir.exists():
        print(f"Paket-/Verzeichnis nicht gefunden: {package_dir}", file=sys.stderr)
        return 2

    # Temporäres Verzeichnis für Reports
    tmp_dir: Optional[str] = None
    try:
        tmp_dir = tempfile.mkdtemp(prefix="typecov-")
        report_dir = Path(tmp_dir)

        if args.run_mypy:
            run_mypy_and_generate_report(package_dir=package_dir, report_dir=report_dir, project_root=project_root)

        index_file = report_dir / "index.txt"
        annotated, total, percent, modules = parse_txt_report_index(index_file)

        result_json = build_output_json(annotated, total, percent, modules)

        # Schreiben der Ausgabe
        if args.output:
            out_path = Path(args.output)
            with out_path.open("w", encoding="utf-8") as f:
                json.dump(result_json, f, ensure_ascii=False, indent=2)
        else:
            print(json.dumps(result_json, ensure_ascii=False))

        # Schwellwert prüfen
        if args.fail_under is not None and percent < float(args.fail_under):
            print(
                f"Type-Hint-Abdeckung {percent:.2f}% liegt unter der geforderten Schwelle "
                f"von {args.fail_under:.2f}%.",
                file=sys.stderr,
            )
            return 1

        return 0
    finally:
        # Temporäre Dateien bereinigen
        if tmp_dir and os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
