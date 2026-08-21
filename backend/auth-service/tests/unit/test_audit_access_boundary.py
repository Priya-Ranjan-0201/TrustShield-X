import pytest
from app.services.enterprise_governance.audit_readiness_engine import AuditReadinessEngine

def test_audit_access_boundary_redaction():
    engine = AuditReadinessEngine()
    raw = {"policy": "enforce_mfa", "database_password": "super_secret_pwd", "jwt_private_key": "raw_rsa_pem"}
    sanitized = engine.sanitize_audit_evidence_export(raw)
    assert sanitized["database_password"] == "[REDACTED_BY_AUDIT_BOUNDARY_FILTER]"
    assert sanitized["jwt_private_key"] == "[REDACTED_BY_AUDIT_BOUNDARY_FILTER]"
    assert sanitized["policy"] == "enforce_mfa"
