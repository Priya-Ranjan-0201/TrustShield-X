import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_crisis_engine_declaration():
    engine = CyberCrisisCommandEngine()
    c = engine.declare_crisis("C-01", "t1", ["INC-1"], "Commander", "Critical breach")
    assert c["crisis_id"] == "C-01"
    assert c["lifecycle_state"] == "CRISIS_DECLARED"
