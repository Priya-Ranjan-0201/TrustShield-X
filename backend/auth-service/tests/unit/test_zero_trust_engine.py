import pytest
from app.services.zero_trust_exposure.zero_trust_security_engine import ZeroTrustSecurityEngine

def test_unified_access_evaluation_allow():
    engine = ZeroTrustSecurityEngine()
    
    # Register identity and device
    engine.identity_engine.register_identity("USR-1", "tenant-1", "alice", "alice@truthshield.io")
    engine.device_engine.register_device("DEV-1", "tenant-1", "USR-1", "host1", "macOS", "14.5", edr_active=True, disk_encrypted=True, firewall_active=True)
    engine.session_engine.create_session("SESS-1", "tenant-1", "USR-1", "DEV-1", "10.0.0.1")
    
    res = engine.evaluate_unified_access_request(
        tenant_id="tenant-1",
        subject_id="USR-1",
        device_id="DEV-1",
        session_id="SESS-1",
        resource_id="DB-VAULT",
        resource_sensitivity="CONFIDENTIAL",
        action="READ",
        source_ip="10.0.0.1"
    )
    assert res["decision"] == "ALLOW"
    assert res["confidence"] >= 0.95

def test_unified_access_evaluation_untrusted_device():
    engine = ZeroTrustSecurityEngine()
    engine.identity_engine.register_identity("USR-2", "tenant-1", "bob", "bob@truthshield.io")
    engine.session_engine.create_session("SESS-2", "tenant-1", "USR-2", "DEV-UNKNOWN", "10.0.0.2")
    
    res = engine.evaluate_unified_access_request(
        tenant_id="tenant-1",
        subject_id="USR-2",
        device_id="DEV-UNKNOWN",
        session_id="SESS-2",
        resource_id="DB-VAULT",
        resource_sensitivity="RESTRICTED",
        action="WRITE",
        source_ip="10.0.0.2"
    )
    assert res["decision"] == "DENY"
    assert "TRUST" in res["decision_reason"] or "INSUFFICIENT" in res["decision_reason"]

def test_generate_trust_scorecard():
    engine = ZeroTrustSecurityEngine()
    engine.identity_engine.register_identity("USR-3", "tenant-1", "charlie", "charlie@truthshield.io")
    scorecard = engine.generate_trust_scorecard("tenant-1", "USR-3")
    assert scorecard["tenant_id"] == "tenant-1"
    assert scorecard["overall_confidence"] > 0.0
