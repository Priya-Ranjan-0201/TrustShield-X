import pytest
from app.services.cyber_digital_twin.cyber_digital_twin_engine import CyberDigitalTwinEngine

def test_digital_twin_environment_creation():
    engine = CyberDigitalTwinEngine()
    env = engine.create_environment("ENV-P35-01", "t1", "PRODUCTION_REPLICA")
    assert env["environment_id"] == "ENV-P35-01"
    assert env["environment_type"] == "PRODUCTION_REPLICA"
    assert env["state_hash"] is not None
