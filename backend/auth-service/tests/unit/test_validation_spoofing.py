import pytest
from app.services.assurance_fabric.control_validation_engine import ControlValidationEngine

def test_validation_spoofing():
    engine = ControlValidationEngine()
    with pytest.raises(ValueError):
        engine.execute_validation("ctl_fake", "SPOOF_TEST", "PASS", "PASS", has_evidence=False)
