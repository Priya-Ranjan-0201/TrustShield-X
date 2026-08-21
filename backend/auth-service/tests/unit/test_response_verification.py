import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_response_verification_timeline():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-VERIF", "t1", ["INC-1"], "Commander", "Test")
    evt = engine.add_timeline_event("C-VERIF", "t1", "VERIFICATION", "Telemetry probe confirmed isolation", "Sensor")
    assert evt["event_type"] == "VERIFICATION"
