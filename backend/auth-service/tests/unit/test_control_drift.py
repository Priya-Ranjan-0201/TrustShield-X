import pytest
from app.services.enterprise_governance.control_drift_engine import ControlDriftEngine

def test_control_drift_detection():
    engine = ControlDriftEngine()
    exp = {"mfa_required": True, "session_timeout_mins": 15}
    act = {"mfa_required": False, "session_timeout_mins": 15}
    res = engine.detect_control_drift("ctrl_iam_mfa_enforcement", exp, act)
    assert res["has_drift"] is True
    assert res["status"] == "CONTROL_DRIFT"
