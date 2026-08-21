import pytest
from app.services.enterprise_governance.enterprise_policy_engine import EnterprisePolicyEngine

def test_abac_governance_deny_precedence():
    engine = EnterprisePolicyEngine()
    res = engine.evaluate_policy_decision("ANALYST", "keys:export", ["DENY"])
    assert res["decision"] == "DENIED"
