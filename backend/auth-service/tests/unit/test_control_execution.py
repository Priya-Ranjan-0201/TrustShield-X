import pytest
from app.services.assurance.control_testing_framework import ControlTestingFramework


def test_control_execution_pass_and_fail():
    framework = ControlTestingFramework()

    # Successful test execution
    pass_exec = framework.execute_test("tst_waf_01", "ctrl_waf_01")
    assert pass_exec.result == "PASS"
    assert pass_exec.duration_ms > 0

    # Simulated failing test execution
    fail_exec = framework.execute_test("tst_waf_01", "ctrl_waf_01", force_failure=True)
    assert fail_exec.result == "FAIL"
    assert "ASSERTION_FAILED" in str(fail_exec.evidence)
