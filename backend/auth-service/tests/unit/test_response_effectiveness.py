import pytest
from app.services.response_effectiveness_engine import ResponseEffectivenessEngine
from app.schemas.autonomous_defense_models import (
    ResponsePlanDTO,
    ResponsePlanActionDTO,
    VerificationResultDTO,
)


def test_calculate_effectiveness_score():
    engine = ResponseEffectivenessEngine()

    action = ResponsePlanActionDTO(action_type="BLOCK_DOMAIN", target="test.com")
    plan = ResponsePlanDTO(
        title="Test Plan",
        description="Test",
        risk_score=90.0,
        confidence=0.95,
        actions=[action],
    )

    ver = VerificationResultDTO(
        action_id=action.action_id,
        target="test.com",
        verified_state="CONTAINED",
        verification_passed=True,
    )

    score_dto = engine.calculate_effectiveness(
        plan=plan,
        verifications=[ver],
        initial_risk=90.0,
        residual_risk=10.0,
        time_to_containment_seconds=4.5,
    )

    assert score_dto.effectiveness_score >= 90.0
    assert score_dto.containment_success_rate == 1.0
    assert "HIGHLY_EFFECTIVE" in score_dto.summary
