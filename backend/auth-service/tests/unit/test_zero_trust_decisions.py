import pytest
from app.services.zero_trust_exposure.zero_trust_decision_engine import ZeroTrustDecisionEngine

def test_zero_trust_compromised_entity_quarantine():
    engine = ZeroTrustDecisionEngine()
    dec = engine.evaluate_access(
        tenant_id="t1",
        correlation_id="corr-comp",
        subject_id="sub-1",
        device_id="dev-1",
        session_id="sess-1",
        resource_id="res-1",
        resource_sensitivity="INTERNAL",
        action="READ",
        identity_trust_state="COMPROMISED",
        device_trust_state="TRUSTED",
        session_state="ACTIVE"
    )
    assert dec["decision"] == "QUARANTINE"
    assert dec["required_action"] == "ISOLATE_AND_RESET_CREDENTIALS"
