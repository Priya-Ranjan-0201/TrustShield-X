import pytest
from app.schemas.assurance_models import ControlTestExecutionDTO


def test_control_test_definitions():
    execution = ControlTestExecutionDTO(
        execution_id="exec_01",
        test_id="tst_rbac_deny_precedence",
        control_id="ctrl_rbac_01",
        environment="STAGING",
        expected="Explicit DENY overrides ALLOW grant",
        actual="Policy evaluator enforced DENY",
        result="PASS",
        evidence={"evaluation_tree": "DENY_AUTHORITATIVE"},
        duration_ms=10,
    )

    assert execution.result == "PASS"
    assert execution.environment == "STAGING"
