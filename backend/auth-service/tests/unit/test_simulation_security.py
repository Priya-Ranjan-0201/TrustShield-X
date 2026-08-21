import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_simulation_security_protected_targets():
    engine = AutonomousDefenseEngine()
    act = engine.propose_defensive_action("ACT-SEC", "t1", "PRODUCTION_ROOT_IAM", "DISABLE_MFA")
    assert act["approval_requirement"] == "FOUR_EYES_DUAL_APPROVAL_REQUIRED"
