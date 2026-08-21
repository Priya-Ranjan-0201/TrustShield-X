import pytest
from app.services.autonomous_defense.security_experiment_engine import SecurityExperimentEngine

def test_security_experiment_lifecycle():
    engine = SecurityExperimentEngine()
    exp = engine.run_experiment(
        hypothesis="Candidate WAF regex decreases latency",
        baseline_strategy="Regex v1",
        candidate_strategy="Regex v2",
        rollback_procedure="Revert to Regex v1",
    )
    assert exp.status == "RUNNING"
    assert exp.rollback_procedure == "Revert to Regex v1"
