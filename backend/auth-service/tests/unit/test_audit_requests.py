import pytest
from app.services.enterprise_governance.audit_readiness_engine import AuditReadinessEngine

def test_audit_request_due_date():
    engine = AuditReadinessEngine()
    req = engine.list_requests()[0]
    assert req.due_date is not None
