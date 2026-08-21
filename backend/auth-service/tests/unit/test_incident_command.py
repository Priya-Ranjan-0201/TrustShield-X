import pytest
from app.services.mission_control_os.mission_incident_command_engine import MissionIncidentCommandEngine

def test_incident_command_status():
    engine = MissionIncidentCommandEngine()
    inc = engine.get_incident("inc_darkstorm_burst")
    assert inc is not None
    assert inc.severity == "CRITICAL"
    assert inc.containment_status == "CONTAINED"
