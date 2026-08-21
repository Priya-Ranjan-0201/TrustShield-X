import pytest
from app.services.autonomous_defense.autonomy_governance_engine import AutonomyGovernanceEngine

def test_autonomy_level_4_requires_approval():
    engine = AutonomyGovernanceEngine()
    res = engine.validate_action_execution("LEVEL_4", "ISOLATE_ROUTER", is_high_impact=True, has_approval=False)
    assert res["allowed"] is False
    assert res["status"] == "APPROVAL_REQUIRED"
