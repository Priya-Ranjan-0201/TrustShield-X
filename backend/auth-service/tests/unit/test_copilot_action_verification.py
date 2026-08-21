import pytest
from app.services.copilot.action_verification_engine import ActionVerificationEngine


def test_copilot_action_divergence_detection():
    verifier = ActionVerificationEngine()
    ver_dto = verifier.verify_action_execution(
        plan_id="act_plan_diverge",
        is_success=False,
        actual_state="PARTIAL_FIREWALL_UPDATE_FAILED",
        expected_state="FIREWALL_DROP_ENFORCED",
    )

    assert ver_dto.action_state == "FAILED"
    assert ver_dto.has_divergence is True
    assert ver_dto.rollback_status == "INITIATED"
