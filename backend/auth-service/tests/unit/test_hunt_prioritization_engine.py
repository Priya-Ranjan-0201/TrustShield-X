import pytest
from app.services.autonomous_defense.threat_hunting_optimization_engine import ThreatHuntingOptimizationEngine

def test_hunt_prioritization_novelty():
    engine = ThreatHuntingOptimizationEngine()
    hunt = engine.create_candidate_hunt("Test hypothesis", ["logs"], novelty_score=0.95)
    assert hunt.priority == "HIGH"
