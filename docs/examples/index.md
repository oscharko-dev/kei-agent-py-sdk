# Beispiele

Praktische Code-Beispiele für verschiedene Anwendungsfälle des KEI-Agent Python SDK.

## 📚 Beispiel-Kategorien

### Grundlagen
- [**Basis-Verwendung**](basic-usage.md) - Einfache Agent-Operationen und Client-Setup
- [**Multi-Protocol**](multi-protocol.md) - Verwendung verschiedener Protokolle
- [**Enterprise Setup**](enterprise-setup.md) - Production-ready Konfiguration

### Erweiterte Anwendungen
- [**Custom Integrations**](custom-integrations.md) - Eigene Protokoll-Clients und Validatoren
- [**Performance Tuning**](performance-tuning.md) - Optimierung für High-Performance Szenarien

## 🚀 Quick Start Beispiele

### Einfacher Agent-Client

```python
import asyncio
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig

async def simple_agent_example():
    """Einfaches Beispiel für Agent-Operationen."""

    # Konfiguration
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="simple-example-agent"
    )

    # Client verwenden
    async with UnifiedKeiAgentClient(config=config) as client:
        # Plan erstellen
        plan = await client.plan_task(
            objective="Analysiere Verkaufsdaten für Q4 2024",
            context={
                "data_source": "sales_database",
                "format": "quarterly_report",
                "include_charts": True
            }
        )
        print(f"Plan erstellt: {plan['plan_id']}")

        # Aktion ausführen
        result = await client.execute_action(
            action="analyze_sales_data",
            parameters={
                "quarter": "Q4-2024",
                "include_trends": True,
                "output_format": "pdf"
            }
        )
        print(f"Analyse abgeschlossen: {result['action_id']}")

        # Ergebnis erklären
        explanation = await client.explain_reasoning(
            query="Welche Trends wurden in den Verkaufsdaten identifiziert?",
            context={"action_id": result['action_id']}
        )
        print(f"Erklärung: {explanation['explanation']}")

# Ausführen
asyncio.run(simple_agent_example())
```

### Multi-Agent Kommunikation

```python
async def multi_agent_example():
    """Beispiel für Agent-to-Agent Kommunikation."""

    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="coordinator-agent"
    )

    async with UnifiedKeiAgentClient(config=config) as client:
        # Aufgabe an Datenanalyse-Agent delegieren
        response = await client.send_agent_message(
            target_agent="data-analysis-agent",
            message_type="analysis_request",
            payload={
                "dataset": "customer_behavior_2024",
                "analysis_type": "clustering",
                "priority": "high",
                "deadline": "2024-12-31T23:59:59Z"
            }
        )
        print(f"Nachricht gesendet: {response['message_id']}")

        # Aufgabe an Report-Generator delegieren
        report_response = await client.send_agent_message(
            target_agent="report-generator-agent",
            message_type="report_request",
            payload={
                "template": "executive_summary",
                "data_source": response['message_id'],
                "format": "pdf",
                "recipients": ["ceo@company.com", "cfo@company.com"]
            }
        )
        print(f"Report-Request gesendet: {report_response['message_id']}")

asyncio.run(multi_agent_example())
```

### Tool-Integration mit MCP

```python
async def tool_integration_example():
    """Beispiel für Tool-Integration über MCP."""

    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="tool-integration-agent"
    )

    async with UnifiedKeiAgentClient(config=config) as client:
        # Verfügbare Tools entdecken
        math_tools = await client.discover_available_tools("math")
        print(f"Verfügbare Math-Tools: {[tool['name'] for tool in math_tools]}")

        data_tools = await client.discover_available_tools("data")
        print(f"Verfügbare Data-Tools: {[tool['name'] for tool in data_tools]}")

        # Calculator-Tool verwenden
        if any(tool['name'] == 'calculator' for tool in math_tools):
            calc_result = await client.use_tool(
                "calculator",
                expression="(1000 * 1.08) + (500 * 0.95) - 200"
            )
            print(f"Berechnungsergebnis: {calc_result['result']}")

        # CSV-Analyzer-Tool verwenden
        if any(tool['name'] == 'csv_analyzer' for tool in data_tools):
            analysis_result = await client.use_tool(
                "csv_analyzer",
                file_path="/data/sales_q4_2024.csv",
                analysis_type="summary_statistics"
            )
            print(f"CSV-Analyse: {analysis_result['summary']}")

asyncio.run(tool_integration_example())
```

