#!/usr/bin/env python3
"""
Setup-Skript für KEI-Agent Python SDK.
Fallback für License-Metadaten-Kompatibilität.
"""

from setuptools import setup, find_packages
import os


# Lese README
def read_readme():
    """Liest README.md für long_description."""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "KEI-Agent Python SDK"


# Lese Requirements
def read_requirements():
    """Liest requirements aus pyproject.toml."""
    return [
        "httpx>=0.24.0,<1.0.0",
        "aiohttp>=3.8.0,<4.0.0",
        "websockets>=11.0.0,<12.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "tenacity>=8.2.0,<9.0.0",
        "msgpack>=1.0.0,<2.0.0",
        "packaging>=21.0",
        "python-dateutil>=2.8.0",
        "psutil>=5.9.0,<8.0.0",
        "structlog>=23.1.0,<26.0.0",
        "typing-extensions>=4.0.0",
        "opentelemetry-api>=1.20.0,<2.0.0",
        "opentelemetry-sdk>=1.20.0,<2.0.0",
        "opentelemetry-exporter-jaeger>=1.20.0,<2.0.0",
        "opentelemetry-exporter-zipkin-json>=1.20.0,<2.0.0",
        "opentelemetry-propagator-b3>=1.20.0,<2.0.0",
    ]


setup(
    name="kei_agent_py_sdk",
    version="0.1.0-beta.1",
    description="Enterprise-Grade Python SDK for Keiko-Personal-Assistant Platform with Multi-Protocol Support",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Oliver Scharkowski",
    author_email="o.scharkowski@oscharko.de",
    license="MIT",  # EXPLIZITE LICENSE FÜR KOMPATIBILITÄT
    url="https://github.com/oscharko/keiko-personal-assistant",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Distributed Computing",
    ],
    keywords="agent framework sdk multi-protocol enterprise",
    project_urls={
        "Bug Reports": "https://github.com/oscharko/keiko-personal-assistant/issues",
        "Source": "https://github.com/oscharko/keiko-personal-assistant",
        "Documentation": "https://docs.kei-framework.com",
    },
)
