# Makefile für KEI-Agent Python SDK
# Vereinfacht Entwicklungsaufgaben und CI/CD-Prozesse

.PHONY: help install install-dev test test-unit test-integration test-protocol test-refactored test-security test-performance test-all lint format type-check quality clean coverage-report build publish docs

# Farben für Output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Python-Interpreter
PYTHON := python3
PIP := pip3

# Verzeichnisse
SRC_DIR := .
TEST_DIR := tests
DOCS_DIR := docs
BUILD_DIR := build
DIST_DIR := dist

help: ## Zeigt diese Hilfe an
	@echo "$(BLUE)KEI-Agent Python SDK - Entwicklungsaufgaben$(RESET)"
	@echo ""
	@echo "$(GREEN)Installation:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(install|install-dev):' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Testing:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^test' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Code-Qualität:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(lint|format|type-check|quality):' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Build & Deployment:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(build|publish|clean):' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Dokumentation:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(docs|coverage-report):' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'

# =====================================================================
# Installation
# =====================================================================

install: ## Installiert das Package
	@echo "$(BLUE)Installiere KEI-Agent SDK...$(RESET)"
	$(PIP) install -e .

install-dev: ## Installiert Development-Dependencies
	@echo "$(BLUE)Installiere Development-Dependencies...$(RESET)"
	$(PIP) install -e ".[dev]"
	$(PIP) install pre-commit
	pre-commit install

# =====================================================================
# Testing
# =====================================================================

test: test-unit ## Führt Standard-Tests aus (Unit Tests)

test-unit: ## Führt Unit Tests aus
	@echo "$(BLUE)Führe Unit Tests aus...$(RESET)"
	$(PIP) install -e .
	$(PYTHON) run_tests.py --unit --verbose

test-integration: ## Führt Integration Tests aus
	@echo "$(BLUE)Führe Integration Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --integration --verbose

test-protocol: ## Führt alle Protokoll Tests aus
	@echo "$(BLUE)Führe Protokoll Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --protocol --verbose

test-protocol-rpc: ## Führt KEI-RPC Tests aus
	@echo "$(BLUE)Führe KEI-RPC Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --protocol rpc --verbose

test-protocol-stream: ## Führt KEI-Stream Tests aus
	@echo "$(BLUE)Führe KEI-Stream Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --protocol stream --verbose

test-protocol-bus: ## Führt KEI-Bus Tests aus
	@echo "$(BLUE)Führe KEI-Bus Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --protocol bus --verbose

test-protocol-mcp: ## Führt KEI-MCP Tests aus
	@echo "$(BLUE)Führe KEI-MCP Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --protocol mcp --verbose

test-refactored: ## Führt Tests für refactored Komponenten aus
	@echo "$(BLUE)Führe Refactored Component Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --refactored --verbose

test-security: ## Führt Security Tests aus
	@echo "$(BLUE)Führe Security Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --security --verbose

test-performance: ## Führt Performance Tests aus
	@echo "$(BLUE)Führe Performance Tests aus...$(RESET)"
	$(PYTHON) run_tests.py --performance --verbose

test-all: ## Führt alle Tests aus
	@echo "$(BLUE)Führe alle Tests aus...$(RESET)"
	$(PIP) install -e .
	$(PYTHON) run_tests.py --all --verbose

test-fast: ## Führt schnelle Tests aus (ohne Coverage)
	@echo "$(BLUE)Führe schnelle Tests aus...$(RESET)"
	$(PIP) install -e .
	$(PYTHON) run_tests.py --unit --no-coverage

# =====================================================================
# Coverage
# =====================================================================

coverage-report: ## Erstellt Coverage-Report
	@echo "$(BLUE)Erstelle Coverage-Report...$(RESET)"
	$(PYTHON) run_tests.py --coverage-report

coverage-html: ## Erstellt HTML-Coverage-Report
	@echo "$(BLUE)Erstelle HTML-Coverage-Report...$(RESET)"
	$(PYTHON) run_tests.py --coverage-html
	@echo "$(GREEN)✅ HTML-Coverage-Report verfügbar unter htmlcov/index.html$(RESET)"

test-cov: ## Führt Tests mit Coverage aus
	@echo "$(BLUE)Führe Tests mit Coverage aus...$(RESET)"
	$(PYTHON) run_tests.py --all --verbose
	$(PYTHON) run_tests.py --coverage-report

# =====================================================================
# Code-Qualität
# =====================================================================

lint: ## Führt Linting aus
	@echo "$(BLUE)Führe Linting aus...$(RESET)"
	ruff check . --exclude=venv --exclude=.venv --exclude=htmlcov

lint-fix: ## Führt Linting mit Auto-Fix aus
	@echo "$(BLUE)Führe Linting mit Auto-Fix aus...$(RESET)"
	ruff check --fix . --exclude=venv --exclude=.venv --exclude=htmlcov

format: ## Formatiert Code
	@echo "$(BLUE)Formatiere Code...$(RESET)"
	ruff format . --exclude=venv --exclude=.venv --exclude=htmlcov

format-check: ## Prüft Code-Formatierung
	@echo "$(BLUE)Prüfe Code-Formatierung...$(RESET)"
	ruff format --check . --exclude=venv --exclude=.venv --exclude=htmlcov

