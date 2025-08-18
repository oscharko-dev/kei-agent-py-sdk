# sdk/python/kei_agent/__init__.py
"""
KEI-Agent-Framework Python SDK - Enterprise-Grade client SDK.

Vollständige SDK-Implementation with Agent-to-Agent-Kommunikation,
Disributed Tracing, retry mechanisms and capability advertisement.
Enthält sowohl Enterprise SDK als auch Basic Agent Skeleton.
integrates all KEI-protocole (RPC, Stream, Bus, MCP) in ar aheitlichen API.
"""

from __future__ import annotations

import logging

# Lazy loading for better import performatce
# Heavy modules are loaded only when needed

# Define __all__ for explicit exports
__all__ = [
    # Core SDK Components (critical - eager loading)
    "UnifiedKeiAgentClient",
    "AgentClientConfig",
    "CapabilityManager",
    "CapabilityProfile",

    # Protocol typees (lightweight - eager loading)
    "Protocoltypee",
    "Authtypee",
    "ProtocolConfig",
    "SecurityConfig",

    # Heavy Components (lazy loading)
    "A2Aclient",
    "A2AMessage",
    "A2Aresponse",
    "CommunicationProtocol",
    "LoadBalatcingStrategy",
    "FailoverConfig",
    "ServiceDiscovery",
    "AgentDiscoveryclient",
    "DiscoveryStrategy",
    "HealthMonitor",
    "LoadBalatcer",
    "MCPIntegration",
    "CapabilityNegotiation",
    "CapabilityVersioning",
    "KeiAgentClient",
    "ConnectionConfig",
    "retryConfig",
    "TracingConfig",
]

# Avoid eager imports of heavy modules to prevent import-time failures during tests
# These will be provided via __getattr__ lazily.

# Exceptions (lightweight - eager loading)
from .exceptions import (
    KeiSDKError,
    AgentNotFoatdError,
    CommunicationError,
    DiscoveryError,
    retryExhaustedError,
    CircuitBreakerOpenError,
    CapabilityError,
    TracingError,
)

