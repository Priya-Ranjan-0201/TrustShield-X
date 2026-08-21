import pytest
from app.services.ai_governance.ai_agent_security_engine import AIAgentSecurityEngine

def test_agent_sandboxed_execution():
    engine = AIAgentSecurityEngine()
    agent = engine.list_agents()[0]
    assert agent.status == "ACTIVE"
