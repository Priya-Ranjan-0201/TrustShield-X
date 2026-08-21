import pytest
from app.services.assurance_fabric.ai_control_assurance_engine import AIControlAssuranceEngine

def test_ai_assurance():
    engine = AIControlAssuranceEngine()
    res = engine.evaluate_ai_safety("Copilot_v3", test_injection=True, tool_authz_verified=True)
    assert res.status == "PASS"
    assert res.hallucination_score < 0.05
    assert res.provenance_coverage > 0.95
