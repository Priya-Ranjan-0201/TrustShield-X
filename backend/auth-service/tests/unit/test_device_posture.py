import pytest
from app.services.zero_trust_exposure.device_trust_engine import DeviceTrustEngine

def test_device_posture_missing_encryption_and_edr():
    engine = DeviceTrustEngine()
    engine.register_device("DEV-P1", "t1", "u1", "laptop1", "Windows", "11")
    
    # Telemetry without encryption and EDR
    res = engine.assess_posture("DEV-P1", "t1", {"disk_encrypted": False, "edr_active": False})
    assert res["posture_score"] <= 5.0
    assert "DISK_NOT_ENCRYPTED" in res["findings"]
    assert "EDR_INACTIVE" in res["findings"]
    assert res["trust_state"] in ["CONDITIONAL", "UNTRUSTED"]
