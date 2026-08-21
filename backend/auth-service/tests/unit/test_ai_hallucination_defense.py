import pytest
from app.services.autonomous_defense.defensive_learning_engine import DefensiveLearningEngine

def test_ai_hallucination_unsupported_learning():
    engine = DefensiveLearningEngine()
    # Attempting to learn with confidence below threshold
    res = engine.evaluate_learning_candidate(
        observation="Hallucinated Pattern",
        evidence=[],
        action_taken="NONE",
        expected_outcome="Unknown",
        actual_outcome="Unknown",
        is_verified_by_telemetry=True,
        confidence=0.55,
    )
    assert res["status"] == "LEARNING_NOT_SUPPORTED"
