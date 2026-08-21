import pytest
from app.services.zero_trust_exposure.zero_trust_security_engine import ZeroTrustSecurityEngine

def test_master_coordinator_unified_flow():
    engine = ZeroTrustSecurityEngine()
    
    # Register identity and device
    engine.identity_engine.register_identity(
        identity_id="USER-SEC-1",
        tenant_id="tenant-alpha",
        username="secops_admin",
        email="secops@truthshield.io",
        roles=["SECURITY_ADMIN"],
        permissions=["read:*", "write:*"],
        mfa_enforced=True
    )
    
    engine.device_engine.register_device(
        device_id="DEV-SEC-1",
        tenant_id="tenant-alpha",
        owner_id="USER-SEC-1",
        hostname="admin-secure-box",
        os_name="Linux",
        os_version="Debian 12"
    )
    
    engine.session_engine.create_session(
        session_id="SESS-SEC-1",
        tenant_id="tenant-alpha",
        subject_id="USER-SEC-1",
        device_id="DEV-SEC-1",
        source_ip="10.0.1.5"
    )
    
    # Evaluate Access
    eval_res = engine.evaluate_unified_access_request(
        tenant_id="tenant-alpha",
        subject_id="USER-SEC-1",
        device_id="DEV-SEC-1",
        session_id="SESS-SEC-1",
        resource_id="VAULT-KEYSTORE",
        resource_sensitivity="RESTRICTED",
        action="DECRYPT",
        source_ip="10.0.1.5",
        device_telemetry={"edr_active": True, "disk_encrypted": True, "jailbroken": False}
    )
    assert eval_res["decision"] == "ALLOW"
    assert eval_res["identity_trust_state"] == "TRUSTED"
    assert eval_res["device_trust_state"] == "TRUSTED"
