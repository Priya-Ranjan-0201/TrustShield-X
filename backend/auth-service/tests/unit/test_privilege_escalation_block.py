import pytest
from app.services.autonomous_defense.autonomy_governance_engine import AutonomyGovernanceEngine

def test_privilege_escalation_strictly_denied():
    engine = AutonomyGovernanceEngine()
    res = engine.validate_action_execution("LEVEL_4", "GRANT_ROOT_ACCESS", is_high_impact=True, attempts_privilege_escalation=True)
    assert res["allowed"] is False
    assert res["status"] == "ACTION_BLOCKED"
    assert "UNAUTHORIZED_PRIVILEGE_ESCALATION" in res["reason"]
