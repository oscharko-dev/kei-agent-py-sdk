# 🏢 Enterprise Setup Examples

Beispiele für Enterprise-grade Deployment und Konfiguration von Keiko Personal Assistant.

## 🔐 Security Configuration

### Multi-Factor Authentication Setup

```python
# config/security.py
from keiko.security import SecurityConfig, MFAConfig, EncryptionConfig

ENTERPRISE_SECURITY_CONFIG = SecurityConfig(
    # Multi-Factor Authentication
    mfa=MFAConfig(
        enabled=True,
        required_methods=["totp", "hardware_token"],
        backup_codes_enabled=True,
        session_timeout_minutes=60,
        remember_device_days=0  # Keine Device-Erinnerung in Enterprise
    ),

    # Encryption
    encryption=EncryptionConfig(
        algorithm="AES-256-GCM",
        key_rotation_days=30,
        data_at_rest_encryption=True,
        data_in_transit_encryption=True
    ),

    # Password Policy
    password_policy={
        "min_length": 12,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_numbers": True,
        "require_special_chars": True,
        "max_age_days": 90,
        "history_count": 12
    },

    # Session Management
    session_config={
        "secure_cookies": True,
        "httponly_cookies": True,
        "samesite": "strict",
        "session_timeout": 3600,
        "concurrent_sessions_limit": 3
    }
)

# Anwendung der Konfiguration
from keiko.core.auth import AuthService

auth_service = AuthService(ENTERPRISE_SECURITY_CONFIG)
```

### Role-Based Access Control (RBAC)

```python
# config/rbac.py
from keiko.security.rbac import Role, Permission, RBACConfig

# Berechtigungen definieren
PERMISSIONS = {
    # System-Berechtigungen
    "system:admin": Permission("system:admin", "Vollzugriff auf System"),
    "system:config": Permission("system:config", "System-Konfiguration"),
    "system:monitoring": Permission("system:monitoring", "System-Monitoring"),

    # Agent-Berechtigungen
    "agents:create": Permission("agents:create", "Agenten erstellen"),
    "agents:read": Permission("agents:read", "Agenten anzeigen"),
    "agents:update": Permission("agents:update", "Agenten bearbeiten"),
    "agents:delete": Permission("agents:delete", "Agenten löschen"),
    "agents:execute": Permission("agents:execute", "Agenten ausführen"),

    # Task-Berechtigungen
    "tasks:create": Permission("tasks:create", "Tasks erstellen"),
    "tasks:read": Permission("tasks:read", "Tasks anzeigen"),
    "tasks:cancel": Permission("tasks:cancel", "Tasks abbrechen"),

    # User-Berechtigungen
    "users:create": Permission("users:create", "Benutzer erstellen"),
    "users:read": Permission("users:read", "Benutzer anzeigen"),
    "users:update": Permission("users:update", "Benutzer bearbeiten"),
    "users:delete": Permission("users:delete", "Benutzer löschen")
}

# Rollen definieren
ROLES = {
    "system_admin": Role(
        name="system_admin",
        description="System-Administrator",
        permissions=[
            PERMISSIONS["system:admin"],
            PERMISSIONS["system:config"],
            PERMISSIONS["system:monitoring"],
            PERMISSIONS["users:create"],
            PERMISSIONS["users:read"],
            PERMISSIONS["users:update"],
            PERMISSIONS["users:delete"]
        ]
    ),

    "agent_operator": Role(
        name="agent_operator",
        description="Agent-Operator",
        permissions=[
            PERMISSIONS["agents:create"],
            PERMISSIONS["agents:read"],
            PERMISSIONS["agents:update"],
            PERMISSIONS["agents:execute"],
            PERMISSIONS["tasks:create"],
            PERMISSIONS["tasks:read"],
            PERMISSIONS["tasks:cancel"]
        ]
    ),

    "business_user": Role(
        name="business_user",
        description="Business-Benutzer",
        permissions=[
            PERMISSIONS["agents:read"],
            PERMISSIONS["agents:execute"],
            PERMISSIONS["tasks:create"],
            PERMISSIONS["tasks:read"]
        ]
    ),

    "viewer": Role(
        name="viewer",
        description="Nur-Lese-Zugriff",
        permissions=[
            PERMISSIONS["agents:read"],
            PERMISSIONS["tasks:read"],
            PERMISSIONS["system:monitoring"]
        ]
    )
}

# RBAC-Konfiguration
RBAC_CONFIG = RBACConfig(
    roles=ROLES,
    permissions=PERMISSIONS,
    default_role="viewer",
    role_inheritance_enabled=True,
    permission_caching_enabled=True,
    cache_ttl_seconds=300
)
```

