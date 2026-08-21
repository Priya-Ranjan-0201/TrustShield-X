import pytest
from app.services.mission_control_os.mission_incident_command_engine import MissionIncidentCommandEngine

def test_alert_incident_correlation_link():
    engine = MissionIncidentCommandEngine()
    inc = engine.get_incident("inc_darkstorm_burst")
    assert "ast_api_gw" in inc.affected_assets
