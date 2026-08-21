import pytest
from app.services.ai_governance.ai_tool_governance_engine import AIToolGovernanceEngine

def test_connector_security_call():
    engine = AIToolGovernanceEngine()
    res = engine.validate_tool_call("tool_query_telemetry", {"target": "ast_api_gw"})
    assert res["allowed"] is True
