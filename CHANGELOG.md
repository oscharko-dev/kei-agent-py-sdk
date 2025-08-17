# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Geplant
- Vollständige End-to-End-Tests
- Performance-Optimierungen
- Erweiterte Monitoring-Features

## [0.1.0b1] - 2024-08-17

### Added
- **Multi-Protocol Support**: KEI-RPC, KEI-Stream, KEI-Bus und KEI-MCP
- **Enterprise Security**: Bearer Token, OIDC und mTLS Authentifizierung
- **Production Monitoring**: Structured Logging und Health Checks
- **Input Validation**: Umfassende Sanitization und XSS/SQL-Injection-Schutz
- **Distributed Tracing**: OpenTelemetry-Integration
- **Retry Mechanisms**: Circuit Breaker und exponential backoff
- **Type Safety**: 100% Type Hints für vollständige IntelliSense
- **Deutsche Dokumentation**: Umfassende Guides und API-Referenz

### Security
- Sichere Token-Verwaltung mit automatischer Erneuerung
- Input-Validierung gegen XSS und SQL-Injection
- Audit-Logging für alle kritischen Operationen
- RBAC-Integration für Enterprise-Umgebungen

### Developer Experience
- Async-First Design für maximale Performance
- Auto-Protocol Selection basierend auf Operation-Typ
- Umfassende Error-Handling mit spezifischen Exception-Typen
- CLI-Tools für Development und Debugging

### Infrastructure
- GitHub Actions CI/CD Pipeline
- Multi-OS Testing (Ubuntu, Windows, macOS)
- Python 3.8-3.12 Unterstützung
- Automatische PyPI-Veröffentlichung

### Documentation
- Vollständige API-Referenz
- Praktische Beispiele und Tutorials
- Enterprise-Integration-Guides
- Performance-Tuning-Dokumentation

## [0.0.1] - 2024-07-01

### Added
- Initiale Projektstruktur
- Grundlegende KEI-RPC-Implementierung
- Basis-Authentifizierung
- Erste Tests und Dokumentation

---

## Versioning-Schema

- **Major** (X.y.z): Breaking Changes in der API
- **Minor** (x.Y.z): Neue Features, rückwärtskompatibel
- **Patch** (x.y.Z): Bugfixes, rückwärtskompatibel
- **Pre-Release**: alpha, beta, rc Suffixe für Vorab-Versionen

## Support-Policy

- **Current Release**: Vollständiger Support und Updates
- **Previous Major**: Security-Updates für 12 Monate
- **Legacy Versions**: Community-Support nur

## Migration-Guides

Detaillierte Migration-Guides für Breaking Changes finden Sie in der [Dokumentation](https://docs.kei-framework.com/migration/).
