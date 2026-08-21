import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_hunt_security_invariants_no_destructive_actions():
    fabric = ThreatHuntingFabric()

    hyp = fabric.create_hunt_hypothesis("Investigate C2 Callback", "Passive hunt", "ASSET_COMPROMISE")
    res = fabric.run_bounded_hunt(hyp.hypothesis_id)

    # Invariant: Recommendations must never include destructive actions by default
    for rec in res.recommendations:
        assert "DELETE" not in rec.upper()
        assert "KILL_PROCESS" not in rec.upper()
        assert "FORMAT" not in rec.upper()
