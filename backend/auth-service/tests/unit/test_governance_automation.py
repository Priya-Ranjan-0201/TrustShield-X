import pytest
from app.services.enterprise_governance.control_testing_engine import ControlTestingEngine

def test_governance_automated_testing():
    engine = ControlTestingEngine()
    res = engine.test_control_effectiveness("ctrl_iam_mfa_enforcement")
    assert res["is_verified"] is True
