import pytest
from app.services.ai_governance.ai_tool_governance_engine import AIToolGovernanceEngine

def test_plugin_security_registered_tools():
    engine = AIToolGovernanceEngine()
    tools = engine.list_tools()
    assert len(tools) >= 2
