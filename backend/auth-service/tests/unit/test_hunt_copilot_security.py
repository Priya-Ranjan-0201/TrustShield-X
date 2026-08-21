import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_copilot_hunt_read_only_safety():
    fabric = ThreatHuntingFabric()

    # Copilot queries recommendations
    hyp = fabric.create_hunt_hypothesis("Copilot Read Query", "Read-only hypothesis", "ANOMALOUS_BEHAVIOR")
    assert hyp.hypothesis_id is not None
    # Ensure copilot cannot fabricate or bypass validation
    assert hyp.conclusion is None