## 🏗️ High-Availability Setup

### Load Balancer Configuration

```yaml
# nginx/keiko.conf
upstream keiko_backend {
    least_conn;
    server keiko-app-1:8000 max_fails=3 fail_timeout=30s;
    server keiko-app-2:8000 max_fails=3 fail_timeout=30s;
    server keiko-app-3:8000 max_fails=3 fail_timeout=30s;
}

upstream keiko_websocket {
    ip_hash;  # Sticky sessions für WebSocket
    server keiko-app-1:8000;
    server keiko-app-2:8000;
    server keiko-app-3:8000;
}

server {
    listen 443 ssl http2;
    server_name api.keiko.enterprise.com;

    # SSL-Konfiguration
    ssl_certificate /etc/ssl/certs/keiko.crt;
    ssl_certificate_key /etc/ssl/private/keiko.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # API-Routen
    location /api/ {
        proxy_pass http://keiko_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Rate Limiting
        limit_req zone=api burst=20 nodelay;
    }

    # WebSocket-Routen
    location /ws {
        proxy_pass http://keiko_websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket-spezifische Timeouts
        proxy_read_timeout 86400;
    }

    # Health Check
    location /health {
        proxy_pass http://keiko_backend;
        access_log off;
    }
}

# Rate Limiting
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=1r/s;
}
```

### Database Cluster Setup

```yaml
# docker-compose.enterprise.yml
version: '3.8'

services:
  # PostgreSQL Master
  postgres-master:
    image: postgres:15
    environment:
      POSTGRES_DB: keiko
      POSTGRES_USER: keiko_user
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
      POSTGRES_REPLICATION_USER: replicator
      POSTGRES_REPLICATION_PASSWORD_FILE: /run/secrets/replication_password
    volumes:
      - postgres_master_data:/var/lib/postgresql/data
      - ./postgres/master.conf:/etc/postgresql/postgresql.conf
      - ./postgres/pg_hba.conf:/etc/postgresql/pg_hba.conf
    secrets:
      - postgres_password
      - replication_password
    networks:
      - keiko_db_network
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager

  # PostgreSQL Read Replicas
  postgres-replica-1:
    image: postgres:15
    environment:
      PGUSER: postgres
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
      POSTGRES_MASTER_SERVICE: postgres-master
    volumes:
      - postgres_replica1_data:/var/lib/postgresql/data
      - ./postgres/replica.conf:/etc/postgresql/postgresql.conf
    secrets:
      - postgres_password
      - replication_password
    networks:
      - keiko_db_network
    depends_on:
      - postgres-master

  # Redis Cluster
  redis-master:
    image: redis:7-alpine
    command: redis-server --appendonly yes --replica-announce-ip redis-master
    volumes:
      - redis_master_data:/data
    networks:
      - keiko_cache_network

  redis-replica-1:
    image: redis:7-alpine
    command: redis-server --replicaof redis-master 6379
    volumes:
      - redis_replica1_data:/data
    networks:
      - keiko_cache_network
    depends_on:
      - redis-master

  # Keiko Application Instances
  keiko-app-1:
    build: .
    environment:
      DATABASE_URL: postgresql://keiko_user:${POSTGRES_PASSWORD}@postgres-master:5432/keiko
      DATABASE_REPLICA_URLS: postgresql://keiko_user:${POSTGRES_PASSWORD}@postgres-replica-1:5432/keiko
      REDIS_URL: redis://redis-master:6379
      INSTANCE_ID: app-1
    secrets:
      - postgres_password
      - azure_ai_key
      - jwt_secret
    networks:
      - keiko_app_network
      - keiko_db_network
      - keiko_cache_network
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

secrets:
  postgres_password:
    external: true
  replication_password:
    external: true
  azure_ai_key:
    external: true
  jwt_secret:
    external: true

networks:
  keiko_app_network:
    driver: overlay
  keiko_db_network:
    driver: overlay
  keiko_cache_network:
    driver: overlay

volumes:
  postgres_master_data:
  postgres_replica1_data:
  redis_master_data:
  redis_replica1_data:
```

## 📊 Enterprise Monitoring

### Comprehensive Monitoring Stack

