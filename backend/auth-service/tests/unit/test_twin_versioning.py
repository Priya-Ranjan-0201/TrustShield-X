import pytest
from app.services.digital_twin_lab.digital_twin_state_engine import DigitalTwinStateEngine

def test_twin_versioning_and_snapshot_retention():
    engine = DigitalTwinStateEngine()
    new_snapshot = engine.create_snapshot(version="v1.1.0-STAGING-DRILL")
    assert new_snapshot.version == "v1.1.0-STAGING-DRILL"
    states = engine.list_states()
    assert len(states) >= 2
