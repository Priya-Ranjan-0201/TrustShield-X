import pytest
from app.services.fusion.incident_command_engine import IncidentCommandEngine


def test_incident_objectives_lifecycle():
    engine = IncidentCommandEngine()
    cmd = engine.create_incident_command("INC-01", "lead", "HIGH", tenant_id="tenant_obj")

    assert cmd.objectives[0].objective_type == "IDENTIFY"
    assert cmd.objectives[0].status == "IN_PROGRESS"
    assert cmd.objectives[1].objective_type == "CONTAIN"
    assert cmd.objectives[1].status == "PENDING"
