# setup.py für KEI-Agent Python SDK
"""Setup-Konfiguration für KEI-Agent-Framework Python SDK."""

from setuptools import setup, find_packages

setup(
    name="kei-agent-sdk",
    version="1.0.0",
    description="Python SDK für KEI-Agent-Framework",
    long_description="Vollständige SDK-Implementation für KEI-Agent-Framework mit Enterprise-Features",
    long_description_content_type="text/plain",
    author="KEI-Framework Team",
    author_email="team@kei-framework.com",
    url="https://github.com/kei-framework/kei-agent-python-sdk",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        # HTTP und WebSocket Clients
        "aiohttp>=3.8.0,<4.0.0",
        "httpx>=0.24.0,<1.0.0",
        "websockets>=11.0.0,<12.0.0",

        # Async und Utilities
        "pydantic>=2.0.0,<3.0.0",
        "typing-extensions>=4.0.0",

        # Tracing und Monitoring
        "opentelemetry-api>=1.20.0,<2.0.0",
        "opentelemetry-sdk>=1.20.0,<2.0.0",
        "opentelemetry-exporter-jaeger>=1.20.0,<2.0.0",
        "opentelemetry-exporter-zipkin-json>=1.20.0,<2.0.0",
        "opentelemetry-propagator-b3>=1.20.0,<2.0.0",

        # Retry und Circuit Breaker
        "tenacity>=8.2.0,<9.0.0",

        # Serialization
        "msgpack>=1.0.0,<2.0.0",

        # Utilities
        "packaging>=21.0",
        "python-dateutil>=2.8.0",

        # Enterprise Features
        "psutil>=5.9.0,<6.0.0",
        "structlog>=23.1.0,<24.0.0",
    ],
    extras_require={
        "security": [
            "authlib>=1.2.0,<2.0.0",
            "cryptography>=41.0.0,<42.0.0",
            "pyopenssl>=23.0.0,<24.0.0",
        ],
        "cli": [
            "click>=8.0.0,<9.0.0",
            "rich>=13.0.0,<14.0.0",
        ],
        "dev": [
            "pytest>=7.4.0,<8.0.0",
            "pytest-asyncio>=0.21.0,<1.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "pytest-mock>=3.11.0,<4.0.0",
            "black>=23.7.0,<24.0.0",
            "isort>=5.12.0,<7.0.0",
            "flake8>=6.0.0,<7.0.0",
            "mypy>=1.5.0,<2.0.0",
        ],
        "all": [
            "authlib>=1.2.0,<2.0.0",
            "cryptography>=41.0.0,<42.0.0",
            "pyopenssl>=23.0.0,<24.0.0",
            "click>=8.0.0,<9.0.0",
            "rich>=13.0.0,<14.0.0",
            "pytest>=7.4.0,<8.0.0",
            "pytest-asyncio>=0.21.0,<1.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "pytest-mock>=3.11.0,<4.0.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: System :: Distributed Computing"
    ],
    keywords="kei agent framework api sdk python enterprise",
    project_urls={
        "Documentation": "https://docs.kei-framework.com/agent/python-sdk",
        "Source": "https://github.com/kei-framework/kei-agent-python-sdk",
        "Tracker": "https://github.com/kei-framework/kei-agent-python-sdk/issues"
    }
)
