import pytest
from app.services.assurance.control_testing_framework import ControlTestingFramework


def test_soar_playbook_assurance():
    framework = ControlTestingFramework()
    execution = framework.execute_test("tst_soar_execution_approval", "ctrl_rbac_01")

    assert execution.result == "PASS"
    assert execution.evidence["telemetry_verified"] is True
