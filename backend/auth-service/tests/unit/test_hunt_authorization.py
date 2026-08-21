import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_hunt_cancellation_authorization():
    fabric = ThreatHuntingFabric()

    hyp = fabric.create_hunt_hypothesis("Cancellable Hunt", "Desc", "THIRD_PARTY_RISK")
    assert hyp.status == "ACTIVE"

    canceled = fabric.cancel_hunt(hyp.hypothesis_id, reason="Operator confirmed benign maintenance window.")
    assert canceled.status == "CLOSED"
    assert canceled.conclusion == "INSUFFICIENT_EVIDENCE"
