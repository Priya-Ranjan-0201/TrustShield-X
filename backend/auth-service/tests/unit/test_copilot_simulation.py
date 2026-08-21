import pytest
from app.services.copilot.security_copilot_service import SecurityCopilot


def test_copilot_simulation_dryrun():
    copilot = SecurityCopilot()
    res = copilot.classifier.classify_request("Simulate isolating srv_checkout_production")

    assert res == "SIMULATION"
