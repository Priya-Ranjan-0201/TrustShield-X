import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_7d_crisis_risk():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-RISK", "t1", ["INC-1"], "Commander", "Test")
    sit = engine.generate_situational_awareness("C-RISK", "t1")
    risk = sit["crisis_risk"]
    assert "threat_score" in risk
    assert "confidence_score" in risk
    assert "uncertainty_score" in risk
