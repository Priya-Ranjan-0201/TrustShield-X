import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_autonomy_level_configuration():
    engine = AutonomousDefenseEngine()
    res = engine.set_tenant_autonomy_level("t1", "LEVEL_1")
    assert res["autonomy_level"] == "LEVEL_1"
    assert res["name"] == "RECOMMEND"
