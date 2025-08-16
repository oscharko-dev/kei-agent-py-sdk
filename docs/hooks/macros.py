"""
MkDocs Hooks für erweiterte Funktionalität.

Dieses Modul stellt Hooks für MkDocs bereit, um erweiterte Funktionalitäten
wie automatische Generierung von Inhalten, Makros und andere Dokumentations-Features
zu ermöglichen.
"""

import re
from pathlib import Path
from typing import Dict, Any

def on_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Hook wird beim Laden der Konfiguration aufgerufen.

    Args:
        config: MkDocs-Konfiguration

    Returns:
        Modifizierte Konfiguration
    """
    return config


def on_pre_build(config: Dict[str, Any]) -> None:
    """Hook wird vor dem Build-Prozess aufgerufen.

    Args:
        config: MkDocs-Konfiguration
    """
    pass


def on_files(files, config: Dict[str, Any]):
    """Hook wird beim Verarbeiten der Dateien aufgerufen.

    Args:
        files: Liste der zu verarbeitenden Dateien
        config: MkDocs-Konfiguration

    Returns:
        Modifizierte Dateiliste
    """
    return files


def on_nav(nav, config: Dict[str, Any], files):
    """Hook wird beim Verarbeiten der Navigation aufgerufen.

    Args:
        nav: Navigation-Struktur
        config: MkDocs-Konfiguration
        files: Dateiliste

    Returns:
        Modifizierte Navigation
    """
    return nav


def on_page_markdown(markdown: str, page, config: Dict[str, Any], files) -> str:
    """Hook wird beim Verarbeiten des Markdown-Inhalts aufgerufen.

    Hier können Makros und automatische Inhalte eingefügt werden.

    Args:
        markdown: Markdown-Inhalt der Seite
        page: Seiten-Objekt
        config: MkDocs-Konfiguration
        files: Dateiliste

    Returns:
        Modifizierter Markdown-Inhalt
    """
    # Beispiel: Automatische Einfügung der SDK-Version
    if "{{SDK_VERSION}}" in markdown:
        # Versuche Version aus pyproject.toml zu lesen
        try:
            pyproject_path = Path(config['docs_dir']).parent / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
                    if version_match:
                        version = version_match.group(1)
                        markdown = markdown.replace("{{SDK_VERSION}}", version)
        except Exception:
            # Fallback-Version
            markdown = markdown.replace("{{SDK_VERSION}}", "0.1.0")

    # Beispiel: Automatische Einfügung des aktuellen Datums
    if "{{BUILD_DATE}}" in markdown:
        from datetime import datetime
        build_date = datetime.now().strftime("%Y-%m-%d")
        markdown = markdown.replace("{{BUILD_DATE}}", build_date)

    return markdown


def on_page_content(html: str, page, config: Dict[str, Any], files) -> str:
    """Hook wird beim Verarbeiten des HTML-Inhalts aufgerufen.

    Args:
        html: HTML-Inhalt der Seite
        page: Seiten-Objekt
        config: MkDocs-Konfiguration
        files: Dateiliste

    Returns:
        Modifizierter HTML-Inhalt
    """
    return html


def on_post_build(config: Dict[str, Any]) -> None:
    """Hook wird nach dem Build-Prozess aufgerufen.

    Args:
        config: MkDocs-Konfiguration
    """
    pass
