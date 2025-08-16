# KEI-Agent Python SDK

Willkommen zur offiziellen Dokumentation des **KEI-Agent Python SDK** - einem Enterprise-Grade Framework für Multi-Agent-Systeme mit umfassender Protokoll-Unterstützung.

## 🚀 Überblick

Das KEI-Agent Python SDK bietet eine einheitliche, typisierte API für die Entwicklung von intelligenten Agenten mit Unterstützung für:

- **Multi-Protocol Support**: KEI-RPC, KEI-Stream, KEI-Bus und KEI-MCP
- **Enterprise Security**: Umfassende Authentifizierung und Input-Validierung
- **Production Monitoring**: Structured Logging und Health Checks
- **Developer Experience**: Vollständige Type Hints und deutsche Dokumentation
- **High Availability**: Automatische Fallback-Mechanismen und Circuit Breaker

## ⚡ Quick Start

```python
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig

# Konfiguration
config = AgentClientConfig(
    base_url="https://api.kei-framework.com",
    api_token="your-api-token",
    agent_id="my-agent"
)

# Client verwenden
async with UnifiedKeiAgentClient(config=config) as client:
    # Plan erstellen
    plan = await client.plan_task("Erstelle einen Quartalsbericht")

    # Aktion ausführen
    result = await client.execute_action("generate_report", {
        "format": "pdf",
        "quarter": "Q4-2024"
    })

    # Health Check
    health = await client.health_check()
    print(f"System Status: {health['status']}")
```

## 🏗️ Architektur-Highlights

### Refactored Design
Das SDK wurde vollständig refactored für Enterprise-Einsatz:

- **Clean Code**: Alle Module ≤200 Zeilen, Funktionen ≤20 Zeilen
- **Type Safety**: 100% Type Hints für alle APIs
- **Modularity**: Klare Trennung von Protokoll-Clients, Security und Utilities
- **Testability**: 85%+ Test-Coverage mit deterministischen Tests

### Multi-Protocol Architecture

```mermaid
graph TB
    subgraph "KEI-Agent SDK"
        UC[UnifiedKeiAgentClient]
        PS[ProtocolSelector]

        subgraph "Protocol Clients"
            RPC[KEI-RPC<br/>Sync Operations]
            STREAM[KEI-Stream<br/>Real-time]
            BUS[KEI-Bus<br/>Async Messages]
            MCP[KEI-MCP<br/>Tool Integration]
        end

        subgraph "Enterprise Features"
            LOG[Structured Logging]
            HEALTH[Health Checks]
            VALID[Input Validation]
            SEC[Security Manager]
        end
    end

    UC --> PS
    PS --> RPC
    PS --> STREAM
    PS --> BUS
    PS --> MCP
    UC --> LOG
    UC --> HEALTH
    UC --> VALID
    UC --> SEC
```

## 🎯 Hauptfeatures

### 🔌 Multi-Protocol Support
- **KEI-RPC**: Synchrone Request-Response Operationen
- **KEI-Stream**: Bidirektionale Real-time Kommunikation
- **KEI-Bus**: Asynchrone Message-Bus Integration
- **KEI-MCP**: Model Context Protocol für Tool-Integration

### 🛡️ Enterprise Security
- **Multi-Auth**: Bearer Token, OIDC, mTLS
- **Input Validation**: Umfassende Sanitization und Validierung
- **Audit Logging**: Vollständige Nachverfolgbarkeit
- **RBAC**: Role-Based Access Control

### 📊 Production Monitoring
- **Structured Logging**: JSON-Format mit Correlation-IDs
- **Health Checks**: Database, API, Memory, Custom
- **Performance Metrics**: Built-in Timing und Resource-Monitoring
- **Distributed Tracing**: OpenTelemetry-Integration

### 🔧 Developer Experience
- **Type Safety**: Vollständige Type Hints für IntelliSense
- **Deutsche Dokumentation**: Umfassende Guides und API-Referenz
- **Auto-Completion**: IDE-Unterstützung für alle APIs
- **Error Messages**: Klare, actionable Fehlermeldungen

## 📚 Dokumentations-Navigation

### Erste Schritte
- [**Installation**](getting-started/installation.md) - Schritt-für-Schritt Setup
- [**Quick Start**](getting-started/quickstart.md) - Erste Schritte in 5 Minuten
- [**Konfiguration**](getting-started/configuration.md) - Client-Setup und Optionen

### Benutzerhandbuch
- [**Basis-Konzepte**](user-guide/concepts.md) - Grundlagen verstehen
- [**Client-Verwendung**](user-guide/client-usage.md) - Praktische Anwendung
- [**Protokolle**](user-guide/protocols.md) - Multi-Protocol Features

### Enterprise Features
- [**Structured Logging**](enterprise/logging.md) - Production-Logging
- [**Health Checks**](enterprise/health-checks.md) - System-Monitoring
- [**Security**](enterprise/security.md) - Sicherheits-Features

### API-Referenz
- [**Unified Client**](api/unified-client.md) - Haupt-API-Klasse
- [**Protocol Types**](api/protocol-types.md) - Konfigurationen und Enums
- [**Enterprise Logging**](api/enterprise-logging.md) - Logging-APIs

## 🔄 Migration

Migrieren Sie von der Legacy-Version? Unser [**Migration Guide**](migration/from-legacy.md) hilft Ihnen bei einem reibungslosen Übergang zur neuen Enterprise-Architektur.

## 🤝 Community & Support

- **GitHub Repository**: [kei-framework/kei-agent](https://github.com/kei-framework/kei-agent)
- **Issues & Bugs**: [GitHub Issues](https://github.com/kei-framework/kei-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kei-framework/kei-agent/discussions)
- **PyPI Package**: [kei-agent-sdk](https://pypi.org/project/kei-agent-sdk/)

## 📄 Lizenz

Das KEI-Agent Python SDK ist unter der [MIT-Lizenz](https://github.com/kei-framework/kei-agent/blob/main/LICENSE) veröffentlicht.

---

**Bereit loszulegen?** Beginnen Sie mit der [Installation](getting-started/installation.md) oder springen Sie direkt zum [Quick Start Guide](getting-started/quickstart.md)!
