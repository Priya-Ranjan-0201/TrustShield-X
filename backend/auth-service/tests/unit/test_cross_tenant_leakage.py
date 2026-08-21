import pytest
from app.services.global_defense.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine

def test_unauthorized_cross_tenant_sharing_blocked():
    engine = IntelligenceSharingPolicyEngine()
    res = engine.evaluate_sharing(
        tenant_id="default_tenant",
        recipient="tenant_unauthorized_external",
        classification="CONFIDENTIAL",
        purpose="THREAT_DEFENSE",
    )
    assert res["decision"] == "SHARING_BLOCKED"
    assert res["allowed"] is False
