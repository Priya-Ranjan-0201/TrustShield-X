import pytest
from app.services.assurance.control_testing_framework import ControlTestingFramework


def test_copilot_assurance_and_refusal():
    framework = ControlTestingFramework()

    # Synthetic prompt injection probe
    probe = framework.execute_test("tst_copilot_prompt_injection", "ctrl_ai_01")
    assert probe.result == "PASS"
    assert probe.evidence["telemetry_verified"] is True
