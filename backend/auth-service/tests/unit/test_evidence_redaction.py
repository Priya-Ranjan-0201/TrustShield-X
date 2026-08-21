import pytest
from app.services.enterprise_governance.audit_readiness_engine import AuditReadinessEngine

def test_evidence_redaction_token_shield():
    engine = AuditReadinessEngine()
    res = engine.sanitize_audit_evidence_export({"api_token": "secret_abc_123"})
    assert res["api_token"] == "[REDACTED_BY_AUDIT_BOUNDARY_FILTER]"