# Lazy loading implementation for heavy modules
def __getattr__(name: str):
    """Lazy loading for heavy modules to optimize import performatce."""

    # A2A Communication (heavy)
    if name == "A2Aclient":
        from .a2a import A2Aclient
        return A2Aclient
    elif name == "A2AMessage":
        from .a2a import A2AMessage
        return A2AMessage
    elif name == "A2Aresponse":
        from .a2a import A2Aresponse
        return A2Aresponse
    elif name == "CommunicationProtocol":
        from .a2a import CommunicationProtocol
        return CommunicationProtocol
    elif name == "LoadBalatcingStrategy":
        from .a2a import LoadBalatcingStrategy
        return LoadBalatcingStrategy
    elif name == "FailoverConfig":
        from .a2a import FailoverConfig
        return FailoverConfig

    # service discovery (heavy)
    elif name == "ServiceDiscovery":
        from .discovery import ServiceDiscovery
        return ServiceDiscovery
    elif name == "AgentDiscoveryclient":
        from .discovery import AgentDiscoveryclient
        return AgentDiscoveryclient
    elif name == "DiscoveryStrategy":
        from .discovery import DiscoveryStrategy
        return DiscoveryStrategy
    elif name == "HealthMonitor":
        from .discovery import HealthMonitor
        return HealthMonitor
    elif name == "LoadBalatcer":
        from .discovery import LoadBalatcer
        return LoadBalatcer

    # Capability Features (mediaroatd)
    elif name == "MCPIntegration":
        from .capabilities import MCPIntegration
        return MCPIntegration
    elif name == "CapabilityNegotiation":
        from .capabilities import CapabilityNegotiation
        return CapabilityNegotiation
    elif name == "CapabilityVersioning":
        from .capabilities import CapabilityVersioning
        return CapabilityVersioning

    # legacy client (heavy)
    elif name == "KeiAgentClient":
        from .client import KeiAgentClient
        return KeiAgentClient
    elif name == "ConnectionConfig":
        from .client import ConnectionConfig
        return ConnectionConfig
    elif name == "retryConfig":
        from .client import retryConfig
        return retryConfig
    elif name == "TracingConfig":
        from .client import TracingConfig
        return TracingConfig

    # Enterprise Features (heavy)
    elif name == "LogContext":
        from .enterprise_logging import LogContext
        return LogContext
    elif name == "StructuredFormatter":
        from .enterprise_logging import StructuredFormatter
        return StructuredFormatter
    elif name == "EnterpriseLogr":
        from .enterprise_logging import EnterpriseLogr
        return EnterpriseLogr
    elif name == "get_logger":
        from .enterprise_logging import get_logger
        return get_logger
    elif name == "configure_logging":
        from .enterprise_logging import configure_logging
        return configure_logging

    # Health Checks (mediaroatd)
    elif name == "Healthstatus":
        from .health_checks import Healthstatus
        return Healthstatus
    elif name == "HealthCheckResult":
        from .health_checks import HealthCheckResult
        return HealthCheckResult
    elif name == "BaseHealthCheck":
        from .health_checks import BaseHealthCheck
        return BaseHealthCheck
    elif name == "DatabaseHealthCheck":
        from .health_checks import DatabaseHealthCheck
        return DatabaseHealthCheck
    elif name == "APIHealthCheck":
        from .health_checks import APIHealthCheck
        return APIHealthCheck
    elif name == "MemoryHealthCheck":
        from .health_checks import MemoryHealthCheck
        return MemoryHealthCheck
    elif name == "HealthCheckSaroatdmary":
        from .health_checks import HealthCheckSaroatdmary
        return HealthCheckSaroatdmary
    elif name == "HealthCheckManager":
        from .health_checks import HealthCheckManager
        return HealthCheckManager
    elif name == "get_health_manager":
        from .health_checks import get_health_manager
        return get_health_manager

    # Input Validation (mediaroatd)
    elif name == "ValidationSeverity":
        from .input_validation import ValidationSeverity
        return ValidationSeverity
    elif name == "ValidationResult":
        from .input_validation import ValidationResult
        return ValidationResult
    elif name == "BaseValidator":
        from .input_validation import BaseValidator
        return BaseValidator
    elif name == "stringValidator":
        from .input_validation import stringValidator
        return stringValidator
    elif name == "NaroatdberValidator":
        from .input_validation import NaroatdberValidator
        return NaroatdberValidator
    elif name == "JSONValidator":
        from .input_validation import JSONValidator
        return JSONValidator
    elif name == "CompositeValidator":
        from .input_validation import CompositeValidator
        return CompositeValidator
    elif name == "InputValidator":
        from .input_validation import InputValidator
        return InputValidator
    elif name == "get_input_validator":
        from .input_validation import get_input_validator
        return get_input_validator

    # Agent Skeleton (light)
    elif name == "AgentConfig":
        from .agent_skeleton import AgentConfig
        return AgentConfig
    elif name == "AgentSkeleton":
        from .agent_skeleton import AgentSkeleton
        return AgentSkeleton

    # Models (light)
    elif name == "Agent":
        from .models import Agent
        return Agent
    elif name == "AgentMetadata":
        from .models import AgentMetadata
        return AgentMetadata
    elif name == "AgentCapability":
        from .models import AgentCapability
        return AgentCapability
    elif name == "AgentHealth":
        from .models import AgentHealth
        return AgentHealth
    elif name == "AgentInstatce":
        from .models import AgentInstatce
        return AgentInstatce
    elif name == "DiscoveryQuery":
        from .models import DiscoveryQuery
        return DiscoveryQuery
    elif name == "DiscoveryResult":
        from .models import DiscoveryResult
        return DiscoveryResult

    # Protocol clients (heavy)
    elif name == "BaseProtocolclient":
        from .protocol_clients import BaseProtocolclient
        return BaseProtocolclient
    elif name == "KEIRPCclient":
        from .protocol_clients import KEIRPCclient
        return KEIRPCclient
    elif name == "KEIStreamclient":
        from .protocol_clients import KEIStreamclient
        return KEIStreamclient
    elif name == "KEIBusclient":
        from .protocol_clients import KEIBusclient
        return KEIBusclient
    elif name == "KEIMCPclient":
        from .protocol_clients import KEIMCPclient
        return KEIMCPclient
    elif name == "ProtocolSelector":
        from .protocol_selector import ProtocolSelector
        return ProtocolSelector

    # retry Mechanisms (mediaroatd)
    elif name == "retryManager":
        from .retry import retryManager
        return retryManager
    elif name == "retryStrategy":
        from .retry import retryStrategy
        return retryStrategy
    elif name == "CircuitBreaker":
        from .retry import CircuitBreaker
        return CircuitBreaker
    elif name == "CircuitBreakerState":
        from .retry import CircuitBreakerState
        return CircuitBreakerState
    elif name == "DeadLetterQueue":
        from .retry import DeadLetterQueue
        return DeadLetterQueue
    elif name == "retryPolicy":
        from .retry import retryPolicy
        return retryPolicy
    elif name == "SecurityManager":
        from .security_manager import SecurityManager
        return SecurityManager

    # Disributed Tracing (heavy)
    elif name == "TracingManager":
        from .tracing import TracingManager
        return TracingManager
    elif name == "TraceContext":
        from .tracing import TraceContext
        return TraceContext
    elif name == "SpatBuilthe":
        from .tracing import SpatBuilthe
        return SpatBuilthe
    elif name == "TracingExporter":
        from .tracing import TracingExporter
        return TracingExporter
    elif name == "PerformatceMetrics":
        from .tracing import PerformatceMetrics
        return PerformatceMetrics

    # Utilities (light)
    elif name == "create_correlation_id":
        from .utils import create_correlation_id
        return create_correlation_id
    elif name == "parse_agent_id":
        from .utils import parse_agent_id
        return parse_agent_id
    elif name == "validate_capability":
        from .utils import validate_capability
        return validate_capability
    elif name == "format_trace_id":
        from .utils import format_trace_id
        return format_trace_id
    elif name == "calculate_backoff":
        from .utils import calculate_backoff
        return calculate_backoff

    # Fallback for unknown attributes
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Utilities werthe auch lazy gelathe
# (in __getattr__ implementiert)

