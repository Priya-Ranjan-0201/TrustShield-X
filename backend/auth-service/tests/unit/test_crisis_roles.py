import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_crisis_role_assignment():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-ROLES", "t1", ["INC-1"], "Commander", "Test")
    role = engine.assign_role("C-ROLES", "t1", "SECURITY_LEAD", "analyst@truthshield.io", "Commander")
    assert role["assignee"] == "analyst@truthshield.io"
    assert role["status"] == "ACTIVE"
