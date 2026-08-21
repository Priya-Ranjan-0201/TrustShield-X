import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_crisis_workspace_state():
    engine = CyberCrisisCommandEngine()
    c = engine.declare_crisis("C-WORK", "t1", ["INC-1"], "Commander", "Test")
    assert c["is_closed"] is False
    assert len(c["command_structure"]) >= 1
