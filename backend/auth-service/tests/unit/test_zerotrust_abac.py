import pytest
from app.services.zero_trust_exposure.zero_trust_decision_engine import ZeroTrustDecisionEngine

def test_zerotrust_abac_explicit_deny_precedence():
    engine = ZeroTrustDecisionEngine()
    # Explicit untrusted device overrides allow
    dec = engine.evaluate_access(
        tenant_id="t1",
        correlation_id="corr-abac",
        subject_id="sub-1",
        device_id="dev-untrusted",
        session_id="sess-1",
        resource_id="res-1",
        resource_sensitivity="CONFIDENTIAL",
        action="zerotrust.manage",
        identity_trust_state="TRUSTED",
        device_trust_state="UNTRUSTED",
        session_state="ACTIVE"
    )
    assert dec["decision"] == "DENY"
    assert "INSUFFICIENT_DEVICE_POSTURE_ASSURANCE" in dec["decision_reason"] or "DEVICE" in dec["decision_reason"]
