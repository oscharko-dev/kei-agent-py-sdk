# Pre-Commit Setup für KEI-Agent Python SDK

Diese Anleitung erklärt, wie Sie Pre-Commit-Hooks für das KEI-Agent Python SDK einrichten und verwenden.

## 🚀 Installation

### 1. Pre-Commit installieren

```bash
# Mit pip
pip install pre-commit

# Oder mit conda
conda install -c conda-forge pre-commit

# Oder mit homebrew (macOS)
brew install pre-commit
```

### 2. Pre-Commit-Hooks installieren

```bash
# Im Projekt-Verzeichnis
cd kei-agent-py-sdk

# Hooks installieren
pre-commit install

# Optional: Commit-Message-Hooks installieren
pre-commit install --hook-type commit-msg
```

### 3. Erste Ausführung (alle Dateien)

```bash
# Alle Hooks auf alle Dateien anwenden
pre-commit run --all-files
```

## 🔧 Verwendung

### Automatische Ausführung

Nach der Installation werden die Hooks automatisch bei jedem `git commit` ausgeführt:

```bash
git add .
git commit -m "Meine Änderungen"
# Pre-Commit-Hooks werden automatisch ausgeführt
```

### Manuelle Ausführung

```bash
# Alle Hooks ausführen
pre-commit run --all-files

# Nur bestimmte Hooks ausführen
pre-commit run ruff
pre-commit run mypy
pre-commit run bandit

# Hooks auf bestimmte Dateien ausführen
pre-commit run --files client.py unified_client.py
```

### Hooks überspringen (Notfall)

```bash
# Alle Hooks überspringen (nicht empfohlen)
git commit --no-verify -m "Notfall-Commit"

# Bestimmte Hooks überspringen
SKIP=mypy,bandit git commit -m "Commit ohne MyPy und Bandit"
```

## 📋 Konfigurierte Hooks

### 🐍 Python Code-Qualität

1. **Ruff Linting** (`ruff`)
   - Ersetzt flake8, pylint
   - Automatische Fixes für viele Probleme
   - Konfiguration: `pyproject.toml`

2. **Ruff Formatierung** (`ruff-format`)
   - Ersetzt black + isort
   - Automatische Code-Formatierung
   - Konsistenter Stil

3. **MyPy Typenprüfung** (`mypy`)
   - Statische Typenanalyse
   - Findet Typ-Fehler vor der Laufzeit
   - Konfiguration: `pyproject.toml`

4. **Bandit Sicherheits-Scan** (`bandit`)
   - Scannt auf Sicherheitsprobleme
   - Findet potenzielle Vulnerabilities
   - Konfiguration: `pyproject.toml`

### 🔧 Allgemeine Code-Qualität

5. **Trailing Whitespace** - Entfernt überflüssige Leerzeichen
6. **End-of-File-Fixer** - Stellt sicher, dass Dateien mit Newline enden
7. **Merge-Konflikt-Check** - Verhindert Commits mit Konflikt-Markern
8. **Große Dateien Check** - Verhindert Commits von Dateien > 500KB
9. **YAML/JSON/TOML Syntax** - Validiert Konfigurationsdateien

### 📚 Dokumentation

10. **Markdown Linting** (`markdownlint`)
    - Prüft Markdown-Dateien auf Stil
    - Automatische Fixes wo möglich
    - Konfiguration: `.markdownlint.json`

11. **MkDocs Validierung** - Prüft MkDocs-Konfiguration

### ⚡ GitHub Actions

12. **ActionLint** - Validiert GitHub Actions Workflows
13. **YAML Linting** - Detaillierte YAML-Syntax-Prüfung

### 🔍 Custom Hooks

14. **Import-Validierung** - Stellt sicher, dass flache Imports verwendet werden
15. **TODO/FIXME Check** - Warnt vor TODO-Kommentaren
16. **pyproject.toml Validierung** - Prüft Projekt-Konfiguration

## 🛠️ Konfiguration anpassen

### Hook-spezifische Konfiguration

Die meisten Tools werden über `pyproject.toml` konfiguriert:

```toml
[tool.ruff]
line-length = 88
target-version = "py39"

[tool.mypy]
python_version = "3.9"
strict = true

[tool.bandit]
exclude_dirs = ["tests"]
```

### Pre-Commit-spezifische Anpassungen

Bearbeiten Sie `.pre-commit-config.yaml`:

```yaml
# Hook deaktivieren
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.11.2
  hooks:
    - id: mypy
      # Hook überspringen
      stages: [manual]

# Zusätzliche Argumente
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.6.9
  hooks:
    - id: ruff
      args: [--fix, --exit-non-zero-on-fix, --show-fixes]
```

## 🚨 Häufige Probleme

### 1. Hook schlägt fehl

```bash
# Details anzeigen
pre-commit run --verbose

# Bestimmten Hook debuggen
pre-commit run ruff --verbose
```

### 2. Hooks aktualisieren

```bash
# Alle Hook-Versionen aktualisieren
pre-commit autoupdate

# Hooks neu installieren
pre-commit clean
pre-commit install
```

### 3. Cache-Probleme

```bash
# Pre-Commit-Cache leeren
pre-commit clean

# Bestimmten Hook-Cache leeren
pre-commit clean --repo https://github.com/astral-sh/ruff-pre-commit
```

### 4. Temporär deaktivieren

```bash
# Alle Hooks deaktivieren
pre-commit uninstall

# Wieder aktivieren
pre-commit install
```

## 📊 Best Practices

### 1. Regelmäßige Updates

```bash
# Wöchentlich ausführen
pre-commit autoupdate
```

### 2. Team-Synchronisation

```bash
# Nach git pull
pre-commit install
pre-commit run --all-files
```

### 3. CI/CD Integration

Die gleichen Checks laufen auch in GitHub Actions:
- `.github/workflows/ci.yml`
- Lokale Checks = CI Checks

### 4. Schrittweise Einführung

```bash
# Nur neue/geänderte Dateien
git add .
pre-commit run

# Alle Dateien (bei Ersteinrichtung)
pre-commit run --all-files
```

## 🔗 Weiterführende Links

- [Pre-Commit Dokumentation](https://pre-commit.com/)
- [Ruff Dokumentation](https://docs.astral.sh/ruff/)
- [MyPy Dokumentation](https://mypy.readthedocs.io/)
- [Bandit Dokumentation](https://bandit.readthedocs.io/)

## 💡 Tipps

1. **IDE-Integration**: Konfigurieren Sie Ihr IDE für die gleichen Regeln
2. **Automatisierung**: Nutzen Sie `pre-commit run --all-files` in CI/CD
3. **Anpassung**: Passen Sie Regeln an Ihr Team an
4. **Dokumentation**: Dokumentieren Sie team-spezifische Konfigurationen
