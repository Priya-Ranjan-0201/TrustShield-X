import pytest
from app.services.mission_control.incident_command_engine import IncidentCommandEngine

def test_incident_declaration_levels():
    engine = IncidentCommandEngine()
    cmd = engine.create_incident_command("t1", "inc_d1", "MEDIUM", 0.5, 0.5, "commander")
    assert cmd.declaration_level == "OBSERVATION"
    cmd = engine.declare_incident_level(cmd.incident_command_id, "INCIDENT", "Confirmed threat", ["ev_01"], 0.85, "analyst_01", "t1")
    assert cmd.declaration_level == "INCIDENT"
    assert cmd.confidence == 0.85
    assert cmd.declared_at is not None
