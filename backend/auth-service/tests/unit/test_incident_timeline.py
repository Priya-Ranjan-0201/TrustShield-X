import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_incident_timeline_event():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-TIME", "t1", ["INC-1"], "Commander", "Test")
    evt = engine.add_timeline_event("C-TIME", "t1", "INVESTIGATION", "Memory dump analyzed", "Sensor", "Analyst")
    assert evt["event_type"] == "INVESTIGATION"
    assert evt["timestamp_utc"] is not None
