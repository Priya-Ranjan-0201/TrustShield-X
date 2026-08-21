import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_crisis_severity_assignment():
    engine = CyberCrisisCommandEngine()
    c = engine.declare_crisis("C-SEV", "t1", ["INC-1"], "Commander", "Test", severity="SEV_2")
    assert c["severity"] == "SEV_2"
