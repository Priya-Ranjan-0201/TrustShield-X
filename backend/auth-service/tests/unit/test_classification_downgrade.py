import pytest
from app.services.global_defense.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine

def test_classification_downgrade_rejection():
    engine = IntelligenceSharingPolicyEngine()
    res = engine.evaluate_sharing(
        tenant_id="default_tenant",
        recipient="tenant_finance_alpha",
        classification="HIGHLY_RESTRICTED",
        purpose="THREAT_DEFENSE",
    )
    assert res["allowed"] is False
    assert "exceeds allowed threshold" in res["reason"]
