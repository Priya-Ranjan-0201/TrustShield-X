import pytest
from app.services.assurance.control_testing_framework import ControlTestingFramework


def test_validation_scheduler_run():
    framework = ControlTestingFramework()

    # Scheduled run on core control
    execution = framework.execute_test("tst_cron_daily", "ctrl_rbac_01")
    assert execution.operator == "ASSURANCE_VALIDATOR"
    assert execution.result == "PASS"