```yaml
# monitoring/docker-compose.monitoring.yml
version: '3.8'

services:
  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'

  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD}
      GF_USERS_ALLOW_SIGN_UP: false
      GF_AUTH_ANONYMOUS_ENABLED: false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

  # AlertManager
  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager

  # Jaeger (Distributed Tracing)
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"
    environment:
      COLLECTOR_OTLP_ENABLED: true

  # ELK Stack für Logging
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.8.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.8.0
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_HOSTS: http://elasticsearch:9200
    depends_on:
      - elasticsearch

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:
  elasticsearch_data:
```

### Enterprise Alerting Configuration

```yaml
# alertmanager/alertmanager.yml
global:
  smtp_smarthost: 'smtp.enterprise.com:587'
  smtp_from: 'alerts@keiko.enterprise.com'
  smtp_auth_username: 'alerts@keiko.enterprise.com'
  smtp_auth_password: '${SMTP_PASSWORD}'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'
      group_wait: 0s
      repeat_interval: 5m
    - match:
        severity: warning
      receiver: 'warning-alerts'
      repeat_interval: 30m

receivers:
  - name: 'default'
    email_configs:
      - to: 'ops-team@enterprise.com'
        subject: 'Keiko Alert: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          Severity: {{ .Labels.severity }}
          Instance: {{ .Labels.instance }}
          {{ end }}

  - name: 'critical-alerts'
    email_configs:
      - to: 'critical-alerts@enterprise.com'
        subject: 'CRITICAL: Keiko Alert'
    slack_configs:
      - api_url: '${SLACK_WEBHOOK_URL}'
        channel: '#critical-alerts'
        title: 'Critical Keiko Alert'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'

  - name: 'warning-alerts'
    email_configs:
      - to: 'warnings@enterprise.com'
        subject: 'WARNING: Keiko Alert'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'cluster', 'service']
```

## 🔒 Compliance & Audit

### GDPR Compliance Setup

```python
# compliance/gdpr.py
from keiko.compliance import GDPRCompliance, DataProcessor, ConsentManager

class EnterpriseGDPRCompliance(GDPRCompliance):
    """Enterprise GDPR-Compliance-Implementation."""

    def __init__(self):
        super().__init__()
        self.data_processor = DataProcessor()
        self.consent_manager = ConsentManager()
        self.audit_logger = AuditLogger()

    async def process_data_subject_request(self, request_type: str, user_id: str) -> dict:
        """Verarbeitet Data Subject Requests."""

        await self.audit_logger.log_gdpr_request(request_type, user_id)

        if request_type == "access":
            return await self._handle_data_access_request(user_id)
        elif request_type == "portability":
            return await self._handle_data_portability_request(user_id)
        elif request_type == "erasure":
            return await self._handle_data_erasure_request(user_id)
        elif request_type == "rectification":
            return await self._handle_data_rectification_request(user_id)
        else:
            raise ValueError(f"Unbekannter Request-Typ: {request_type}")

    async def _handle_data_access_request(self, user_id: str) -> dict:
        """Behandelt Data Access Request (Art. 15 GDPR)."""

        # Alle Benutzerdaten sammeln
        user_data = await self.data_processor.collect_user_data(user_id)

        # Daten anonymisieren/pseudonymisieren wo nötig
        processed_data = await self.data_processor.prepare_for_export(user_data)

        # Export-Datei erstellen
        export_file = await self.data_processor.create_export_file(
            user_id, processed_data, format="json"
        )

        return {
            "request_type": "access",
            "user_id": user_id,
            "export_file": export_file,
            "data_categories": list(processed_data.keys()),
            "processing_date": datetime.utcnow().isoformat()
        }

    async def _handle_data_erasure_request(self, user_id: str) -> dict:
        """Behandelt Right to be Forgotten (Art. 17 GDPR)."""

        # Prüfen ob Löschung rechtlich zulässig
        legal_check = await self.data_processor.check_erasure_legality(user_id)

        if not legal_check.allowed:
            return {
                "request_type": "erasure",
                "user_id": user_id,
                "status": "rejected",
                "reason": legal_check.reason
            }

        # Daten löschen
        deletion_result = await self.data_processor.erase_user_data(
            user_id,
            categories=legal_check.erasable_categories
        )

        # Audit-Log erstellen
        await self.audit_logger.log_data_erasure(user_id, deletion_result)

        return {
            "request_type": "erasure",
            "user_id": user_id,
            "status": "completed",
            "deleted_categories": deletion_result.deleted_categories,
            "retained_categories": deletion_result.retained_categories,
            "retention_reasons": deletion_result.retention_reasons
        }

# GDPR-Service konfigurieren
gdpr_service = EnterpriseGDPRCompliance()

# Data Subject Request verarbeiten
@app.post("/api/v1/gdpr/data-subject-request")
async def handle_data_subject_request(
    request: DataSubjectRequest,
    current_user: User = Depends(get_current_user)
):
    """Endpoint für Data Subject Requests."""

    # Berechtigung prüfen (nur eigene Daten oder Admin)
    if request.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Nicht berechtigt")

    result = await gdpr_service.process_data_subject_request(
        request.request_type,
        request.user_id
    )

    return result
```

