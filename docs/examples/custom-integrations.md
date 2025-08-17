# 🧰 Custom Integrations

Eigene Erweiterungen und Integrationen mit dem KEI-Agent Python SDK.

## Eigener Protocol-Client

```python
from typing import Dict, Any
from protocol_clients import BaseProtocolClient
from security_manager import SecurityManager

class CustomProtocolClient(BaseProtocolClient):
    """Beispiel für einen benutzerdefinierten Protocol-Client."""

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False

    async def do_custom_call(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = await self._get_auth_headers()
        # Hier würde die echte Kommunikation stattfinden
        return {"status": "ok", "echo": payload, "headers": headers}
```

## Nutzung im Unified Client

```python
from kei_agent import UnifiedKeiAgentClient, AgentClientConfig

async def use_custom_protocol():
    client = UnifiedKeiAgentClient(AgentClientConfig(
        base_url="https://api.kei-framework.com",
        api_token="your-token",
        agent_id="custom-protocol-agent"
    ))
    # Custom client könnte parallel verwendet und in eigene Workflows integriert werden
```
