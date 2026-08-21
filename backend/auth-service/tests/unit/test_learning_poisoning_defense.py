import pytest
from app.services.autonomous_defense.defensive_learning_engine import DefensiveLearningEngine

def test_learning_poisoning_defense():
    engine = DefensiveLearningEngine()
    # False claim of success when actual telemetry failed
    res = engine.evaluate_learning_candidate(
        observation="Fake Attack",
        evidence=["Forged log"],
        action_taken="NO_OP",
        expected_outcome="Success",
        actual_outcome=None,
        is_verified_by_telemetry=False,
        confidence=0.95,
    )
    assert res["status"] == "OUTCOME_NOT_VERIFIED"
    assert res["can_learn_to_production"] is False