### SOC 2 Compliance

```python
# compliance/soc2.py
from keiko.compliance import SOC2Compliance, SecurityControl

class EnterpriseSOC2Compliance(SOC2Compliance):
    """SOC 2 Type II Compliance-Implementation."""

    def __init__(self):
        self.security_controls = self._initialize_security_controls()
        self.audit_logger = AuditLogger()
        self.evidence_collector = EvidenceCollector()

    def _initialize_security_controls(self) -> Dict[str, SecurityControl]:
        """Initialisiert SOC 2 Security Controls."""

        return {
            # CC1: Control Environment
            "CC1.1": SecurityControl(
                id="CC1.1",
                description="Management establishes structures, reporting lines, and appropriate authorities",
                implementation=self._check_organizational_structure,
                frequency="quarterly"
            ),

            # CC2: Communication and Information
            "CC2.1": SecurityControl(
                id="CC2.1",
                description="Management communicates information security policies",
                implementation=self._check_security_communication,
                frequency="monthly"
            ),

            # CC6: Logical and Physical Access Controls
            "CC6.1": SecurityControl(
                id="CC6.1",
                description="Logical access security measures",
                implementation=self._check_logical_access_controls,
                frequency="daily"
            ),

            # CC7: System Operations
            "CC7.1": SecurityControl(
                id="CC7.1",
                description="System operations procedures",
                implementation=self._check_system_operations,
                frequency="daily"
            ),

            # CC8: Change Management
            "CC8.1": SecurityControl(
                id="CC8.1",
                description="Change management procedures",
                implementation=self._check_change_management,
                frequency="per_change"
            )
        }

    async def run_compliance_check(self) -> SOC2ComplianceReport:
        """Führt vollständige SOC 2 Compliance-Prüfung durch."""

        report = SOC2ComplianceReport()

        for control_id, control in self.security_controls.items():
            try:
                result = await control.implementation()

                report.add_control_result(control_id, result)

                # Evidence sammeln
                evidence = await self.evidence_collector.collect_evidence(
                    control_id, result
                )
                report.add_evidence(control_id, evidence)

            except Exception as e:
                report.add_control_failure(control_id, str(e))

        # Audit-Log erstellen
        await self.audit_logger.log_compliance_check("SOC2", report)

        return report

    async def _check_logical_access_controls(self) -> ControlResult:
        """Prüft logische Zugangskontrollen (CC6.1)."""

        checks = []

        # Multi-Factor Authentication
        mfa_enabled = await self._check_mfa_enforcement()
        checks.append(("MFA Enforcement", mfa_enabled))

        # Password Policy
        password_policy = await self._check_password_policy_compliance()
        checks.append(("Password Policy", password_policy))

        # Session Management
        session_controls = await self._check_session_controls()
        checks.append(("Session Controls", session_controls))

        # Access Reviews
        access_reviews = await self._check_access_reviews()
        checks.append(("Access Reviews", access_reviews))

        # Privileged Access
        privileged_access = await self._check_privileged_access_controls()
        checks.append(("Privileged Access", privileged_access))

        passed_checks = sum(1 for _, result in checks if result.passed)
        total_checks = len(checks)

        return ControlResult(
            control_id="CC6.1",
            passed=passed_checks == total_checks,
            score=passed_checks / total_checks,
            details=checks,
            evidence_collected=True
        )
```

!!! warning "Enterprise-Sicherheit"
    Diese Beispiele zeigen Enterprise-grade Konfigurationen. Passen Sie sie an Ihre spezifischen Sicherheitsanforderungen und Compliance-Standards an.

!!! info "Skalierung"
    Für große Enterprise-Deployments sollten Sie zusätzlich Container-Orchestrierung (Kubernetes), Service-Mesh (Istio) und erweiterte Monitoring-Lösungen in Betracht ziehen.
