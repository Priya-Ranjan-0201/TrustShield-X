import pytest
from app.services.ai_governance.ai_agent_security_engine import AIAgentSecurityEngine

def test_agent_tool_authorization():
    engine = AIAgentSecurityEngine()
    res = engine.validate_agent_execution("agt_soc_investigator", "query_telemetry")
    assert res["allowed"] is True
    assert res["status"] == "AGENT_ACTION_AUTHORIZED"
