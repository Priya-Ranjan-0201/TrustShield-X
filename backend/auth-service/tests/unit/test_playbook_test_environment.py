import pytest
from app.services.soc.incident_replay_engine import IncidentReplayEngine


def test_playbook_test_environment_mock_providers():
    replay = IncidentReplayEngine()
    res = replay.replay_incident("inc_test_01", "pb_phishing_containment")

    assert res["is_safe"] is True
    assert "NONE" in res["simulated_side_effects"]
