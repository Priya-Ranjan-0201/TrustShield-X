import pytest
from app.services.autonomous_defense.adaptive_security_policy_engine import AdaptiveSecurityPolicyEngine

def test_policy_safety_blocks_auth_weakening():
    engine = AdaptiveSecurityPolicyEngine()
    res = engine.propose_policy_change("pol_unsafe_01", "Disable MFA on Ingress", modifies_auth=True)
    assert res["status"] == "BLOCKED"
    assert "SAFETY_VIOLATION" in res["reason"]
