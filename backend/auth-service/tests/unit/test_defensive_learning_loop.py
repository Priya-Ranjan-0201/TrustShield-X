import pytest
from app.services.autonomous_defense.defensive_learning_engine import DefensiveLearningEngine

def test_defensive_learning_loop_verified():
    engine = DefensiveLearningEngine()
    res = engine.evaluate_learning_candidate(
        observation="DarkStorm C2 DNS Tunneling Anomaly",
        evidence=["Sigma entropy hit", "Netflow logs"],
        action_taken="WAF_RATE_LIMIT",
        expected_outcome="Contain C2 lateral spread",
        actual_outcome="C2 lateral spread reduced by 95%",
        is_verified_by_telemetry=True,
        confidence=0.95,
    )
    assert res["status"] == "LEARNED"
    assert res["can_learn_to_production"] is True
