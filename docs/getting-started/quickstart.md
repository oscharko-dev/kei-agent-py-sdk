# Quick Start Guide

Lernen Sie die Grundlagen des KEI-Agent SDK in nur 5 Minuten! Diese Anleitung zeigt Ihnen die wichtigsten Features anhand praktischer Beispiele.

## 🚀 Ihr erster Agent-Client

### 1. Basis-Setup

```python
import asyncio
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig

async def main():
    # Konfiguration erstellen
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="my-first-agent"
    )
    
    # Client verwenden
    async with UnifiedKeiAgentClient(config=config) as client:
        print("🎉 Client erfolgreich verbunden!")
        
        # Client-Informationen anzeigen
        info = client.get_client_info()
        print(f"Agent ID: {info['agent_id']}")
        print(f"Verfügbare Protokolle: {info['available_protocols']}")

# Ausführen
asyncio.run(main())
```

### 2. Erste Agent-Operationen

```python
async def agent_operations():
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="demo-agent"
    )
    
    async with UnifiedKeiAgentClient(config=config) as client:
        # 📋 Plan erstellen
        plan = await client.plan_task(
            objective="Erstelle einen Quartalsbericht für Q4 2024",
            context={
                "format": "pdf",
                "sections": ["executive_summary", "financials", "outlook"],
                "deadline": "2024-12-31"
            }
        )
        print(f"Plan erstellt: {plan['plan_id']}")
        
        # ⚡ Aktion ausführen
        result = await client.execute_action(
            action="generate_report",
            parameters={
                "template": "quarterly_template",
                "data_source": "financial_db",
                "output_format": "pdf"
            }
        )
        print(f"Aktion ausgeführt: {result['action_id']}")
        
        # 👁️ Umgebung beobachten
        observation = await client.observe_environment(
            observation_type="system_metrics",
            data={"interval": 60, "metrics": ["cpu", "memory", "disk"]}
        )
        print(f"Beobachtung: {observation['observation_id']}")
        
        # 💡 Reasoning erklären
        explanation = await client.explain_reasoning(
            query="Warum wurde diese Vorlage gewählt?",
            context={"action_id": result['action_id']}
        )
        print(f"Erklärung: {explanation['explanation']}")

asyncio.run(agent_operations())
```

## 🔌 Multi-Protocol Features

### Automatische Protokoll-Auswahl

```python
async def multi_protocol_demo():
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="multi-protocol-agent"
    )
    
    async with UnifiedKeiAgentClient(config=config) as client:
        # 🔄 RPC für synchrone Operationen (automatisch gewählt)
        sync_result = await client.plan_task("Synchrone Planung")
        
        # 🌊 Stream für Real-time (automatisch gewählt für "stream_" Prefix)
        await client.execute_agent_operation(
            "stream_data_processing",
            {"data": "real-time-feed"}
        )
        
        # 📨 Bus für asynchrone Nachrichten (automatisch gewählt für "async_" Prefix)
        await client.execute_agent_operation(
            "async_background_task",
            {"task": "data_cleanup", "priority": "low"}
        )
        
        # 🛠️ MCP für Tool-Integration (automatisch gewählt für "tool_" Prefix)
        tools = await client.discover_available_tools("utilities")
        print(f"Verfügbare Tools: {len(tools)}")

asyncio.run(multi_protocol_demo())
```

### Spezifische Protokoll-Auswahl

```python
from kei_agent import ProtocolType

async def specific_protocol_demo():
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="protocol-specific-agent"
    )
    
    async with UnifiedKeiAgentClient(config=config) as client:
        # Explizit RPC verwenden
        rpc_result = await client.execute_agent_operation(
            "custom_operation",
            {"data": "test"},
            protocol=ProtocolType.RPC
        )
        
        # Explizit Stream verwenden
        stream_result = await client.execute_agent_operation(
            "real_time_operation",
            {"stream": True},
            protocol=ProtocolType.STREAM
        )

asyncio.run(specific_protocol_demo())
```

## 🛡️ Enterprise Features

### Structured Logging

```python
from kei_agent import get_logger, LogContext

async def logging_demo():
    # Logger konfigurieren
    logger = get_logger("my_agent")
    
    # Kontext setzen
    correlation_id = logger.create_correlation_id()
    logger.set_context(LogContext(
        correlation_id=correlation_id,
        user_id="user-123",
        agent_id="demo-agent"
    ))
    
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="logging-demo-agent"
    )
    
    async with UnifiedKeiAgentClient(config=config) as client:
        # Operation mit Logging
        operation_id = logger.log_operation_start("plan_creation")
        
        try:
            plan = await client.plan_task("Demo-Plan mit Logging")
            logger.log_operation_end("plan_creation", operation_id, time.time(), success=True)
            logger.info("Plan erfolgreich erstellt", plan_id=plan.get('plan_id'))
            
        except Exception as e:
            logger.log_operation_end("plan_creation", operation_id, time.time(), success=False)
            logger.error("Plan-Erstellung fehlgeschlagen", error=str(e))

import time
asyncio.run(logging_demo())
```

### Health Checks

