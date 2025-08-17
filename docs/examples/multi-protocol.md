# 🌐 Multi-Protocol Examples

Beispiele für die Nutzung verschiedener Kommunikationsprotokolle in Keiko Personal Assistant.

## 🔌 Protocol-Client-Setup

### HTTP/REST-Client

```python
from keiko.protocols.http import HTTPClient, HTTPConfig

# HTTP-Client konfigurieren
http_config = HTTPConfig(
    base_url="https://api.example.com",
    timeout=30.0,
    max_retries=3,
    auth_token="your-api-token",
    verify_ssl=True
)

# Client verwenden
async with HTTPClient(http_config) as client:
    # GET-Request
    response = await client.get("/users", params={"limit": 10})
    users = response.json["users"]

    # POST-Request
    new_user = {
        "username": "newuser",
        "email": "user@example.com"
    }
    response = await client.post("/users", data=new_user)
    created_user = response.json

    print(f"Benutzer erstellt: {created_user['id']}")
```

### WebSocket-Client

```python
from keiko.protocols.websocket import WebSocketClient, WebSocketConfig

# WebSocket-Client konfigurieren
ws_config = WebSocketConfig(
    url="wss://api.example.com/ws",
    auth_token="your-token",
    ping_interval=30.0,
    max_message_size=1024*1024
)

# Event-Handler definieren
async def handle_notification(data):
    print(f"Benachrichtigung: {data['message']}")

async def handle_task_update(data):
    print(f"Task-Update: {data['task_id']} -> {data['status']}")

# Client verwenden
client = WebSocketClient(ws_config)

# Handler registrieren
client.register_handler("notification", handle_notification)
client.register_handler("task_update", handle_task_update)

# Verbindung herstellen
await client.connect()

# Nachrichten senden
await client.send_message("subscribe", {
    "events": ["notifications", "task_updates"],
    "user_id": "user123"
})

# Verbindung offen halten
try:
    while client.is_connected:
        await asyncio.sleep(1)
except KeyboardInterrupt:
    await client.disconnect()
```

### MCP-Client

```python
from keiko.protocols.mcp import MCPClient

# MCP-Client konfigurieren
mcp_config = {
    'server_url': 'http://localhost:8080',
    'auth_config': {
        'type': 'api_key',
        'api_key': 'your-mcp-key'
    }
}

async with MCPClient(**mcp_config) as client:
    # Server-Informationen abrufen
    server_info = await client.get_server_info()
    print(f"MCP-Server: {server_info['name']} v{server_info['version']}")

    # Verfügbare Tools auflisten
    tools = await client.list_tools()
    for tool in tools:
        print(f"Tool: {tool['name']} - {tool['description']}")

    # Tool ausführen
    result = await client.execute_tool(
        tool_name="weather_forecast",
        arguments={
            "location": "Berlin, Germany",
            "days": 3
        }
    )

    print(f"Wettervorhersage: {result}")
```

## 🎯 Protocol-Selection

### Automatische Protocol-Auswahl

```python
from keiko.protocols import ProtocolSelector, ProtocolRequirements, ServiceCapabilities

# Service-Capabilities definieren
service_caps = ServiceCapabilities(
    supports_http=True,
    supports_websocket=True,
    supports_grpc=False,
    supports_mcp=True,
    real_time_required=False,
    high_throughput=False
)

# Anforderungen definieren
requirements = ProtocolRequirements(
    operation_type="query",
    data_size=1024,  # 1KB
    expected_response_time=2.0,
    reliability_level="normal"
)

# Protocol-Selector verwenden
selector = ProtocolSelector()
best_protocol = selector.select_protocol(service_caps, requirements)

print(f"Empfohlenes Protokoll: {best_protocol.protocol.value}")
print(f"Score: {best_protocol.score:.2f}")
print(f"Gründe: {best_protocol.reasons}")
```

### Conditional Protocol Usage

