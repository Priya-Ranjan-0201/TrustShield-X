import pytest
from app.services.assurance.control_testing_framework import ControlTestingFramework


def test_false_pass_prevention():
    framework = ControlTestingFramework()

    # Upstream dependency is unavailable
    blocked_exec = framework.execute_test("tst_db_dependent", "ctrl_audit_01", dependency_healthy=False)

    # Invariant: Unhealthy dependency must NEVER produce a PASS
    assert blocked_exec.result == "BLOCKED"
    assert "DEPENDENCY_UNAVAILABLE" in str(blocked_exec.evidence)
