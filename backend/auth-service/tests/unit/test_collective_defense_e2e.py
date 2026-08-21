import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.collective_defense_fabric import CollectiveDefenseFabric


def test_collective_defense_e2e_pipeline():
    fabric = CollectiveDefenseFabric()

    # 1. Register tenant consent
    fabric.policy.register_tenant_consent("tenant_omega", ["SHARED_THREAT_INTELLIGENCE", "INTERNAL"])

    # 2. Local tenant observes an IOC
    local_ioc = ThreatIntelligenceObjectDTO(
        tenant_id="tenant_omega",
        intelligence_type="DOMAIN",
        raw_indicator="malicious-credential-harvest.com",
        classification="INTERNAL",
        confidence=0.88,
    )

    # 3. Process and share with collective defense network
    shared = fabric.process_and_share_local_intelligence(local_ioc, tenant_industry="FINANCIAL_SERVICES")
    assert shared is not None
    assert shared.sharing_state == "SHARED"
    assert shared.tenant_id == "ANONYMIZED_FEDERATION_SOURCE"
    assert "COHORT_FINANCIAL_SERVICES" in shared.anonymized_tenant_cohort

    # 4. Cluster into global campaign
    campaign = fabric.campaign_graph.cluster_campaign("Operation Harvest Alpha", [shared])
    assert campaign.confidence >= 0.60
    assert campaign.attribution_status == "ATTRIBUTION_UNCONFIRMED"

    # 5. Evaluate early warning
    warning = fabric.early_warning.evaluate_campaign_for_warning(campaign)

    # 6. Tenant Beta localizes the threat
    relevance = fabric.localization.compute_tenant_relevance(
        tenant_id="tenant_beta",
        tenant_industry="FINANCIAL_SERVICES",
        local_assets=["unrelated-asset.com"],
        obj=shared,
    )
    assert relevance.is_applicable is True
    assert len(relevance.recommended_hunts) >= 1

    # 7. Summary metrics check
    summary = fabric.get_summary()
    assert summary.total_intelligence_objects >= 1
    assert summary.total_shared_objects >= 1
    assert summary.total_global_campaigns >= 1
