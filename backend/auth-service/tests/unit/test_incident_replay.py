import pytest
from app.services.cyber_digital_twin.incident_replay_purple_team_engine import IncidentReplayPurpleTeamEngine

def test_historical_incident_replay():
    engine = IncidentReplayPurpleTeamEngine()
    timeline = [{"step": 1, "action": "Phishing"}, {"step": 2, "action": "Lateral Pivot"}]
    replay = engine.replay_incident("REP-01", "t1", "INC-2024-99", timeline, alternative_controls=["MICROSEGMENTATION"])
    assert replay["is_simulation"] is True
    assert replay["outcome_with_alternative_controls"] == "ATTACK_PREVENTED_AT_STEP_2"
    assert replay["historical_loss_avoidance_potential"] > 0
