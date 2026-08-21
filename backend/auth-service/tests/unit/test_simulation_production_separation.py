import pytest
from app.services.autonomous_defense.defensive_learning_engine import DefensiveLearningEngine

def test_simulation_cannot_learn_production():
    engine = DefensiveLearningEngine()
    res = engine.evaluate_learning_candidate(
        observation="Simulated Attack",
        evidence=["Digital Twin Sandbox Log"],
        action_taken="SIM_WAF",
        expected_outcome="Simulated 99% containment",
        actual_outcome="Simulated 99% containment",
        is_verified_by_telemetry=True,
        confidence=0.95,
        is_simulation_only=True,
    )
    assert res["status"] == "SIMULATED"
    assert res["can_learn_to_production"] is False
