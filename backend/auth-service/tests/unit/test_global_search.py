import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.collective_defense_fabric import CollectiveDefenseFabric


def test_global_search_tenant_isolation():
    fabric = CollectiveDefenseFabric()

    obj_shared = ThreatIntelligenceObjectDTO(
        intelligence_type="DOMAIN",
        raw_indicator="shared-threat-phish-domain.com",
        classification="SHARED_THREAT_INTELLIGENCE",
        sharing_state="SHARED",
    )
    obj_internal_a = ThreatIntelligenceObjectDTO(
        tenant_id="tenant_a",
        intelligence_type="DOMAIN",
        raw_indicator="internal-tenant-a-threat.com",
        classification="INTERNAL",
    )

    fabric.normalization.ingest_or_merge(obj_shared, source_id="FED")
    fabric.normalization.ingest_or_merge(obj_internal_a, source_id="TENANT_A")

    # Tenant B should find shared, but NOT Tenant A internal
    results_b = fabric.search_intelligence("threat", tenant_id="tenant_b")
    assert any("shared-threat-phish-domain" in r.canonical_identifier for r in results_b)
    assert not any("internal-tenant-a" in r.canonical_identifier for r in results_b)

    # Tenant A should see their own internal
    results_a = fabric.search_intelligence("threat", tenant_id="tenant_a")
    assert any("internal-tenant-a" in r.canonical_identifier for r in results_a)
