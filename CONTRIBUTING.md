# Beitragende Richtlinien

Bitte vor Pull Requests:

- make quality und make test lokal ausführen
- PEP 8/257/484 sowie Clean Code beachten
- Tests und deutsche Docstrings für öffentliche APIs schreiben

## Development Setup

- Python venv anlegen und aktivieren
- pip install -e ".[dev,docs,security]"
- pre-commit install

## Release Prozess

- Version in pyproject.toml und **init**.py erhöhen
- CHANGELOG.md aktualisieren
- Tag vX.Y.Z bzw. vX.Y.ZbN erstellen und pushen
- Der Release-Workflow publiziert Pakete nach PyPI/TestPyPI
