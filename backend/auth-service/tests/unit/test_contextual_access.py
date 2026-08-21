import pytest
from app.services.zero_trust_exposure.zero_trust_decision_engine import ZeroTrustDecisionEngine

def test_contextual_access_risk_escalation():
    engine = ZeroTrustDecisionEngine()
    # High risk score triggers step-up or deny
    dec = engine.evaluate_access(
        tenant_id="t1",
        correlation_id="corr-1",
        subject_id="sub-1",
        device_id="dev-1",
        session_id="sess-1",
        resource_id="res-1",
        resource_sensitivity="INTERNAL",
        action="READ",
        identity_trust_state="TRUSTED",
        device_trust_state="TRUSTED",
        session_state="ACTIVE",
        risk_score=5.5
    )
    assert dec["decision"] == "STEP_UP"
    assert dec["required_action"] == "MFA_PROMPT"

def test_contextual_access_critical_risk():
    engine = ZeroTrustDecisionEngine()
    dec = engine.evaluate_access(
        tenant_id="t1",
        correlation_id="corr-2",
        subject_id="sub-1",
        device_id="dev-1",
        session_id="sess-1",
        resource_id="res-1",
        resource_sensitivity="INTERNAL",
        action="READ",
        identity_trust_state="TRUSTED",
        device_trust_state="TRUSTED",
        session_state="ACTIVE",
        risk_score=9.0
    )
    assert dec["decision"] == "DENY"
    assert dec["decision_reason"] == "EXCESSIVE_RISK_SCORE"
