import pytest
from app.schemas.autonomous_soc_models import ActionVerificationResultDTO


def test_verification_failure_divergence_flag():
    res = ActionVerificationResultDTO(
        action_id="act_fail",
        verification_status="FAILED",
        expected_state="FIREWALL_DROP",
        actual_state="FIREWALL_ALLOW_STILL_ACTIVE",
        divergence_detected=True,
    )

    assert res.verification_status == "FAILED"
    assert res.divergence_detected is True
