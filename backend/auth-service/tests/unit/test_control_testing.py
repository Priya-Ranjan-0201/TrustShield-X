import pytest
from app.services.enterprise_governance.control_testing_engine import ControlTestingEngine

def test_control_testing_execution():
    engine = ControlTestingEngine()
    res = engine.test_control_effectiveness("ctrl_iam_mfa_enforcement")
    assert res["test_result"] == "PASSED"
    assert res["effectiveness"] == "EFFECTIVE"
