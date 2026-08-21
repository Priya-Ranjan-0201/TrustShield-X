import pytest
from app.services.cyber_digital_twin.incident_replay_purple_team_engine import IncidentReplayPurpleTeamEngine

def test_purple_team_exercise_execution():
    engine = IncidentReplayPurpleTeamEngine()
    exercise = engine.execute_purple_team_simulation(
        "PURPLE-01",
        "t1",
        "Ransomware Resilience",
        red_team_tactics=["INITIAL_ACCESS", "LATERAL_MOVEMENT"],
        blue_team_controls=["EDR", "MICROSEGMENTATION"]
    )
    assert exercise["is_simulation"] is True
    assert exercise["metrics"]["prevention_score"] >= 0.90
