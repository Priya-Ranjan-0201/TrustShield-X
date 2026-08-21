import pytest
from app.services.zero_trust_exposure.session_security_engine import SessionSecurityEngine

def test_session_anomaly_device_drift():
    engine = SessionSecurityEngine()
    engine.create_session("SESS-ANOM-1", "tenant-1", "USR-1", "DEV-KNOWN", "10.0.0.1")
    
    # Device drift mid-session
    res = engine.evaluate_session_activity(
        session_id="SESS-ANOM-1",
        tenant_id="tenant-1",
        current_ip="10.0.0.1",
        current_device="DEV-UNKNOWN"
    )
    assert "DEVICE_CONTEXT_DRIFT" in res["signals"]
    assert res["risk_score"] >= 6.0
