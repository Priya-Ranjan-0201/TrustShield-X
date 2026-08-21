import pytest
from app.services.assurance_fabric.control_validation_engine import ControlValidationEngine

def test_assurance_abac():
    engine = ControlValidationEngine()
    res = engine.execute_validation("ctl_tenant_isolation", "ABAC_TEST", "ALLOW", "ALLOW", has_evidence=True)
    assert res.status == "PASS"
