import pytest
from app.services.security_engineering.change_validation_engine import ChangeValidationEngine

def test_change_validation():
    engine = ChangeValidationEngine()
    val = engine.validate_change("imp_test", syntax_valid=True, security_regression_free=True, tenant_isolated=True, authz_verified=True)
    assert val["overall_validation"] == "PASSED"
    assert val["ready_for_rollout"] is True
