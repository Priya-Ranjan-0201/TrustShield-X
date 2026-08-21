import pytest
from app.services.enterprise_governance.enterprise_policy_engine import EnterprisePolicyEngine

def test_policy_governance_listing():
    engine = EnterprisePolicyEngine()
    policies = engine.list_policies()
    assert len(policies) >= 1
    assert policies[0]["version"] == "2.1.0"
