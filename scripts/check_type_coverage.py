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

    # mypy darf mit Fehlercode != 0 enden; der Report wird dennoch genutzt
    subprocess.run(cmd, check=False)


def parse_txt_report_index(index_file: Path) -> Tuple[int, int, float, List[Dict[str, Any]]]:
    """\
    Parst die mypy-Text-Report-Datei `index.txt` und extrahiert Gesamtsummen sowie Modulwerte.

    Rückgabe: (annotated_total, lines_total, coverage_percent, module_entries)
    """
    if not index_file.exists():
        raise FileNotFoundError(f"Report-Datei nicht gefunden: {index_file}")

    total_annotated: Optional[int] = None
    total_lines: Optional[int] = None
    total_percent: Optional[float] = None
    modules: List[Dict[str, Any]] = []

    # Muster für Modulzeilen und die Gesamtsumme
    module_pattern = re.compile(r"^\s*(?P<name>\S.*?)\s+(?P<ann>\d+)\s*/\s*(?P<tot>\d+)\s+\|\s+(?P<pct>[\d.]+)%\s*$")
    total_pattern = re.compile(r"^\s*Total\s+(?P<ann>\d+)\s*/\s*(?P<tot>\d+)\s+\|\s+(?P<pct>[\d.]+)%\s*$")

    with index_file.open("r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            # Gesamtsumme zuerst prüfen
            m_total = total_pattern.match(line)
            if m_total:
                total_annotated = int(m_total.group("ann"))
                total_lines = int(m_total.group("tot"))
                total_percent = float(m_total.group("pct"))
                continue

            # Modulzeilen (überspringt Kopf-/Trennzeilen)
            m_mod = module_pattern.match(line)
            if m_mod and not m_mod.group("name").lower().startswith("name"):
                name = m_mod.group("name")
                ann = int(m_mod.group("ann"))
                tot = int(m_mod.group("tot"))
                pct = float(m_mod.group("pct"))
                modules.append(
                    {
                        "module": name,
                        "annotated_lines": ann,
                        "total_lines": tot,
                        "coverage_percentage": pct,
                    }
                )

    # Fallback: Manche mypy-Versionen formatieren anders – heuristischer Versuch
    if total_percent is None and index_file.exists():
        with index_file.open("r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        # Suche nach einer Zeile mit 'Total' und Prozentzahl
        m = re.search(r"Total[^\n]*?(?P<ann>\d+)\s*/\s*(?P<tot>\d+)[^\n]*?(?P<pct>[\d.]+)%", text)
        if m:
            total_annotated = int(m.group("ann"))
            total_lines = int(m.group("tot"))
            total_percent = float(m.group("pct"))

    if total_annotated is None or total_lines is None or total_percent is None:
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
