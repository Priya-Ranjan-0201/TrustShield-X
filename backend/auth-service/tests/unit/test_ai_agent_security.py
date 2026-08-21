import pytest
from app.services.ai_governance.ai_agent_security_engine import AIAgentSecurityEngine

def test_ai_agent_security_configuration():
    engine = AIAgentSecurityEngine()
    agents = engine.list_agents()
    assert len(agents) >= 1
    assert agents[0].autonomy_level == "LEVEL_2"
