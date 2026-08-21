import pytest
from app.services.enterprise_governance.enterprise_policy_engine import EnterprisePolicyEngine

def test_rbac_governance_eval():
    engine = EnterprisePolicyEngine()
    res = engine.evaluate_policy_decision("ADMIN", "telemetry:read", ["ALLOW"])
    assert res["decision"] == "ALLOWED"