## 🔧 Konfiguration-Beispiele

### Development-Konfiguration

```python
from kei_agent import ProtocolConfig, SecurityConfig, AuthType

def create_development_config():
    """Erstellt Development-Konfiguration."""

    agent_config = AgentClientConfig(
        base_url="http://localhost:8000",
        api_token="dev-token",
        agent_id="dev-agent",
        timeout=10,
        max_retries=1
    )

    # Vereinfachte Protokoll-Konfiguration
    protocol_config = ProtocolConfig(
        rpc_enabled=True,
        stream_enabled=False,  # Vereinfacht für Development
        bus_enabled=False,
        mcp_enabled=True,
        auto_protocol_selection=False
    )

    # Einfache Security für Development
    security_config = SecurityConfig(
        auth_type=AuthType.BEARER,
        api_token="dev-token",
        rbac_enabled=False,
        audit_enabled=False
    )

    return agent_config, protocol_config, security_config
```

### Production-Konfiguration

```python
def create_production_config():
    """Erstellt Production-Konfiguration."""

    agent_config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token=os.getenv("KEI_API_TOKEN"),
        agent_id=f"prod-agent-{socket.gethostname()}",
        timeout=30,
        max_retries=5,
        retry_delay=2.0
    )

    # Vollständige Protokoll-Unterstützung
    protocol_config = ProtocolConfig(
        rpc_enabled=True,
        stream_enabled=True,
        bus_enabled=True,
        mcp_enabled=True,
        auto_protocol_selection=True,
        protocol_fallback_enabled=True
    )

    # Enterprise Security
    security_config = SecurityConfig(
        auth_type=AuthType.OIDC,
        oidc_issuer=os.getenv("OIDC_ISSUER"),
        oidc_client_id=os.getenv("OIDC_CLIENT_ID"),
        oidc_client_secret=os.getenv("OIDC_CLIENT_SECRET"),
        rbac_enabled=True,
        audit_enabled=True,
        token_refresh_enabled=True
    )

    return agent_config, protocol_config, security_config
```

## 📊 Monitoring-Beispiele

### Health Check Setup

```python
from kei_agent import get_health_manager, APIHealthCheck, MemoryHealthCheck

async def setup_monitoring():
    """Richtet umfassendes Monitoring ein."""

    health_manager = get_health_manager()

    # API Health Checks
    health_manager.register_check(APIHealthCheck(
        name="kei_api",
        url="https://api.kei-framework.com/health",
        timeout_seconds=10,
        critical=True
    ))

    health_manager.register_check(APIHealthCheck(
        name="external_data_api",
        url="https://data-api.company.com/health",
        timeout_seconds=5,
        critical=False
    ))

    # System Health Checks
    health_manager.register_check(MemoryHealthCheck(
        name="system_memory",
        warning_threshold=0.8,
        critical_threshold=0.95,
        critical=True
    ))

    # Kontinuierliches Monitoring
    while True:
        summary = await health_manager.run_all_checks()

        if summary.overall_status != "healthy":
            print(f"⚠️ System Status: {summary.overall_status}")
            for check in summary.checks:
                if check.status != "healthy":
                    print(f"  - {check.name}: {check.status} - {check.message}")
        else:
            print("✅ All systems healthy")

        await asyncio.sleep(60)  # Check every minute

# Background monitoring starten
asyncio.create_task(setup_monitoring())
```

### Performance Monitoring

```python
import time
import psutil
from kei_agent import get_logger

async def performance_monitoring_example():
    """Beispiel für Performance-Monitoring."""

    logger = get_logger("performance_monitor")

    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="performance-monitored-agent"
    )

    async with UnifiedKeiAgentClient(config=config) as client:
        # Performance-Tracking für Operation
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss

        try:
            # Agent-Operation ausführen
            result = await client.plan_task("Performance-Test-Operation")

            # Performance-Metriken berechnen
            duration = (time.time() - start_time) * 1000
            end_memory = psutil.Process().memory_info().rss
            memory_delta = (end_memory - start_memory) / 1024 / 1024  # MB

            # Performance-Metriken loggen
            logger.log_performance(
                operation="plan_task",
                duration_ms=duration,
                memory_usage=memory_delta,
                cpu_usage=psutil.cpu_percent(),
                success=True
            )

            print(f"Operation completed in {duration:.2f}ms")
            print(f"Memory usage: {memory_delta:.2f}MB")

        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.log_performance(
                operation="plan_task",
                duration_ms=duration,
                success=False,
                error=str(e)
            )
            raise

asyncio.run(performance_monitoring_example())
```

