import pytest
from app.services.security_engineering.change_validation_engine import ChangeValidationEngine

def test_detection_regression():
    engine = ChangeValidationEngine()
    regr_free = engine.validate_change("imp_1", security_regression_free=True)
    assert regr_free["security_regression"] == "PASSED"
    regr_fail = engine.validate_change("imp_2", security_regression_free=False)
    assert regr_fail["security_regression"] == "REGRESSION_DETECTED"
    assert regr_fail["ready_for_rollout"] is False
