import pytest
from app.services.zero_trust_exposure.continuous_identity_engine import ContinuousIdentityEngine

def test_continuous_identity_lifecycle():
    engine = ContinuousIdentityEngine()
    
    # Registration
    ident = engine.register_identity(
        identity_id="ID-100",
        tenant_id="tenant-alpha",
        username="alice_secops",
        email="alice@tenant-alpha.com",
        roles=["SECURITY_ANALYST"],
        permissions=["read:alerts", "write:remediation"],
        mfa_enforced=True
    )
    assert ident["identity_id"] == "ID-100"
    assert ident["identity_trust_state"] == "TRUSTED"
    
    # Evaluation with consistent IP
    eval1 = engine.evaluate_identity_confidence(
        identity_id="ID-100",
        tenant_id="tenant-alpha",
        current_ip="192.168.1.50"
    )
    assert eval1["trust_state"] == "TRUSTED"
    assert eval1["risk_score"] == 0.0
    
    # Impossible travel evaluation
    eval2 = engine.evaluate_identity_confidence(
        identity_id="ID-100",
        tenant_id="tenant-alpha",
        current_ip="203.0.113.195",
        auth_context={"impossible_travel": True}
    )
    assert eval2["trust_state"] == "IDENTITY_UNTRUSTED"
    assert eval2["risk_score"] == 9.0
