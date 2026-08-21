import pytest
from app.services.autonomous_defense.threat_hunting_optimization_engine import ThreatHuntingOptimizationEngine

def test_threat_hunting_optimization_candidates():
    engine = ThreatHuntingOptimizationEngine()
    hunts = engine.list_candidate_hunts()
    assert len(hunts) >= 1
    assert hunts[0].status == "CANDIDATE"
