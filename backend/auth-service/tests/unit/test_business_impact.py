import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_8d_business_impact():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-BIZ", "t1", ["INC-1"], "Commander", "Test")
    sit = engine.generate_situational_awareness("C-BIZ", "t1")
    impact = sit["business_impact"]
    assert "service_availability" in impact
    assert "data_confidentiality" in impact
    assert "financial_impact" in impact
