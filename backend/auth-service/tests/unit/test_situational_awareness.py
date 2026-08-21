import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_situational_awareness_generation():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-SIT", "t1", ["INC-1"], "Commander", "Test")
    sit = engine.generate_situational_awareness("C-SIT", "t1")
    assert "business_impact" in sit
    assert "crisis_risk" in sit
    assert "blast_radius" in sit
