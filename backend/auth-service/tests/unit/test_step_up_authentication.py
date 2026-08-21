import pytest
from app.services.zero_trust_exposure.zero_trust_decision_engine import ZeroTrustDecisionEngine

def test_step_up_on_restricted_resource():
    engine = ZeroTrustDecisionEngine()
    dec = engine.evaluate_access(
        tenant_id="t1",
        correlation_id="corr-stepup",
        subject_id="sub-1",
        device_id="dev-1",
        session_id="sess-1",
        resource_id="VAULT-KEYSTORE",
        resource_sensitivity="RESTRICTED",
        action="EXPORT_KEY",
        identity_trust_state="TRUSTED",
        device_trust_state="TRUSTED",
        session_state="ACTIVE",
        risk_score=3.5
    )
    assert dec["decision"] == "STEP_UP"
    assert dec["required_action"] == "FIDO2_PASSKEY_STEP_UP"
