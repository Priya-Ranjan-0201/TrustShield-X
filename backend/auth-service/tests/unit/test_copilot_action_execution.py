import pytest
from app.services.copilot.action_verification_engine import ActionVerificationEngine


def test_copilot_action_execution_outcome():
    verifier = ActionVerificationEngine()
    ver_dto = verifier.verify_action_execution(
        plan_id="act_plan_01",
        is_success=True,
        actual_state="ISOLATED_SECURITY_GROUP_APPLIED",
        expected_state="ISOLATED_SECURITY_GROUP_APPLIED",
    )

    assert ver_dto.action_state == "VERIFIED"
    assert ver_dto.has_divergence is False
    assert ver_dto.rollback_status == "READY"
