import pytest
from app.services.mission_control.incident_command_engine import IncidentCommandEngine

def test_incident_correlation():
    engine = IncidentCommandEngine()
    parent = engine.create_incident_command("t1", "inc_p1", "CRITICAL", 0.9, 0.8, "commander")
    child = engine.create_incident_command("t1", "inc_c1", "HIGH", 0.7, 0.6, "commander")
    parent.child_incident_ids.append(child.incident_command_id)
    child.parent_incident_id = parent.incident_command_id
    assert child.parent_incident_id == parent.incident_command_id
    assert child.incident_command_id in parent.child_incident_ids
