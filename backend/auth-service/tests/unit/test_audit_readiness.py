import pytest
from app.services.enterprise_governance.audit_readiness_engine import AuditReadinessEngine

def test_audit_readiness_listing():
    engine = AuditReadinessEngine()
    reqs = engine.list_requests()
    assert len(reqs) >= 1
    assert reqs[0].status == "SUBMITTED"
