import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_timeline_chronological_ordering():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-ORDER", "t1", ["INC-1"], "Commander", "Test")
    engine.add_timeline_event("C-ORDER", "t1", "STEP_1", "First event", "Sensor")
    engine.add_timeline_event("C-ORDER", "t1", "STEP_2", "Second event", "Sensor")
    timeline = engine.get_timeline("C-ORDER", "t1")
    assert len(timeline) >= 3  # Initial + 2 added
    assert timeline[1]["timestamp_epoch"] <= timeline[2]["timestamp_epoch"]
