import pytest
from app.services.federation.federated_intelligence_service import FederatedIntelligenceService
from app.services.federation.cross_tenant_intelligence_safety import CrossTenantIntelligenceSafety


def test_cross_tenant_sanitization_zero_leakage():
    service = FederatedIntelligenceService()
    safety = CrossTenantIntelligenceSafety()

    # Tenant A registers threat with internal metadata
    obj = service.submit_intelligence(
        intelligence_type="DOMAIN",
        canonical_identifier="phish-victim-portal.com",
        tenant_scope="tenant_victim_a",
        sharing_scope="GLOBAL",
        provenance={
            "origin_tenant": "tenant_victim_a",
            "private_customer_id": "cust_12345",
            "internal_ip_address": "10.14.22.8",
            "detector": "INTERNAL_SOC",
        },
    )

    # Tenant B accesses global threat
    sanitized = safety.sanitize_for_consumer(obj, consumer_tenant_id="tenant_consumer_b")

    # Invariant: Tenant B must NEVER receive Tenant A's private identifiers
    assert "private_customer_id" not in sanitized["provenance"]
    assert "internal_ip_address" not in sanitized["provenance"]
    assert sanitized["tenant_scope"] == "COMMUNITY_ANONYMIZED"
    assert sanitized["provenance"]["contributing_scope"] == "FEDERATED_COMMUNITY_PARTICIPANT"
    assert sanitized["provenance"]["detector"] == "INTERNAL_SOC"
