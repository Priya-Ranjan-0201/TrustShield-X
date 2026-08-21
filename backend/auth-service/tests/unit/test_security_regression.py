import pytest
from app.services.assurance_fabric.security_regression_engine import SecurityRegressionEngine

def test_security_regression():
    engine = SecurityRegressionEngine()
    run = engine.run_regression_suite(
        trigger_event="PR_MERGE_AUTH",
        changed_components=["app_auth_service"],
        affected_controls=["ctl_tenant_isolation", "ctl_four_eyes_response"],
        baseline_states={"ctl_tenant_isolation": "PASS", "ctl_four_eyes_response": "PASS"},
        current_test_results={"ctl_tenant_isolation": "PASS", "ctl_four_eyes_response": "PASS"},
    )
    assert run.passed_count == 2
    assert run.failed_count == 0
    assert len(run.regressions_detected) == 0
