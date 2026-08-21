import pytest
from app.services.security_engineering.change_validation_engine import ChangeValidationEngine

def test_post_change_validation():
    engine = ChangeValidationEngine()
    res = engine.validate_change("imp_test", security_regression_free=True)
    assert res["security_regression"] == "PASSED"
