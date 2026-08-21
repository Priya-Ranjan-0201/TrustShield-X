import pytest
from app.services.autonomous_defense.security_experiment_engine import SecurityExperimentEngine

def test_champion_challenger_experiment():
    engine = SecurityExperimentEngine()
    exps = engine.list_experiments()
    assert len(exps) >= 1
    exp = exps[0]
    assert exp.baseline_strategy != exp.candidate_strategy
    assert "fp_reduction" in exp.metrics
