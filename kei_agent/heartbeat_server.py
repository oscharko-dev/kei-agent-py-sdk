"""
Agent Heartbeat Server

Einfacher HTTP-Server für Agent-Heartbeat-Checks.
Läuft parallel zum Agent und antwortet auf Heartbeat-Requests der Platform.
"""

import time
from typing import Optional
from aiohttp import web
import logging

logger = logging.getLogger(__name__)


class AgentHeartbeatServer:
    """Einfacher Heartbeat-Server für Agents."""

    def __init__(self, port: int = 8080, host: str = "0.0.0.0"):
        """Initialisiert den Heartbeat-Server.

        Args:
            port: Port für den Server
            host: Host-Adresse
        """
        self.port = port
        self.host = host
        self.app = None
        self.runner = None
        self.site = None
        self.start_time = time.time()
        self.agent_info = {}

    def set_agent_info(self, agent_id: str, name: str, capabilities: list):
        """Setzt Agent-Informationen für Heartbeat-Response.

        Args:
            agent_id: Agent-ID
            name: Agent-Name
            capabilities: Agent-Capabilities
        """
        self.agent_info = {
            "agent_id": agent_id,
            "name": name,
            "capabilities": capabilities,
            "start_time": self.start_time,
            "status": "running",
        }

    async def heartbeat_handler(self, request):
        """Handler für Heartbeat-Requests."""
        uptime = time.time() - self.start_time

        response_data = {
            "status": "alive",
            "timestamp": time.time(),
            "uptime_seconds": uptime,
            **self.agent_info,
        }

        logger.debug(f"Heartbeat-Request beantwortet: {response_data}")
        return web.json_response(response_data)

    async def health_handler(self, request):
        """Handler für Health-Checks."""
        return web.json_response(
            {
                "status": "healthy",
                "timestamp": time.time(),
                "uptime_seconds": time.time() - self.start_time,
            }
        )

    async def start(self):
        """Startet den Heartbeat-Server."""
        if self.runner:
            return  # Bereits gestartet

        self.app = web.Application()
        self.app.router.add_get("/heartbeat", self.heartbeat_handler)
        self.app.router.add_get("/health", self.health_handler)
        self.app.router.add_get("/", self.health_handler)  # Fallback

        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()

        logger.info(f"💓 Heartbeat-Server gestartet auf {self.host}:{self.port}")

    async def stop(self):
        """Stoppt den Heartbeat-Server."""
        if self.site:
            await self.site.stop()
            self.site = None

        if self.runner:
            await self.runner.cleanup()
            self.runner = None

        self.app = None
        logger.info("💓 Heartbeat-Server gestoppt")

    def get_heartbeat_url(self) -> str:
        """Gibt die Heartbeat-URL zurück."""
        return f"http://{self.host}:{self.port}/heartbeat"


class AgentHeartbeatManager:
    """Manager für Agent-Heartbeat-Funktionalität."""

    def __init__(self, agent_id: str, name: str = "", capabilities: list = None):
        """Initialisiert den Heartbeat-Manager.

        Args:
            agent_id: Agent-ID
            name: Agent-Name
            capabilities: Agent-Capabilities
        """
        self.agent_id = agent_id
        self.name = name or agent_id
        self.capabilities = capabilities or []
        self.server: Optional[AgentHeartbeatServer] = None
        self.auto_port = True
        self.port = 8080

    async def start_heartbeat_server(
        self, port: int = None, host: str = "0.0.0.0"
    ) -> str:
        """Startet den Heartbeat-Server.

        Args:
            port: Port für den Server (None für automatische Auswahl)
            host: Host-Adresse

        Returns:
            Heartbeat-URL
        """
        if self.server:
            return self.server.get_heartbeat_url()

        # Automatische Port-Auswahl wenn nicht angegeben
        if port is None:
            port = await self._find_free_port()

        self.port = port
        self.server = AgentHeartbeatServer(port=port, host=host)
        self.server.set_agent_info(self.agent_id, self.name, self.capabilities)

        try:
            await self.server.start()
            heartbeat_url = self.server.get_heartbeat_url()
            logger.info(
                f"✅ Heartbeat-Server für Agent {self.agent_id} gestartet: {heartbeat_url}"
            )
            return heartbeat_url
        except Exception as e:
            logger.error(f"❌ Fehler beim Starten des Heartbeat-Servers: {e}")
            self.server = None
            raise

    async def stop_heartbeat_server(self):
        """Stoppt den Heartbeat-Server."""
        if self.server:
            await self.server.stop()
            self.server = None
            logger.info(f"🛑 Heartbeat-Server für Agent {self.agent_id} gestoppt")

    async def _find_free_port(
        self, start_port: int = 8080, max_attempts: int = 100
    ) -> int:
        """Findet einen freien Port.

        Args:
            start_port: Startport für die Suche
            max_attempts: Maximale Anzahl Versuche

        Returns:
            Freier Port
        """
        import socket

        for i in range(max_attempts):
            port = start_port + i
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(("", port))
                    return port
            except OSError:
                continue

        raise RuntimeError(
            f"Kein freier Port gefunden (versucht: {start_port}-{start_port + max_attempts})"
        )

    def get_heartbeat_url(self) -> Optional[str]:
        """Gibt die aktuelle Heartbeat-URL zurück."""
        if self.server:
            return self.server.get_heartbeat_url()
        return None

    def is_running(self) -> bool:
        """Prüft ob der Heartbeat-Server läuft."""
        return self.server is not None


# Convenience-Funktionen
async def start_agent_heartbeat(
    agent_id: str,
    name: str = "",
    capabilities: list = None,
    port: int = None,
    host: str = "0.0.0.0",
) -> tuple[AgentHeartbeatManager, str]:
    """Startet einen Heartbeat-Server für einen Agent.

    Args:
        agent_id: Agent-ID
        name: Agent-Name
        capabilities: Agent-Capabilities
        port: Port (None für automatische Auswahl)
        host: Host-Adresse

    Returns:
        Tuple aus (HeartbeatManager, Heartbeat-URL)
    """
    manager = AgentHeartbeatManager(agent_id, name, capabilities)
    heartbeat_url = await manager.start_heartbeat_server(port, host)
    return manager, heartbeat_url


async def stop_agent_heartbeat(manager: AgentHeartbeatManager):
    """Stoppt einen Agent-Heartbeat-Server.

    Args:
        manager: Heartbeat-Manager
    """
    await manager.stop_heartbeat_server()
