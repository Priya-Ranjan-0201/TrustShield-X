import pytest
from app.services.zero_trust_exposure.zero_trust_decision_engine import ZeroTrustDecisionEngine

def test_zerotrust_rbac_authorization():
    engine = ZeroTrustDecisionEngine()
    # Read action allowed for trusted subject
    dec = engine.evaluate_access(
        tenant_id="t1",
        correlation_id="corr-rbac",
        subject_id="sub-1",
        device_id="dev-1",
        session_id="sess-1",
        resource_id="res-1",
        resource_sensitivity="INTERNAL",
        action="zerotrust.read",
        identity_trust_state="TRUSTED",
        device_trust_state="TRUSTED",
        session_state="ACTIVE"
    )
    assert dec["decision"] == "ALLOW"