```python
class AdaptiveClient:
    """Client der sich automatisch an verfügbare Protokolle anpasst."""

    def __init__(self, service_url: str):
        self.service_url = service_url
        self.available_protocols = self._detect_protocols()
        self.current_client = None

    async def _detect_protocols(self) -> List[str]:
        """Erkennt verfügbare Protokolle."""
        protocols = []

        # HTTP-Verfügbarkeit prüfen
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.service_url}/health") as response:
                    if response.status == 200:
                        protocols.append("http")
        except:
            pass

        # WebSocket-Verfügbarkeit prüfen
        try:
            ws_url = self.service_url.replace("http", "ws") + "/ws"
            async with websockets.connect(ws_url) as ws:
                protocols.append("websocket")
        except:
            pass

        return protocols

    async def send_request(self, operation: str, data: dict) -> dict:
        """Sendet Request mit bestem verfügbaren Protokoll."""

        if operation == "real_time_stream" and "websocket" in self.available_protocols:
            return await self._send_websocket_request(operation, data)
        elif "http" in self.available_protocols:
            return await self._send_http_request(operation, data)
        else:
            raise Exception("Keine verfügbaren Protokolle")

    async def _send_http_request(self, operation: str, data: dict) -> dict:
        """Sendet HTTP-Request."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.service_url}/api/{operation}",
                json=data
            ) as response:
                return await response.json()

    async def _send_websocket_request(self, operation: str, data: dict) -> dict:
        """Sendet WebSocket-Request."""
        ws_url = self.service_url.replace("http", "ws") + "/ws"

        async with websockets.connect(ws_url) as ws:
            request = {
                "operation": operation,
                "data": data,
                "request_id": str(uuid.uuid4())
            }

            await ws.send(json.dumps(request))
            response = await ws.recv()
            return json.loads(response)

# Verwendung
client = AdaptiveClient("http://localhost:8000")

# Normale Anfrage (wird HTTP verwenden)
result = await client.send_request("get_data", {"query": "users"})

# Real-Time-Anfrage (wird WebSocket verwenden wenn verfügbar)
stream_result = await client.send_request("real_time_stream", {"topic": "events"})
```

## 🔄 Protocol-Switching

### Fallback-Mechanismus

```python
class ResilientClient:
    """Client mit automatischem Protocol-Fallback."""

    def __init__(self, config: dict):
        self.config = config
        self.protocol_priority = ["grpc", "websocket", "http"]
        self.clients = {}

    async def initialize(self):
        """Initialisiert verfügbare Clients."""

        # HTTP-Client (immer verfügbar)
        self.clients["http"] = HTTPClient(HTTPConfig(**self.config["http"]))

        # WebSocket-Client (optional)
        if "websocket" in self.config:
            try:
                self.clients["websocket"] = WebSocketClient(
                    WebSocketConfig(**self.config["websocket"])
                )
                await self.clients["websocket"].connect()
            except Exception as e:
                print(f"WebSocket nicht verfügbar: {e}")

        # gRPC-Client (optional)
        if "grpc" in self.config:
            try:
                self.clients["grpc"] = GRPCClient(GRPCConfig(**self.config["grpc"]))
                await self.clients["grpc"].connect()
            except Exception as e:
                print(f"gRPC nicht verfügbar: {e}")

    async def execute_with_fallback(self, operation: str, data: dict) -> dict:
        """Führt Operation mit Fallback-Mechanismus aus."""

        last_error = None

        for protocol in self.protocol_priority:
            if protocol not in self.clients:
                continue

            try:
                client = self.clients[protocol]

                if protocol == "http":
                    return await client.post(f"/api/{operation}", data=data)
                elif protocol == "websocket":
                    await client.send_message(operation, data)
                    # Warten auf Response (vereinfacht)
                    return {"status": "sent"}
                elif protocol == "grpc":
                    # gRPC-spezifische Implementierung
                    return await client.call_method(operation, data)

            except Exception as e:
                last_error = e
                print(f"Protokoll {protocol} fehlgeschlagen: {e}")
                continue

        raise Exception(f"Alle Protokolle fehlgeschlagen. Letzter Fehler: {last_error}")

# Verwendung
config = {
    "http": {
        "base_url": "http://localhost:8000",
        "timeout": 30.0
    },
    "websocket": {
        "url": "ws://localhost:8000/ws"
    },
    "grpc": {
        "server_address": "localhost:9000"
    }
}

client = ResilientClient(config)
await client.initialize()

# Operation ausführen (automatischer Fallback)
result = await client.execute_with_fallback("process_data", {
    "input": "test data",
    "options": {"format": "json"}
})
```

