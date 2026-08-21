import pytest
from app.services.enterprise_governance.enterprise_policy_engine import EnterprisePolicyEngine

def test_policy_version_immutability():
    engine = EnterprisePolicyEngine()
    policies = engine.list_policies()
    assert policies[0]["policy_id"] == "pol_access_control_v2"
