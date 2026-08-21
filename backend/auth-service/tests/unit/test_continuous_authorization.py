import pytest
from app.services.zero_trust_exposure.session_security_engine import SessionSecurityEngine

def test_continuous_authorization_ip_change_trigger():
    engine = SessionSecurityEngine()
    engine.create_session("SESS-CONT-1", "tenant-1", "USR-1", "DEV-1", "192.168.1.10")
    
    # Material context change: IP changes mid-session
    res = engine.evaluate_session_activity(
        session_id="SESS-CONT-1",
        tenant_id="tenant-1",
        current_ip="203.0.113.55",
        current_device="DEV-1"
    )
    assert res["session_state"] == "SUSPENDED"
    assert res["step_up_required"] is True
    assert "IP_ADDRESS_HIJACK_DETECTED" in res["signals"]
