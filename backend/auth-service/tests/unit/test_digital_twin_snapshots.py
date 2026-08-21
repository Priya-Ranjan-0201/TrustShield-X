import pytest
from app.services.cyber_digital_twin.cyber_digital_twin_engine import CyberDigitalTwinEngine

def test_digital_twin_snapshot_creation():
    engine = CyberDigitalTwinEngine()
    engine.create_environment("ENV-SNAP", "t1")
    snap = engine.create_snapshot("SNAP-P35-01", "ENV-SNAP", "t1")
    assert snap["snapshot_id"] == "SNAP-P35-01"
    assert snap["is_immutable"] is True
    assert snap["state_hash"] is not None
