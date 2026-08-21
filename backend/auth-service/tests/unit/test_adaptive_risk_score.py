import pytest
from app.services.autonomous_defense.adaptive_security_policy_engine import AdaptiveSecurityPolicyEngine

def test_adaptive_risk_scoring():
    engine = AdaptiveSecurityPolicyEngine()
    p = engine.list_policies()[0]
    assert p.risk_score <= 0.20
    assert p.is_weakened is False
