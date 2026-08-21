import pytest
from app.services.assurance_fabric.control_validation_engine import ControlValidationEngine

def test_control_validation_execution():
    engine = ControlValidationEngine()
    res = engine.execute_validation(
        control_id="ctl_tenant_isolation",
        test_name="CROSS_TENANT_QUERY_TEST",
        expected_result="ACCESS_DENIED",
        actual_result="ACCESS_DENIED",
        has_evidence=True,
    )
    assert res.status == "PASS"
    assert res.evidence_hash.startswith("sha256_")
