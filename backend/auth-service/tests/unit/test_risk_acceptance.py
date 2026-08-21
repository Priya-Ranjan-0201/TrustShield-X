import pytest
from app.services.enterprise_governance.enterprise_risk_engine import EnterpriseRiskEngine

def test_risk_acceptance_requires_executive_and_expiry():
    engine = EnterpriseRiskEngine()
    
    # Non-CISO cannot accept
    r1 = engine.evaluate_risk_acceptance("rsk_unauthorized_admin_access", authorized_by="JUNIOR_DEV", rationale="Too busy", expiration_date="2026-09-01T00:00:00Z")
    assert r1["allowed"] is False
    assert r1["status"] == "REJECTED"
    
    # Permanent acceptance forbidden
    r2 = engine.evaluate_risk_acceptance("rsk_unauthorized_admin_access", authorized_by="CISO", rationale="Valid business need", expiration_date=None)
    assert r2["allowed"] is False
    assert r2["status"] == "REJECTED"
    
    # Valid CISO time-bound acceptance
    r3 = engine.evaluate_risk_acceptance("rsk_unauthorized_admin_access", authorized_by="CISO", rationale="Valid temporary bridge", expiration_date="2026-09-01T00:00:00Z")
    assert r3["allowed"] is True
    assert r3["status"] == "RISK_ACCEPTED"
