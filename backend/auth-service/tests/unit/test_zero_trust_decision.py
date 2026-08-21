import pytest
from app.services.zero_trust_exposure.zero_trust_decision_engine import ZeroTrustDecisionEngine

def test_8d_decision_rules():
    engine = ZeroTrustDecisionEngine()
    
    # High risk access to restricted resource -> DENY
    dec1 = engine.evaluate_access(
        tenant_id="tenant-alpha",
        correlation_id="CORR-1",
        subject_id="ID-100",
        device_id="DEV-200",
        session_id="SESS-300",
        resource_id="DB-VAULT",
        resource_sensitivity="RESTRICTED",
        action="READ",
        identity_trust_state="IDENTITY_UNTRUSTED",
        device_trust_state="TRUSTED",
        session_state="ACTIVE",
        risk_score=9.0
    )
    assert dec1["decision"] == "DENY"
    
    # Full trust to restricted resource -> ALLOW
    dec2 = engine.evaluate_access(
        tenant_id="tenant-alpha",
        correlation_id="CORR-2",
        subject_id="ID-100",
        device_id="DEV-200",
        session_id="SESS-300",
        resource_id="DB-VAULT",
        resource_sensitivity="RESTRICTED",
        action="READ",
        identity_trust_state="TRUSTED",
        device_trust_state="TRUSTED",
        session_state="ACTIVE",
        risk_score=0.1
    )
    assert dec2["decision"] == "ALLOW"
