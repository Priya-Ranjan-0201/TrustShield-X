import pytest
from app.services.cyber_digital_twin.incident_replay_purple_team_engine import IncidentReplayPurpleTeamEngine

def test_detection_validation_pipeline():
    engine = IncidentReplayPurpleTeamEngine()
    exercise = engine.execute_purple_team_simulation("PURPLE-DET", "t1", "SIEM Test", ["INITIAL_ACCESS"], ["EDR"])
    assert exercise["metrics"]["soc_alert_generation"] == "VERIFIED_SIMULATED_ALERT"
    assert exercise["soc_integration_verified"] is True
