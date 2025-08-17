# 🧩 Basis-Verwendung

Einfaches, ausführbares Beispiel für den Einstieg mit dem `UnifiedKeiAgentClient`.

## Voraussetzungen

- Python 3.8+
- Installation des SDKs:

```bash
pip install kei_agent_py_sdk
```

## Beispiel

```python
import asyncio
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig

async def main():
    # Konfiguration
    config = AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-api-token",
        agent_id="basic-usage-agent"
    )

    # Client verwenden (Async Context Manager)
    async with UnifiedKeiAgentClient(config=config) as client:
        # Plan erstellen
        plan = await client.plan_task(
            objective="Erstelle einen Quartalsbericht",
            context={"format": "pdf", "quarter": "Q4-2024"}
        )
        print(f"Plan erstellt: {plan.get('plan_id')}")

        # Aktion ausführen
        result = await client.execute_action(
            action="generate_report",
            parameters={"template": "quarterly", "data_source": "financial_db"}
        )
        print(f"Report generiert: {result.get('action_id')}")

        # Health Check
        health = await client.health_check()
        print(f"System Status: {health.get('status')}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Hinweise

- Platzhalter (`your-api-token`) durch reale Werte ersetzen
- Für lokale Tests kann ein Mock-/Staging-Endpunkt verwendet werden
