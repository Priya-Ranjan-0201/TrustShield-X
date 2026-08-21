import pytest
from app.services.enterprise_governance.continuous_assurance_engine import ContinuousAssuranceEngine

def test_compliance_drift_tracking():
    engine = ContinuousAssuranceEngine()
    engine.trigger_change_based_reassessment("ctrl_iam_mfa_enforcement", "EVENT", False)
    drifts = engine.list_drift_events()
    assert len(drifts) >= 1
    assert drifts[0].current_state == "DEGRADED"
