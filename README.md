# KEI-Agent Python SDK

[![PyPI version](https://badge.fury.io/py/kei-agent-sdk.svg)](https://badge.fury.io/py/kei-agent-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/kei-agent-sdk.svg)](https://pypi.org/project/kei-agent-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.kei-framework.com)

**Enterprise-Grade Python SDK für KEI-Agent Framework mit Multi-Protocol Support**

Das KEI-Agent Python SDK bietet eine einheitliche, typisierte API für die Entwicklung von intelligenten Agenten mit umfassender Protokoll-Unterstützung, Enterprise-Security und Production-Monitoring.

## 🚀 Features

### Multi-Protocol Support
- **KEI-RPC**: Synchrone Request-Response Operationen
- **KEI-Stream**: Bidirektionale Real-time Kommunikation  
- **KEI-Bus**: Asynchrone Message-Bus Integration
- **KEI-MCP**: Model Context Protocol für Tool-Integration

### Enterprise Security
- **Multi-Auth**: Bearer Token, OIDC, mTLS
- **Input Validation**: Umfassende Sanitization und XSS/SQL-Injection-Schutz
- **Audit Logging**: Vollständige Nachverfolgbarkeit aller Operationen
- **RBAC**: Role-Based Access Control Integration

### Production Monitoring
- **Structured Logging**: JSON-Format mit Correlation-IDs
- **Health Checks**: Database, API, Memory, Custom Checks
- **Performance Metrics**: Built-in Timing und Resource-Monitoring
- **Distributed Tracing**: OpenTelemetry-Integration

### Developer Experience
- **Type Safety**: 100% Type Hints für vollständige IntelliSense
- **Deutsche Dokumentation**: Umfassende Guides und API-Referenz
- **Auto-Protocol Selection**: Intelligente Protokoll-Auswahl
- **Async-First**: Non-blocking I/O für maximale Performance

## 📦 Installation

### Standard-Installation

```bash
pip install kei-agent-sdk
```

### Mit Enterprise-Features

```bash
pip install "kei-agent-sdk[security,docs]"
```

### Development-Installation

```bash
git clone https://github.com/kei-framework/kei-agent.git
cd kei-agent/sdk/python/kei_agent
pip install -e ".[dev,docs,security]"
```

## ⚡ Quick Start

### Einfacher Agent-Client

```python
import asyncio
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig

async def main():
    # Konfiguration
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="my-agent"
    )
    
    # Client verwenden
    async with UnifiedKeiAgentClient(config=config) as client:
        # Plan erstellen
        plan = await client.plan_task(
            objective="Erstelle einen Quartalsbericht",
            context={"format": "pdf", "quarter": "Q4-2024"}
        )
        print(f"Plan erstellt: {plan['plan_id']}")
        
        # Aktion ausführen
        result = await client.execute_action(
            action="generate_report",
            parameters={"template": "quarterly", "data_source": "financial_db"}
        )
        print(f"Report generiert: {result['action_id']}")
        
        # Health Check
        health = await client.health_check()
        print(f"System Status: {health['status']}")

asyncio.run(main())
```

### Multi-Protocol Features

```python
from kei_agent import ProtocolType

async def multi_protocol_example():
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="multi-protocol-agent"
    )
    
    async with UnifiedKeiAgentClient(config=config) as client:
        # Automatische Protokoll-Auswahl
        plan = await client.plan_task("Synchrone Planung")  # → RPC
        
        # Real-time Streaming
        await client.execute_agent_operation(
            "stream_data_processing",
            {"data": "real-time-feed"}  # → STREAM
        )
        
        # Asynchrone Nachrichten
        await client.send_agent_message(
            target_agent="data-processor",
            message_type="task_request",
            payload={"task": "analyze_data"}  # → BUS
        )
        
        # Tool-Integration
        tools = await client.discover_available_tools("math")  # → MCP
        result = await client.use_tool("calculator", expression="100 * 1.08")

asyncio.run(multi_protocol_example())
```

### Enterprise Features

```python
from kei_agent import (
    get_logger, 
    get_health_manager, 
    LogContext,
    APIHealthCheck,
    MemoryHealthCheck
)

# Structured Logging
logger = get_logger("enterprise_agent")
logger.set_context(LogContext(
    correlation_id=logger.create_correlation_id(),
    user_id="user-123",
    agent_id="enterprise-agent"
))

# Health Monitoring
health_manager = get_health_manager()
health_manager.register_check(APIHealthCheck(
    name="external_api",
    url="https://api.external.com/health"
))
health_manager.register_check(MemoryHealthCheck(
    name="system_memory",
    warning_threshold=0.8
))

async def enterprise_example():
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="enterprise-agent"
    )
    
    async with UnifiedKeiAgentClient(config=config) as client:
        # Operation mit Logging
        operation_id = logger.log_operation_start("business_process")
        
        try:
            result = await client.plan_task("Enterprise task")
            logger.log_operation_end("business_process", operation_id, time.time(), success=True)
            
            # Health Check
            summary = await health_manager.run_all_checks()
            logger.info("Health check completed", 
                       overall_status=summary.overall_status,
                       healthy_count=summary.healthy_count)
            
        except Exception as e:
            logger.log_operation_end("business_process", operation_id, time.time(), success=False)
            logger.error("Business process failed", error=str(e))
            raise

asyncio.run(enterprise_example())
```

## 🏗️ Architektur

Das SDK folgt einer modularen, Enterprise-Grade Architektur:

```
kei_agent/
├── unified_client_refactored.py    # Haupt-API-Klasse
├── protocol_types.py               # Typ-Definitionen und Konfigurationen  
├── security_manager.py             # Authentifizierung und Token-Management
├── protocol_clients.py             # KEI-RPC, Stream, Bus, MCP Clients
├── protocol_selector.py            # Intelligente Protokoll-Auswahl
├── enterprise_logging.py           # Strukturiertes JSON-Logging
├── health_checks.py               # System-Monitoring und Health-Checks
└── input_validation.py            # Input-Validierung und Sanitization
```

### Design-Prinzipien

- **Clean Code**: Alle Module ≤200 Zeilen, Funktionen ≤20 Zeilen
- **Type Safety**: 100% Type Hints für alle öffentlichen APIs
- **Single Responsibility**: Jedes Modul hat eine klar definierte Verantwortlichkeit
- **Async-First**: Non-blocking I/O für maximale Performance
- **Enterprise-Ready**: Production-Monitoring und Security-Hardening

## 📚 Dokumentation

- **[Vollständige Dokumentation](https://docs.kei-framework.com)** - Umfassende Guides und API-Referenz
- **[Installation Guide](https://docs.kei-framework.com/getting-started/installation/)** - Schritt-für-Schritt Setup
- **[Quick Start](https://docs.kei-framework.com/getting-started/quickstart/)** - Erste Schritte in 5 Minuten
- **[API-Referenz](https://docs.kei-framework.com/api/)** - Vollständige API-Dokumentation
- **[Enterprise Features](https://docs.kei-framework.com/enterprise/)** - Production-Features
- **[Beispiele](https://docs.kei-framework.com/examples/)** - Praktische Code-Beispiele
- **[Migration Guide](https://docs.kei-framework.com/migration/)** - Upgrade von Legacy-Versionen

## 🔧 Konfiguration

### Basis-Konfiguration

```python
from kei_agent import AgentClientConfig, ProtocolConfig, SecurityConfig, AuthType

# Agent-Konfiguration
agent_config = AgentClientConfig(
    base_url="https://api.kei-framework.com",
    api_token="your-api-token",
    agent_id="my-agent",
    timeout=30,
    max_retries=3
)

# Protokoll-Konfiguration
protocol_config = ProtocolConfig(
    rpc_enabled=True,
    stream_enabled=True,
    bus_enabled=True,
    mcp_enabled=True,
    auto_protocol_selection=True,
    protocol_fallback_enabled=True
)

# Sicherheitskonfiguration
security_config = SecurityConfig(
    auth_type=AuthType.BEARER,
    api_token="your-api-token",
    rbac_enabled=True,
    audit_enabled=True
)

# Client mit vollständiger Konfiguration
client = UnifiedKeiAgentClient(
    config=agent_config,
    protocol_config=protocol_config,
    security_config=security_config
)
```

### Umgebungsvariablen

```bash
export KEI_API_URL="https://api.kei-framework.com"
export KEI_API_TOKEN="your-api-token"
export KEI_AGENT_ID="my-agent"
export KEI_AUTH_TYPE="bearer"
export KEI_RBAC_ENABLED="true"
export KEI_AUDIT_ENABLED="true"
```

## 🧪 Testing

```bash
# Unit Tests ausführen
python -m pytest tests/ -v

# Mit Coverage
python -m pytest tests/ --cov=kei_agent --cov-report=html

# Spezifische Test-Kategorien
python -m pytest tests/ -m "unit"          # Unit Tests
python -m pytest tests/ -m "integration"   # Integration Tests
python -m pytest tests/ -m "security"      # Security Tests

# Performance Tests
python -m pytest tests/ -m "performance"
```

## 🤝 Contributing

Wir freuen uns über Beiträge! Bitte lesen Sie unseren [Contributing Guide](CONTRIBUTING.md) für Details.

### Development Setup

```bash
# Repository klonen
git clone https://github.com/kei-framework/kei-agent.git
cd kei-agent/sdk/python/kei_agent

# Development-Umgebung einrichten
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -e ".[dev,docs,security]"

# Pre-commit hooks installieren
pre-commit install

# Tests ausführen
make test

# Dokumentation erstellen
make docs
```

## 📄 Lizenz

Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert.

## 🔗 Links

- **GitHub Repository**: [kei-framework/kei-agent](https://github.com/kei-framework/kei-agent)
- **PyPI Package**: [kei-agent-sdk](https://pypi.org/project/kei-agent-sdk/)
- **Dokumentation**: [docs.kei-framework.com](https://docs.kei-framework.com)
- **Issues**: [GitHub Issues](https://github.com/kei-framework/kei-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kei-framework/kei-agent/discussions)

## 📊 Status

- ✅ **Production Ready**: Vollständig getestet und dokumentiert
- ✅ **Type Safe**: 100% Type Hints für alle APIs
- ✅ **Enterprise Grade**: Security, Monitoring und Compliance-Features
- ✅ **Well Documented**: Umfassende deutsche Dokumentation
- ✅ **Actively Maintained**: Regelmäßige Updates und Support

---

**Bereit loszulegen?** Installieren Sie das SDK und folgen Sie unserem [Quick Start Guide](https://docs.kei-framework.com/getting-started/quickstart/)!