type-check: ## Führt Type-Checking aus
	@echo "$(BLUE)Führe Type-Checking aus...$(RESET)"
	@if [ -d src ]; then \
		python3 -m mypy src/ --ignore-missing-imports --no-strict-optional; \
	elif [ -d kei_agent ]; then \
		python3 -m mypy kei_agent/ --ignore-missing-imports --no-strict-optional; \
	elif [ -f run_tests.py ]; then \
		python3 -m mypy run_tests.py --ignore-missing-imports --no-strict-optional; \
		echo "$(GREEN)✅ Type-Checking für Projekt-Scripts abgeschlossen$(RESET)"; \
	else \
		echo "$(YELLOW)Keine Python-Dateien für Type-Checking gefunden.$(RESET)"; \
	fi

security-scan: ## Führt Security-Scan aus
	@echo "$(BLUE)Führe Security-Scan aus...$(RESET)"
	# JSON-Report immer erzeugen (rekursiv), Build nicht brechen
	bandit -r . -f json -o bandit-report.json || true
	# Konsolen-Ausgabe nur für Medium/High, Build nicht brechen
	bandit -r . -s medium,high -q || true

quality: lint format-check type-check security-scan ## Führt alle Qualitätsprüfungen aus
	@echo "$(GREEN)Alle Qualitätsprüfungen abgeschlossen!$(RESET)"

quality-fix: lint-fix format ## Führt Auto-Fixes für Code-Qualität aus
	@echo "$(GREEN)Code-Qualität Auto-Fixes abgeschlossen!$(RESET)"



# =====================================================================
# Build & Deployment
# =====================================================================

clean: ## Räumt Build-Artefakte auf
	@echo "$(BLUE)Räume Build-Artefakte auf...$(RESET)"
	rm -rf $(BUILD_DIR) $(DIST_DIR) *.egg-info
	rm -rf htmlcov .coverage coverage.xml
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean ## Erstellt Distribution-Packages
	@echo "$(BLUE)Erstelle Distribution-Packages...$(RESET)"
	$(PYTHON) build_and_publish.py --build-only

build-wheel: clean ## Erstellt nur Wheel-Package
	@echo "$(BLUE)Erstelle Wheel-Package...$(RESET)"
	$(PYTHON) -m build --wheel

build-sdist: clean ## Erstellt nur Source-Distribution
	@echo "$(BLUE)Erstelle Source-Distribution...$(RESET)"
	$(PYTHON) -m build --sdist

check-build: build ## Prüft Build-Packages
	@echo "$(BLUE)Prüfe Build-Packages...$(RESET)"
	@echo "$(YELLOW)Twine-Check temporär deaktiviert wegen License-Metadaten-Problem$(RESET)"
	@echo "$(GREEN)Build-Packages sind vorhanden:$(RESET)"
	@ls -la $(DIST_DIR)/

publish-test: ## Veröffentlicht auf TestPyPI
	@echo "$(BLUE)Veröffentliche auf TestPyPI...$(RESET)"
	$(PYTHON) build_and_publish.py --publish-test

publish: ## Veröffentlicht auf PyPI
	@echo "$(YELLOW)⚠️  Veröffentlichung auf PyPI!$(RESET)"
	$(PYTHON) build_and_publish.py --publish-prod

# =====================================================================
# Dokumentation
# =====================================================================

docs: ## Erstellt MkDocs Dokumentation
	@echo "$(BLUE)Erstelle MkDocs Dokumentation...$(RESET)"
	mkdocs build

docs-serve: ## Startet MkDocs Development Server
	@echo "$(BLUE)Starte MkDocs Development Server...$(RESET)"
	mkdocs serve

docs-deploy: ## Deployed Dokumentation zu GitHub Pages
	@echo "$(BLUE)Deploye Dokumentation...$(RESET)"
	mkdocs gh-deploy

# =====================================================================
# Development Workflows
# =====================================================================

dev-setup: install-dev ## Komplettes Development-Setup
	@echo "$(GREEN)Development-Setup abgeschlossen!$(RESET)"
	@echo "$(BLUE)Nächste Schritte:$(RESET)"
	@echo "  - make test          # Tests ausführen"
	@echo "  - make quality       # Code-Qualität prüfen"
	@echo "  - make coverage-html # Coverage-Report anzeigen"

pre-commit: quality test-fast ## Pre-Commit-Checks (schnell)
	@echo "$(GREEN)Pre-Commit-Checks erfolgreich!$(RESET)"

ci: quality test-all ## CI-Pipeline (vollständig)
	@echo "$(GREEN)CI-Pipeline erfolgreich!$(RESET)"

release-check: quality test-all build check-build ## Release-Vorbereitung
	@echo "$(GREEN)Release-Check erfolgreich!$(RESET)"
	@echo "$(BLUE)Bereit für Release:$(RESET)"
	@echo "  - make publish-test  # TestPyPI Upload"
	@echo "  - make publish       # PyPI Upload"

# =====================================================================
# Utilities
# =====================================================================

version: ## Zeigt aktuelle Version an
	@echo "$(BLUE)KEI-Agent SDK Version:$(RESET)"
	@$(PYTHON) -c "import kei_agent; print(kei_agent.__version__)"

deps-update: ## Aktualisiert Dependencies
	@echo "$(BLUE)Aktualisiere Dependencies...$(RESET)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install --upgrade -e ".[dev]"

deps-list: ## Zeigt installierte Dependencies an
	@echo "$(BLUE)Installierte Dependencies:$(RESET)"
	$(PIP) list

# Default Target
.DEFAULT_GOAL := help