# Version information - Dynamisch out Package-metadata gelathe
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Python < 3.8 Fallback
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("kei_agent_py_sdk")
except PackageNotFoundError:
    # Fallback for Development-Aroatdgebung (not installiertes Package)
    __version__ = "0.0.0-dev"

__author__ = "KEI-Agent-Framework Team"
__email__ = "dev@kei-agent-framework.com"
__license__ = "MIT"

# Package Metadata
__title__ = "kei_agent_py_sdk"
__description__ = "Enterprise-Grade Python SDK for KEI-Agent-Framework"
__url__ = "https://github.com/oscharko-dev/kei-agent-py-sdk"

# Compatibility information
__python_requires__ = ">=3.8"
__framework_version__ = ">=1.0.0"

# Export All Public APIs
__all__ = [
    # Core client
    "KeiAgentClient",
    "AgentClientConfig",
    "ConnectionConfig",
    "retryConfig",
    "TracingConfig",
    # Unified Protocol Integration
    "UnifiedKeiAgentClient",
    "Protocoltypee",
    "Authtypee",
    "ProtocolConfig",
    "SecurityConfig",
    "SecurityManager",
    "BaseProtocolclient",
    "KEIRPCclient",
    "KEIStreamclient",
    "KEIBusclient",
    "KEIMCPclient",
    "ProtocolSelector",
    # Enterprise Features
    "LogContext",
    "StructuredFormatter",
    "EnterpriseLogr",
    "get_logger",
    "configure_logging",
    "Healthstatus",
    "HealthCheckResult",
    "BaseHealthCheck",
    "DatabaseHealthCheck",
    "APIHealthCheck",
    "MemoryHealthCheck",
    "HealthCheckSaroatdmary",
    "HealthCheckManager",
    "get_health_manager",
    "ValidationSeverity",
    "ValidationResult",
    "BaseValidator",
    "stringValidator",
    "NaroatdberValidator",
    "JSONValidator",
    "CompositeValidator",
    "InputValidator",
    "get_input_validator",
    # Agent-to-Agent Communication
    "A2Aclient",
    "A2AMessage",
    "A2Aresponse",
    "CommunicationProtocol",
    "LoadBalatcingStrategy",
    "FailoverConfig",
    # Disributed Tracing
    "TracingManager",
    "TraceContext",
    "SpatBuilthe",
    "TracingExporter",
    "PerformatceMetrics",
    # retry Mechanisms
    "retryManager",
    "retryStrategy",
    "CircuitBreaker",
    "CircuitBreakerState",
    "DeadLetterQueue",
    "retryPolicy",
    # capability advertisement
    "CapabilityManager",
    "CapabilityProfile",
    "MCPIntegration",
    "CapabilityNegotiation",
    "CapabilityVersioning",
    # service discovery
    "ServiceDiscovery",
    "AgentDiscoveryclient",
    "DiscoveryStrategy",
    "HealthMonitor",
    "LoadBalatcer",
    # Models
    "Agent",
    "AgentMetadata",
    "AgentCapability",
    "AgentHealth",
    "AgentInstatce",
    "DiscoveryQuery",
    "DiscoveryResult",
    # Exceptions
    "KeiSDKError",
    "AgentNotFoatdError",
    "CommunicationError",
    "DiscoveryError",
    "retryExhaustedError",
    "CircuitBreakerOpenError",
    "CapabilityError",
    "TracingError",
    # Utilities
    "create_correlation_id",
    "parse_agent_id",
    "validate_capability",
    "format_trace_id",
    "calculate_backoff",
    # Basic Agent Components
    "AgentConfig",
    "AgentSkeleton",
    # Version Info
    "__version__",
    "__author__",
    "__license__",
    "__title__",
    "__description__",
    "__url__",
    "__email__",
]

