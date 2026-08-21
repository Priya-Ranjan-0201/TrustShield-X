import pytest
from app.services.enterprise_governance.enterprise_policy_engine import EnterprisePolicyEngine

def test_policy_conflict_explicit_deny_wins():
    engine = EnterprisePolicyEngine()
    res = engine.evaluate_policy_decision("ANALYST", "keys:export", ["ALLOW", "DENY"])
    assert res["decision"] == "DENIED"
    assert res["reason"] == "EXPLICIT_DENY_PRECEDENCE"
