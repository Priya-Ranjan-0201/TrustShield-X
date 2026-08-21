import pytest
from app.services.global_defense.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine

def test_sharing_policy_approval():
    engine = IntelligenceSharingPolicyEngine()
    res = engine.evaluate_sharing(
        tenant_id="default_tenant",
        recipient="tenant_finance_alpha",
        classification="CONFIDENTIAL",
        purpose="THREAT_DEFENSE",
    )
    assert res["decision"] == "APPROVED"
    assert res["allowed"] is True
    assert res["requires_four_eyes"] is True
