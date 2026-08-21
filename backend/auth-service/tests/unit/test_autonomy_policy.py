import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_autonomy_policy_level_2_requires_approval():
    engine = AutonomousDefenseEngine()
    engine.set_tenant_autonomy_level("t1", "LEVEL_2")
    act = engine.propose_defensive_action("ACT-POL", "t1", "HOST-01", "QUARANTINE_NON_CRITICAL_ENDPOINT")
    assert act["approval_requirement"] == "HUMAN_APPROVAL_REQUIRED"
