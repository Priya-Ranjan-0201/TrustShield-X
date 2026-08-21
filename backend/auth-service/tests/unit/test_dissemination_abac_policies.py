import pytest
from app.services.threat_intelligence_fusion.intelligence_dissemination_engine import IntelligenceDisseminationEngine

def test_dissemination_abac_policies_and_explicit_deny():
    engine = IntelligenceDisseminationEngine()
    # Explicit DENY: insufficient clearance
    rec_deny = engine.evaluate_dissemination_policy(
        product_type="ACTOR_PROFILE",
        recipient="EXTERNAL_PARTNER",
        classification="HIGHLY_RESTRICTED",
        requester_clearance="CONFIDENTIAL",
        tenant_scope="GLOBAL",
        recipient_tenant="GLOBAL"
    )
    assert rec_deny.policy_verdict == "BLOCKED"
    assert "insufficient" in rec_deny.reason.lower()
    
    # ALLOW: valid clearance
    rec_allow = engine.evaluate_dissemination_policy(
        product_type="IOC_BUNDLE",
        recipient="SOC_TIER_2",
        classification="INTERNAL",
        requester_clearance="SECRET",
        tenant_scope="GLOBAL",
        recipient_tenant="GLOBAL"
    )
    assert rec_allow.policy_verdict == "PERMITTED"
