import pytest
from app.schemas.adaptive_defense_models import DefenseChangeRecordDTO, DefenseSimulationResultDTO
from app.services.adaptive_defense.defense_verification_engine import DefenseVerificationEngine


def test_post_adaptation_verification_success_and_divergence():
    engine = DefenseVerificationEngine()
    change = DefenseChangeRecordDTO(action_type="ISOLATE", target="ep-01", reason="Containment")

    # Successful verification
    sim = DefenseSimulationResultDTO(
        action_id="chg_01",
        simulated_after_state={"active_threat_exposure": 0.15},
    )
    outcome_ok = engine.verify_change(change, {"status": "ACTIVE", "is_mitigated": True, "actual_threat_exposure": 0.15}, sim)
    assert outcome_ok == "VERIFIED"

    # Divergence detection (actual exposure 0.70 vs expected 0.15)
    outcome_div = engine.verify_change(change, {"status": "ACTIVE", "is_mitigated": True, "actual_threat_exposure": 0.70}, sim)
    assert outcome_div == "SIMULATION_PRODUCTION_DIVERGENCE"
