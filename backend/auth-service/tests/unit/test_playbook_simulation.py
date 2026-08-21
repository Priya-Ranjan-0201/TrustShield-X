import pytest
from app.services.soc.incident_replay_engine import IncidentReplayEngine


def test_playbook_simulation_dryrun():
    replay = IncidentReplayEngine()
    res = replay.replay_incident("inc_hist_01", "pb_phishing_containment")

    assert res["is_safe"] is True
    assert res["simulation_environment"] == "ISOLATED_SANDBOX"
    assert res["estimated_time_saved_minutes"] > 0
