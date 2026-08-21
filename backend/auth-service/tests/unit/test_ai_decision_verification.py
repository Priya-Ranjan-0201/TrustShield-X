import pytest
from app.services.ai_governance.ai_tool_governance_engine import AIToolGovernanceEngine

def test_high_impact_tool_requires_approval():
    engine = AIToolGovernanceEngine()
    res = engine.validate_tool_call("tool_reboot_router", {"router_id": "core_r1"}, has_approval=False)
    assert res["allowed"] is False
    assert res["status"] == "APPROVAL_REQUIRED"
