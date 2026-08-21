import pytest
from app.services.mission_control.incident_command_engine import IncidentCommandEngine

def test_evidence_conflicts():
    engine = IncidentCommandEngine()
    cmd = engine.create_incident_command("t1", "inc_cf", "HIGH", 0.7, 0.6, "commander")
    ev_a = engine.add_evidence(cmd.incident_command_id, "SRC_A", "VERIFIED", 0.9, "Source A says compromised", tenant_id="t1")
    ev_b = engine.add_evidence(cmd.incident_command_id, "SRC_B", "VERIFIED", 0.85, "Source B says clean", tenant_id="t1")
    conflict = engine.register_evidence_conflict(cmd.incident_command_id, ev_a.evidence_item_id, ev_b.evidence_item_id, "Conflicting compromise assessment", 0.9, 0.85, "t1")
    assert conflict.resolution_status == "OPEN"
    room = engine.get_evidence_room(cmd.incident_command_id, "t1")
    assert len(room.conflicts) == 1
