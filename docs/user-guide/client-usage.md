# Client-Verwendung

*Diese Seite wird noch entwickelt.*

## Übersicht

Hier finden Sie detaillierte Informationen zur Verwendung des UnifiedKeiAgentClient.

## Grundlegende Verwendung

```python
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig

# Client konfigurieren
config = AgentClientConfig(
    base_url="https://your-kei-agent.com",
    api_token="your-api-token",
    agent_id="your-agent-id"
)

# Client verwenden
async with UnifiedKeiAgentClient(config) as client:
    result = await client.plan_task("Ihre Aufgabe")
    print(result)
```

## Weitere Informationen

- [Basis-Konzepte](concepts.md)
- [Protokolle](protocols.md)
- [Authentifizierung](authentication.md)
