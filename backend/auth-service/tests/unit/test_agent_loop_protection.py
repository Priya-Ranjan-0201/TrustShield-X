import pytest
from app.services.ai_governance.ai_agent_security_engine import AIAgentSecurityEngine

def test_agent_circuit_breaker_loop_protection():
    engine = AIAgentSecurityEngine()
    res = engine.validate_agent_execution("agt_soc_investigator", "query_telemetry", iteration_count=15)
    assert res["allowed"] is False
    assert res["status"] == "CIRCUIT_BREAKER_TRIGGERED"