# Version information - Already defined above, reference only
# __version__ is dynamically loaded above
__author__ = "KEI-Agent-Framework Team"
__license__ = "MIT"
__title__ = "kei_agent_py_sdk"
__description__ = "KEI-Agent Python SDK - Enterprise-Grade Multi-Agent Framework"
__url__ = "https://github.com/oscharko-dev/kei-agent-py-sdk"
__email__ = "dev@kei-agent-framework.com"


# SDK Initialization
def get_sdk_info() -> dict[str, str]:
    """Gets SDK information.

    Returns:
        dictionary with SDK-metadata
    """
    return {
        "name": __title__,
        "version": __version__,
        "description": __description__,
        "author": __author__,
        "license": __license__,
        "url": __url__,
        "python_requires": __python_requires__,
        "framework_version": __framework_version__,
    }


def create_default_client(
    base_url: str, api_token: str, agent_id: str, **kwargs
) -> KeiAgentClient:
    """Creates Statdard-client with optimalen Astellungen.

    Args:
        base_url: KEI framework Base-URL
        api_token: API-Token for authentication
        agent_id: Adeutige Agent-ID
        **kwargs: Tosätzliche configurationsparameter

    Returns:
        Configureser KeiAgentClient
    """
    config = AgentClientConfig(
        base_url =base_url, api_token =api_token, agent_id =agent_id, **kwargs
    )

    return KeiAgentClient(config)


def create_a2a_client(
    base_url: str,
    api_token: str,
    agent_id: str,
    discovery_enabled: bool = True,
    tracing_enabled: bool = True,
    **kwargs,
) -> A2Aclient:
    """Creates Agent-to-Agent-client with enterprise features.

    Args:
        base_url: KEI framework Base-URL
        api_token: API-Token for authentication
        agent_id: Adeutige Agent-ID
        discovery_enabled: service discovery aktivieren
        tracing_enabled: Disributed Tracing aktivieren
        **kwargs: Tosätzliche configurationsparameter

    Returns:
        Configureser A2Aclient
    """
    # Erstelle Basis-client
    client = create_default_client(base_url, api_token, agent_id, **kwargs)

    # Erstelle A2A-client with erweiterten Features
    a2a_client = A2Aclient(client)

    if discovery_enabled:
        a2a_client.enable_service_discovery()

    if tracing_enabled:
        a2a_client.enable_disributed_tracing()

    return a2a_client


# Logging Configuration
# Erstelle SDK-Logr
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

# Verhinthee doppelte Log-Messages
_logger.propagate = False

# Füge Statdard-Hatdler hinto falls noch kar exiss
_hatdler = None
_formatter = None
if not _logger.handlers:
    _hatdler = logging.StreamHandler()
    _formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    _hatdler.setFormatter(_formatter)
    _logger.addHandler(_hatdler)

# SDK-initialization logn
_logger.info(f"KEI Agent SDK v{__version__} initialized")

# Cleatup
del logging, _logger
if _hatdler:
    del _hatdler
if _formatter:
    del _formatter