```python
from kei_agent import get_health_manager, APIHealthCheck, MemoryHealthCheck

async def health_check_demo():
    # Health Manager konfigurieren
    health_manager = get_health_manager()
    
    # Health Checks registrieren
    health_manager.register_check(APIHealthCheck(
        name="kei_api",
        url="https://api.kei-framework.com/health"
    ))
    
    health_manager.register_check(MemoryHealthCheck(
        name="system_memory",
        warning_threshold=0.8,
        critical_threshold=0.95
    ))
    
    # Health Checks ausführen
    summary = await health_manager.run_all_checks()
    
    print(f"Gesamtstatus: {summary.overall_status}")
    print(f"Gesunde Komponenten: {summary.healthy_count}")
    print(f"Problematische Komponenten: {summary.unhealthy_count}")
    
    # Detaillierte Ergebnisse
    for check in summary.checks:
        status_emoji = "✅" if check.status == "healthy" else "❌"
        print(f"{status_emoji} {check.name}: {check.message}")

asyncio.run(health_check_demo())
```

### Input Validation

```python
from kei_agent import get_input_validator

def validation_demo():
    validator = get_input_validator()
    
    # Agent-Operation validieren
    operation_data = {
        "objective": "Erstelle einen Bericht",
        "context": {
            "format": "pdf",
            "deadline": "2024-12-31"
        }
    }
    
    result = validator.validate_agent_operation("plan", operation_data)
    
    if result.valid:
        print("✅ Input-Validierung erfolgreich")
        print(f"Bereinigte Daten: {result.sanitized_value}")
    else:
        print("❌ Validierungsfehler:")
        for error in result.errors:
            print(f"  - {error}")

validation_demo()
```

## 🔧 Erweiterte Konfiguration

### Vollständige Client-Konfiguration

```python
from kei_agent import (
    UnifiedKeiAgentClient,
    AgentClientConfig,
    ProtocolConfig,
    SecurityConfig,
    AuthType
)

async def advanced_config_demo():
    # Basis-Konfiguration
    agent_config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="advanced-agent",
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
        audit_enabled=True,
        token_refresh_enabled=True
    )
    
    # Client mit vollständiger Konfiguration
    async with UnifiedKeiAgentClient(
        config=agent_config,
        protocol_config=protocol_config,
        security_config=security_config
    ) as client:
        print("🚀 Erweiterte Konfiguration aktiv")
        
        # Client-Informationen
        info = client.get_client_info()
        print(f"Features: {info['features']}")
        print(f"Security Context: {info['security_context']}")

asyncio.run(advanced_config_demo())
```

## 🎯 Praktische Beispiele

### Agent-to-Agent Kommunikation

```python
async def agent_communication_demo():
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="sender-agent"
    )
    
    async with UnifiedKeiAgentClient(config=config) as client:
        # Nachricht an anderen Agent senden
        response = await client.send_agent_message(
            target_agent="receiver-agent",
            message_type="task_request",
            payload={
                "task": "data_analysis",
                "dataset": "sales_q4_2024",
                "priority": "high"
            }
        )
        print(f"Nachricht gesendet: {response['message_id']}")

asyncio.run(agent_communication_demo())
```

### Tool-Integration mit MCP

```python
async def tool_integration_demo():
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="tool-agent"
    )
    
    async with UnifiedKeiAgentClient(config=config) as client:
        # Verfügbare Tools entdecken
        tools = await client.discover_available_tools("math")
        print(f"Verfügbare Math-Tools: {[tool['name'] for tool in tools]}")
        
        # Tool verwenden
        if tools:
            result = await client.use_tool(
                "calculator",
                expression="(100 * 1.08) - 50"
            )
            print(f"Berechnungsergebnis: {result['result']}")

asyncio.run(tool_integration_demo())
```

## 🚨 Fehlerbehandlung

```python
from kei_agent.exceptions import KeiSDKError, ProtocolError, SecurityError

async def error_handling_demo():
    config = AgentClientConfig(
        base_url="https://invalid-url.example.com",
        api_token="invalid-token",
        agent_id="error-demo-agent"
    )
    
    try:
        async with UnifiedKeiAgentClient(config=config) as client:
            await client.plan_task("Test-Plan")
            
    except SecurityError as e:
        print(f"🔒 Sicherheitsfehler: {e}")
    except ProtocolError as e:
        print(f"🔌 Protokollfehler: {e}")
    except KeiSDKError as e:
        print(f"⚠️ SDK-Fehler: {e}")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")

asyncio.run(error_handling_demo())
```

## 🎉 Nächste Schritte

Herzlichen Glückwunsch! Sie haben die Grundlagen des KEI-Agent SDK gelernt. Hier sind Ihre nächsten Schritte:

### Vertiefen Sie Ihr Wissen
- [**Basis-Konzepte**](../user-guide/concepts.md) - Verstehen Sie die Architektur
- [**Client-Verwendung**](../user-guide/client-usage.md) - Erweiterte Client-Features
- [**Protokolle**](../user-guide/protocols.md) - Multi-Protocol Deep Dive

### Enterprise Features erkunden
- [**Structured Logging**](../enterprise/logging.md) - Production-Logging
- [**Health Checks**](../enterprise/health-checks.md) - System-Monitoring
- [**Security**](../enterprise/security.md) - Sicherheits-Features

### Praktische Anwendung
- [**Beispiele**](../examples/index.md) - Umfassende Code-Beispiele
- [**API-Referenz**](../api/index.md) - Vollständige API-Dokumentation

---

**Bereit für mehr?** Erkunden Sie die [Basis-Konzepte →](../user-guide/concepts.md)
