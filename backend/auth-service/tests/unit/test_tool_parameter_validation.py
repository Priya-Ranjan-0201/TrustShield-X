import pytest
from app.services.ai_governance.ai_tool_governance_engine import AIToolGovernanceEngine

def test_tool_parameter_sql_injection_blocked():
    engine = AIToolGovernanceEngine()
    res = engine.validate_tool_call("tool_query_telemetry", {"target": "ast_api_gw; DROP TABLE users;--"})
    assert res["allowed"] is False
    assert res["status"] == "TOOL_ACTION_BLOCKED"