## 🔐 Security-Beispiele

### Input Validation

```python
from kei_agent import get_input_validator, ValidationSeverity

def secure_input_handling_example():
    """Beispiel für sichere Input-Verarbeitung."""

    validator = get_input_validator()

    # Unsichere Eingaben testen
    test_inputs = [
        {
            "objective": "Normal objective",
            "context": {"format": "pdf"}
        },
        {
            "objective": "<script>alert('xss')</script>",
            "context": {"format": "pdf"}
        },
        {
            "objective": "'; DROP TABLE users; --",
            "context": {"format": "pdf"}
        }
    ]

    for i, input_data in enumerate(test_inputs):
        print(f"\n--- Test Input {i+1} ---")

        result = validator.validate_agent_operation("plan", input_data)

        if result.valid:
            print("✅ Input valid")
            print(f"Sanitized: {result.sanitized_value}")
        else:
            print("❌ Input invalid")
            for error in result.errors:
                print(f"  Error: {error}")
            for warning in result.warnings:
                print(f"  Warning: {warning}")

secure_input_handling_example()
```

### Audit Logging

```python
from kei_agent import get_logger, LogContext

async def audit_logging_example():
    """Beispiel für Audit-Logging."""

    logger = get_logger("audit_example")

    # Audit-Kontext setzen
    logger.set_context(LogContext(
        correlation_id=logger.create_correlation_id(),
        user_id="user-123",
        agent_id="audit-agent",
        operation="sensitive_data_access"
    ))

    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="audit-agent"
    )

    async with UnifiedKeiAgentClient(config=config) as client:
        # Sensitive Operation mit Audit-Logging
        logger.log_security_event(
            event_type="sensitive_operation_started",
            severity="info",
            description="User accessing sensitive financial data",
            user_id="user-123",
            resource="financial_reports",
            action="read"
        )

        try:
            result = await client.plan_task(
                "Generate confidential financial report",
                context={"classification": "confidential"}
            )

            logger.log_security_event(
                event_type="sensitive_operation_completed",
                severity="info",
                description="Sensitive operation completed successfully",
                result_id=result.get('plan_id')
            )

        except Exception as e:
            logger.log_security_event(
                event_type="sensitive_operation_failed",
                severity="error",
                description="Sensitive operation failed",
                error=str(e)
            )
            raise

asyncio.run(audit_logging_example())
```

## 🔄 Error Handling Beispiele

### Robuste Fehlerbehandlung

```python
from kei_agent.exceptions import KeiSDKError, ProtocolError, SecurityError

async def robust_error_handling_example():
    """Beispiel für robuste Fehlerbehandlung."""

    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="error-handling-agent"
    )

    async with UnifiedKeiAgentClient(config=config) as client:
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(max_retries):
            try:
                result = await client.plan_task("Potentially failing operation")
                print(f"✅ Operation successful: {result['plan_id']}")
                break

            except SecurityError as e:
                print(f"🔒 Security error (attempt {attempt + 1}): {e}")
                # Security errors sind nicht retry-bar
                raise

            except ProtocolError as e:
                print(f"🔌 Protocol error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("❌ All retry attempts failed")
                    raise

            except KeiSDKError as e:
                print(f"⚠️ SDK error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                else:
                    raise

            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                raise

asyncio.run(robust_error_handling_example())
```

## 📁 Vollständige Anwendungsbeispiele

Die folgenden Seiten enthalten vollständige, ausführbare Beispiele für spezifische Anwendungsfälle:

- **[Basis-Verwendung →](basic-usage.md)** - Grundlegende Agent-Operationen
- **[Multi-Protocol →](multi-protocol.md)** - Protokoll-spezifische Features
- **[Enterprise Setup →](enterprise-setup.md)** - Production-Deployment
- **[Custom Integrations →](custom-integrations.md)** - Erweiterungen und Anpassungen
- **[Performance Tuning →](performance-tuning.md)** - Optimierung für High-Performance

---

**Tipp:** Alle Beispiele sind vollständig ausführbar. Ersetzen Sie einfach die Platzhalter-Werte (API-Token, URLs) durch Ihre tatsächlichen Konfigurationsdaten.
