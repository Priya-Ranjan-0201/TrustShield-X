import pytest
from app.services.autonomous_defense.security_decision_engine import SecurityDecisionEngine

def test_decision_explainability_fields():
    engine = SecurityDecisionEngine()
    exp = engine.explain_decision("dec_waf_containment_01")
    assert "why" in exp
    assert "evidence" in exp
    assert "policy" in exp
    assert "alternatives" in exp
    assert "confidence" in exp
    assert "rollback_plan" in exp
