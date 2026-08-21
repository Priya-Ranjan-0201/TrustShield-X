import pytest
from app.services.ai_governance.ai_agent_security_engine import AIAgentSecurityEngine

def test_tool_not_in_allowlist_blocked():
    engine = AIAgentSecurityEngine()
    res = engine.validate_agent_execution("agt_soc_investigator", "reboot_core_router")
    assert res["allowed"] is False
    assert res["status"] == "TOOL_NOT_AUTHORIZED"