## 📊 Protocol-Performance-Monitoring

### Performance-Vergleich

```python
import time
from typing import Dict, List

class ProtocolBenchmark:
    """Benchmark für verschiedene Protokolle."""

    def __init__(self):
        self.results: Dict[str, List[float]] = {}

    async def benchmark_protocol(
        self,
        protocol_name: str,
        client,
        operation: str,
        data: dict,
        iterations: int = 100
    ):
        """Benchmarkt ein Protokoll."""

        times = []

        for i in range(iterations):
            start_time = time.time()

            try:
                if protocol_name == "http":
                    await client.post(f"/api/{operation}", data=data)
                elif protocol_name == "websocket":
                    await client.send_message(operation, data)
                elif protocol_name == "grpc":
                    await client.call_method(operation, data)

                duration = time.time() - start_time
                times.append(duration)

            except Exception as e:
                print(f"Fehler in Iteration {i}: {e}")

        self.results[protocol_name] = times

        # Statistiken berechnen
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"{protocol_name} Benchmark:")
        print(f"  Durchschnitt: {avg_time:.3f}s")
        print(f"  Minimum: {min_time:.3f}s")
        print(f"  Maximum: {max_time:.3f}s")
        print(f"  Erfolgreiche Requests: {len(times)}/{iterations}")

    async def compare_protocols(self):
        """Vergleicht alle benchmarkten Protokolle."""

        if not self.results:
            print("Keine Benchmark-Daten verfügbar")
            return

        print("\nProtokoll-Vergleich:")
        print("-" * 50)

        for protocol, times in self.results.items():
            avg_time = sum(times) / len(times)
            throughput = len(times) / sum(times)

            print(f"{protocol:12} | Avg: {avg_time:.3f}s | Throughput: {throughput:.1f} req/s")

# Benchmark ausführen
benchmark = ProtocolBenchmark()

# HTTP-Benchmark
http_client = HTTPClient(HTTPConfig(base_url="http://localhost:8000"))
await benchmark.benchmark_protocol(
    "http", http_client, "echo", {"message": "test"}, 100
)

# WebSocket-Benchmark
ws_client = WebSocketClient(WebSocketConfig(url="ws://localhost:8000/ws"))
await ws_client.connect()
await benchmark.benchmark_protocol(
    "websocket", ws_client, "echo", {"message": "test"}, 100
)

# Vergleich anzeigen
await benchmark.compare_protocols()
```

## 🔧 Protocol-Konfiguration

### Umgebungs-spezifische Protokolle

