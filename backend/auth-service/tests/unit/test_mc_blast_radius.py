import pytest
from app.services.mission_control.security_mission_control import SecurityMissionControl

def test_blast_radius():
    mc = SecurityMissionControl()
    cmd = mc.incident_command.create_incident_command("t1", "inc_br", "CRITICAL", 0.9, 0.8, "commander")
    mc.incident_command.add_evidence(cmd.incident_command_id, "EDR", "VERIFIED", 0.95, "Compromise confirmed", {"host": "srv-01"}, "t1")
    blast = mc.calculate_blast_radius(cmd.incident_command_id, "t1")
    assert blast["total_confirmed"] >= 0
    assert "confirmed_affected" in blast
