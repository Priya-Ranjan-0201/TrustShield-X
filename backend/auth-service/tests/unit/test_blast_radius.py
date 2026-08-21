import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_blast_radius_categories():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-BLAST", "t1", ["INC-1"], "Commander", "Test")
    sit = engine.generate_situational_awareness("C-BLAST", "t1")
    blast = sit["blast_radius"]
    assert "confirmed_impact" in blast
    assert "probable_impact" in blast
    assert "simulated_impact" in blast
