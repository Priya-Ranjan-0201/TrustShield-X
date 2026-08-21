import pytest
from app.services.threat_intelligence.local_threat_relevance_engine import LocalThreatRelevanceEngine


def test_local_threat_relevance_overlap_scoring():
    engine = LocalThreatRelevanceEngine()

    # Overlapping tech stack
    rel = engine.compute_relevance(
        tenant_id="tenant_bank",
        threat_entity_id="camp_shadowstrike",
        targeted_technologies=["NGINX", "POSTGRES"],
        tenant_inventory_techs=["NGINX", "KUBERNETES"],
        exposed_assets=["srv_ingress_01"],
    )

    assert rel.overall_relevance_score > 70.0
    assert "srv_ingress_01" in rel.affected_local_assets
    assert rel.recommended_defensive_action == "APPLY_VIRTUAL_PATCH_AND_SIMULATE_CONTAINMENT"
