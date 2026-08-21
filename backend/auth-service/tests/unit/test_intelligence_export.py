import pytest
from app.services.federation.federated_intelligence_service import FederatedIntelligenceService
from app.services.federation.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine


def test_intelligence_export_policy_clearance():
    service = FederatedIntelligenceService()
    policy_engine = IntelligenceSharingPolicyEngine()

    service.submit_intelligence(
        intelligence_type="DOMAIN",
        canonical_identifier="exportable-phish.net",
        tenant_scope="tenant_exp",
        sharing_scope="COMMUNITY",
    )

    items = service.list_intelligence(requesting_tenant_id="tenant_exp", scope="COMMUNITY")
    assert len(items) >= 1

    decision = policy_engine.evaluate_sharing({"items_count": len(items)}, requested_scope="COMMUNITY")
    assert decision.decision in ("SHARE", "SHARE_REDACTED")
