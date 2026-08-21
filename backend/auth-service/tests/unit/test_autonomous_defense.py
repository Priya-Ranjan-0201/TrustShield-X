import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_propose_autonomous_action():
    engine = AutonomousDefenseEngine()
    engine.set_tenant_autonomy_level("t1", "LEVEL_3")
    act = engine.propose_defensive_action("ACT-01", "t1", "HOST-01", "QUARANTINE_NON_CRITICAL_ENDPOINT")
    assert act["action_id"] == "ACT-01"
    assert act["approval_requirement"] == "AUTONOMOUS_EXECUTION_PERMITTED"
