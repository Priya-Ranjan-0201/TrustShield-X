import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_protected_target_blocks_autonomous_action():
    engine = AutonomousDefenseEngine()
    engine.set_tenant_autonomy_level("t1", "LEVEL_4")
    act = engine.propose_defensive_action("ACT-PROT", "t1", "DB-MAIN-CORE-VAULT", "FLUSH_DNS_CACHE")
    assert act["is_protected_target"] is True
    assert act["approval_requirement"] == "FOUR_EYES_DUAL_APPROVAL_REQUIRED"