```python
# config/protocols.py
PROTOCOL_CONFIGS = {
    "development": {
        "preferred_protocols": ["http", "websocket"],
        "http": {
            "base_url": "http://localhost:8000",
            "timeout": 30.0,
            "verify_ssl": False
        },
        "websocket": {
            "url": "ws://localhost:8000/ws",
            "ping_interval": 30.0
        }
    },
    "production": {
        "preferred_protocols": ["grpc", "https", "websocket"],
        "https": {
            "base_url": "https://api.keiko.com",
            "timeout": 10.0,
            "verify_ssl": True,
            "cert_file": "/etc/ssl/client.pem"
        },
        "grpc": {
            "server_address": "grpc.keiko.com:443",
            "use_tls": True
        },
        "websocket": {
            "url": "wss://api.keiko.com/ws",
            "ping_interval": 60.0
        }
    }
}

def get_protocol_config(environment: str = "development") -> dict:
    """Lädt Protocol-Konfiguration für Umgebung."""
    return PROTOCOL_CONFIGS.get(environment, PROTOCOL_CONFIGS["development"])

# Verwendung
import os
env = os.getenv("ENVIRONMENT", "development")
config = get_protocol_config(env)

# Client-Factory mit Umgebungs-Konfiguration
class ProtocolClientFactory:
    """Factory für umgebungs-spezifische Protocol-Clients."""

    @staticmethod
    def create_clients(config: dict) -> Dict[str, Any]:
        """Erstellt Clients basierend auf Konfiguration."""
        clients = {}

        for protocol in config["preferred_protocols"]:
            if protocol in config:
                if protocol == "http" or protocol == "https":
                    clients[protocol] = HTTPClient(HTTPConfig(**config[protocol]))
                elif protocol == "websocket":
                    clients[protocol] = WebSocketClient(WebSocketConfig(**config[protocol]))
                elif protocol == "grpc":
                    clients[protocol] = GRPCClient(GRPCConfig(**config[protocol]))

        return clients

# Clients erstellen
clients = ProtocolClientFactory.create_clients(config)
```

## 🚀 Advanced Protocol Usage

### Protocol-Multiplexing

```python
class MultiplexedClient:
    """Client der mehrere Protokolle gleichzeitig nutzt."""

    def __init__(self, clients: Dict[str, Any]):
        self.clients = clients
        self.load_balancer = RoundRobinBalancer(list(clients.keys()))

    async def parallel_request(self, operation: str, data: dict) -> List[dict]:
        """Sendet Request parallel über alle Protokolle."""

        tasks = []
        for protocol, client in self.clients.items():
            task = asyncio.create_task(
                self._send_request(protocol, client, operation, data)
            )
            tasks.append(task)

        # Warten auf alle Responses
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Erfolgreiche Responses filtern
        successful_results = [
            result for result in results
            if not isinstance(result, Exception)
        ]

        return successful_results

    async def fastest_response(self, operation: str, data: dict) -> dict:
        """Nutzt das schnellste verfügbare Protokoll."""

        tasks = []
        for protocol, client in self.clients.items():
            task = asyncio.create_task(
                self._send_request(protocol, client, operation, data)
            )
            tasks.append(task)

        # Erstes erfolgreiches Ergebnis zurückgeben
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED
        )

        # Verbleibende Tasks abbrechen
        for task in pending:
            task.cancel()

        # Erstes Ergebnis zurückgeben
        result = done.pop().result()
        return result

    async def _send_request(self, protocol: str, client, operation: str, data: dict) -> dict:
        """Sendet Request über spezifisches Protokoll."""

        if protocol == "http":
            response = await client.post(f"/api/{operation}", data=data)
            return response.json
        elif protocol == "websocket":
            await client.send_message(operation, data)
            return {"protocol": protocol, "status": "sent"}
        # Weitere Protokolle...

# Verwendung
multiplexed = MultiplexedClient(clients)

# Parallele Requests
all_results = await multiplexed.parallel_request("get_status", {})
print(f"Ergebnisse von {len(all_results)} Protokollen")

# Schnellste Response
fastest = await multiplexed.fastest_response("get_data", {"id": 123})
print(f"Schnellste Antwort: {fastest}")
```

!!! tip "Protocol-Auswahl"
    Wählen Sie das Protokoll basierend auf Ihren spezifischen Anforderungen:
    - **HTTP**: Einfache Request/Response-Patterns
    - **WebSocket**: Real-Time-Kommunikation
    - **gRPC**: High-Performance mit starker Typisierung
    - **MCP**: Model Context Protocol-spezifische Operationen

!!! info "Performance-Optimierung"
    Nutzen Sie Connection-Pooling, Keep-Alive und Compression für bessere Performance bei allen Protokollen.
