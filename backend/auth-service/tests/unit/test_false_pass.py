import pytest
from app.services.assurance_fabric.control_validation_engine import ControlValidationEngine

def test_false_pass():
    engine = ControlValidationEngine()
    with pytest.raises(ValueError, match="Cannot certify PASS without associated execution evidence"):
        engine.execute_validation("ctl_1", "TEST_FALSE_PASS", "OK", "OK", has_evidence=False)
