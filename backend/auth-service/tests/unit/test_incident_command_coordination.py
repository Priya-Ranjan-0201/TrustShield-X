import pytest
from app.services.global_defense.incident_command_bridge import IncidentCommandBridge

def test_incident_command_role_assignment():
    bridge = IncidentCommandBridge()
    roles = bridge.get_command_roles("coord_darkstorm_finance_defense")
    assert roles["incident_commander"] == "usr_ciso_alpha"
    assert roles["technical_lead"] == "usr_secops_lead"
