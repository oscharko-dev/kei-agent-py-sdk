#!/bin/bash

# Setup-Script für Git Hooks im KEI Agent Python SDK

set -e

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Setup Git Hooks für KEI Agent Python SDK${NC}"

# Prüfe, ob wir in einem Git-Repository sind
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Fehler: Nicht in einem Git-Repository${NC}"
    exit 1
fi

# Prüfe, ob .githooks Verzeichnis existiert
if [ ! -d ".githooks" ]; then
    echo -e "${RED}❌ Fehler: .githooks Verzeichnis nicht gefunden${NC}"
    exit 1
fi

# Prüfe, ob pre-commit Hook existiert
if [ ! -f ".githooks/pre-commit" ]; then
    echo -e "${RED}❌ Fehler: .githooks/pre-commit nicht gefunden${NC}"
    exit 1
fi

echo -e "${BLUE}📝 Konfiguriere Git Hooks...${NC}"

# Setze Git Hooks Pfad
git config core.hooksPath .githooks

# Mache alle Hooks ausführbar
chmod +x .githooks/*

echo -e "${GREEN}✅ Git Hooks erfolgreich konfiguriert!${NC}"
echo -e "${BLUE}📋 Konfigurierte Hooks:${NC}"

# Liste alle verfügbaren Hooks auf
for hook in .githooks/*; do
    if [ -f "$hook" ] && [ -x "$hook" ]; then
        hook_name=$(basename "$hook")
        echo -e "  ${GREEN}✓${NC} $hook_name"
    fi
done

echo ""
echo -e "${YELLOW}💡 Info:${NC}"
echo -e "  - Der pre-commit Hook führt automatisch 'make lint' vor jedem Commit aus"
echo -e "  - Commits werden nur erlaubt, wenn alle Linting-Checks bestehen"
echo -e "  - Formatierte Dateien werden automatisch zum Commit hinzugefügt"
echo ""
echo -e "${GREEN}🎉 Setup abgeschlossen!${NC}"
