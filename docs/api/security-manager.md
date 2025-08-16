# Security Manager

*Diese API-Dokumentation wird noch entwickelt.*

## Übersicht

Der SecurityManager verwaltet Authentifizierung, Autorisierung und Sicherheitsrichtlinien.

## Klasse: SecurityManager

```python
class SecurityManager:
    def __init__(self, config: SecurityConfig):
        """Initialisiert den Security Manager."""
        
    async def authenticate(self) -> bool:
        """Führt Authentifizierung durch."""
        
    async def refresh_token(self) -> str:
        """Erneuert das Authentifizierungs-Token."""
        
    def validate_permissions(self, operation: str) -> bool:
        """Validiert Berechtigungen für eine Operation."""
```

## Authentifizierungstypen

- **Bearer Token**: Einfache Token-basierte Authentifizierung
- **OIDC**: OpenID Connect Integration
- **mTLS**: Mutual TLS für höchste Sicherheit

## Weitere Informationen

- [Protocol Types](protocol-types.md)
- [Unified Client](unified-client.md)
