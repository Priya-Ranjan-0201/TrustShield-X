import pytest
from app.services.cyber_digital_twin.incident_replay_purple_team_engine import IncidentReplayPurpleTeamEngine

def test_soar_simulation_dispatch():
    engine = IncidentReplayPurpleTeamEngine()
    exercise = engine.execute_purple_team_simulation("PURPLE-SOAR", "t1", "SOAR Test", ["ACCESS"], ["EDR"])
    assert exercise["metrics"]["soar_playbook_triggered"] == "SIMULATED_QUARANTINE_PLAYBOOK"
