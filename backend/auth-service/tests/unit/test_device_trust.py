import pytest
from app.services.zero_trust_exposure.device_trust_engine import DeviceTrustEngine

def test_device_posture_and_jailbreak_detection():
    engine = DeviceTrustEngine()
    
    # Register compliant device
    dev = engine.register_device(
        device_id="DEV-200",
        tenant_id="tenant-alpha",
        owner_id="ID-100",
        hostname="corp-mac-01",
        os_name="macOS",
        os_version="14.5",
        edr_active=True,
        disk_encrypted=True,
        firewall_active=True
    )
    assert dev["trust_state"] == "TRUSTED"
    assert dev["posture_score"] == 10.0
    
    # Posture check with jailbreak / root detection
    res = engine.assess_posture(
        device_id="DEV-200",
        tenant_id="tenant-alpha",
        telemetry={"jailbroken": True}
    )
    assert res["trust_state"] == "UNTRUSTED"
    assert res["posture_score"] == 0.0
