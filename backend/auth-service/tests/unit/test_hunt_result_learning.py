import pytest
from app.services.autonomous_defense.defensive_learning_engine import DefensiveLearningEngine

def test_hunt_result_learning():
    engine = DefensiveLearningEngine()
    res = engine.evaluate_learning_candidate(
        observation="Proactive hunt discovered orphaned cron job",
        evidence=["Auditd execution log"],
        action_taken="CONTAIN_CRON",
        expected_outcome="Prevent persistence",
        actual_outcome="Cron removed, 0 side effects",
        is_verified_by_telemetry=True,
        confidence=0.90,
    )
    assert res["status"] == "LEARNED"
