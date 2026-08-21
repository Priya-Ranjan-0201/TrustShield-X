import pytest
from app.services.zero_trust_exposure.session_security_engine import SessionSecurityEngine

def test_session_lifecycle_and_invalidation():
    engine = SessionSecurityEngine()
    
    # Create session
    sess = engine.create_session(
        session_id="SESS-300",
        tenant_id="tenant-alpha",
        subject_id="ID-100",
        device_id="DEV-200",
        source_ip="192.168.1.50"
    )
    assert sess["state"] == "ACTIVE"
    
    # Evaluate activity with sudden IP switch
    eval1 = engine.evaluate_session_activity(
        session_id="SESS-300",
        tenant_id="tenant-alpha",
        current_ip="10.0.0.99",
        current_device="DEV-200"
    )
    assert eval1["state"] == "SUSPENDED"
    assert eval1["risk_score"] == 8.5
    
    # Revoke
    rev = engine.revoke_session("SESS-300", "tenant-alpha", reason="Security policy trigger")
    assert rev["state"] == "REVOKED"
