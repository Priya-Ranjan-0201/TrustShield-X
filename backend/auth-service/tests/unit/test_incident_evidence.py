import pytest
from app.services.mission_control.incident_command_engine import IncidentCommandEngine

def test_incident_evidence_room():
    engine = IncidentCommandEngine()
    cmd = engine.create_incident_command("t1", "inc_ev", "HIGH", 0.8, 0.7, "commander")
    ev = engine.add_evidence(cmd.incident_command_id, "SIEM", "VERIFIED", 0.95, "Malware signature detected", tenant_id="t1")
    assert ev.classification == "VERIFIED"
    room = engine.get_evidence_room(cmd.incident_command_id, "t1")
    assert room.total_verified == 1
