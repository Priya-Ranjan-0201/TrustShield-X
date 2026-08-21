import pytest
from app.services.autonomous_defense.security_decision_engine import SecurityDecisionEngine

def test_autonomous_decision_observability_trace():
    engine = SecurityDecisionEngine()
    dec = engine.get_decision("dec_waf_containment_01")
    assert dec.decision_time is not None
    assert dec.actor_type == "AUTONOMOUS_ENGINE"
    assert len(dec.evidence) >= 1
