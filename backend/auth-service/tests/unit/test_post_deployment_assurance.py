import pytest
from app.services.assurance.control_testing_framework import ControlTestingFramework


def test_post_deployment_assurance_smoke():
    framework = ControlTestingFramework()

    # Verify smoke test after deployment
    execution = framework.execute_test("tst_post_deploy_smoke", "ctrl_waf_01", environment="PRODUCTION_CANARY")
    assert execution.result == "PASS"
    assert execution.environment == "PRODUCTION_CANARY"
