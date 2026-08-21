import pytest
from app.services.autonomous_defense.autonomy_governance_engine import AutonomyGovernanceEngine

def test_automation_escalation_blocked():
    engine = AutonomyGovernanceEngine()
    res = engine.validate_action_execution("LEVEL_2", "DROP_DATABASE_TABLE", is_high_impact=True, has_approval=False)
    assert res["allowed"] is False
