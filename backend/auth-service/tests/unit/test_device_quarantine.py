import pytest
from app.services.zero_trust_exposure.device_trust_engine import DeviceTrustEngine

def test_device_quarantine_action():
    engine = DeviceTrustEngine()
    engine.register_device("DEV-Q1", "t1", "u1", "host-q", "macOS", "14.0")
    
    res = engine.quarantine_device("DEV-Q1", "t1", "MALWARE_SIGNATURE_DETECTED")
    assert res["trust_state"] == "QUARANTINED"
    assert res["quarantine_reason"] == "MALWARE_SIGNATURE_DETECTED"
