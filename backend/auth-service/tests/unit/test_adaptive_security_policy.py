import pytest
from app.services.autonomous_defense.adaptive_security_policy_engine import AdaptiveSecurityPolicyEngine

def test_adaptive_policy_safe_proposal():
    engine = AdaptiveSecurityPolicyEngine()
    res = engine.propose_policy_change("pol_safe_01", "Rate Limit Tuning")
    assert res["status"] == "PENDING_APPROVAL"
