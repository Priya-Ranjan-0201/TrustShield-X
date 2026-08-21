import pytest
from app.services.assurance_fabric.ai_control_assurance_engine import AIControlAssuranceEngine

def test_ai_tool_security():
    engine = AIControlAssuranceEngine()
    failed_tool = engine.evaluate_ai_safety("Copilot_v3", tool_authz_verified=False)
    assert failed_tool.status == "FAIL"
