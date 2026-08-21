import pytest
from app.services.assurance_fabric.control_validation_engine import ControlValidationEngine

def test_production_safety():
    engine = ControlValidationEngine()
    res = engine.execute_validation(
        control_id="ctl_1",
        test_name="READ_ONLY_PROD_CHECK",
        expected_result="HEALTHY",
        actual_result="HEALTHY",
        has_evidence=True,
        environment="PRODUCTION_READ_ONLY",
    )
    assert res.environment == "PRODUCTION_READ_ONLY"
    assert res.status == "PASS"
