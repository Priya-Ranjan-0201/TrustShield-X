import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_autonomous_defense_timeline_logging():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-AUTO", "t1", ["INC-1"], "Commander", "Test")
    evt = engine.add_timeline_event("C-AUTO", "t1", "ACTION", "Autonomous Action ACT-01 Executed", "AutonomousDefenseEngine")
    assert evt["event_type"] == "ACTION"
