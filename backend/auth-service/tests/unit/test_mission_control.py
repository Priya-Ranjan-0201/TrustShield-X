import pytest
from app.services.cyber_digital_twin.cyber_digital_twin_engine import CyberDigitalTwinEngine

def test_mission_control_overview():
    engine = CyberDigitalTwinEngine()
    env = engine.create_environment("ENV-MC", "t1")
    assert env["asset_count"] >= 0
