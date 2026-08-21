import pytest
from app.services.cyber_digital_twin.incident_replay_purple_team_engine import IncidentReplayPurpleTeamEngine

def test_soc_simulation_isolation():
    engine = IncidentReplayPurpleTeamEngine()
    exercise = engine.execute_purple_team_simulation("PURPLE-SOC", "t1", "SOC Test", ["ACCESS"], ["EDR"])
    assert exercise["simulation_marker"] == "SIMULATION_MODE_ONLY"
