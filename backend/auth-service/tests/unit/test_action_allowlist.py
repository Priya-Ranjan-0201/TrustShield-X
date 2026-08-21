import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_non_allowlisted_action_requires_approval():
    engine = AutonomousDefenseEngine()
    engine.set_tenant_autonomy_level("t1", "LEVEL_4")
    # Action not in allowlist
    act = engine.propose_defensive_action("ACT-CUSTOM", "t1", "HOST-01", "WIPE_ENTIRE_SERVER_DISK", category="DESTRUCTIVE")
    assert act["approval_requirement"] == "FOUR_EYES_DUAL_APPROVAL_REQUIRED"
