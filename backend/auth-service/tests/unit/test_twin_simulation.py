import pytest
from app.services.soc.incident_replay_engine import IncidentReplayEngine


def test_twin_simulation_impact_estimation():
    replay = IncidentReplayEngine()
    sim = replay.replay_incident("inc_sim_01", "pb_phishing_containment")

    assert sim["simulation_environment"] == "ISOLATED_SANDBOX"
    assert sim["is_safe"] is True
