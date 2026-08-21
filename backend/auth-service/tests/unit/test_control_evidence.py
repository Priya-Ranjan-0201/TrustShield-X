import pytest
from app.services.assurance.control_testing_framework import ControlTestingFramework


def test_control_evidence_generation():
    framework = ControlTestingFramework()
    execution = framework.execute_test("tst_audit_immutability", "ctrl_audit_01")

    assert execution.evidence is not None
    assert "telemetry_verified" in execution.evidence
    assert execution.evidence["assertions_checked"] >= 1
