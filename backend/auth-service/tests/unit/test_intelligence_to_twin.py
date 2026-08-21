import pytest
from app.services.threat_intelligence.local_threat_relevance_engine import LocalThreatRelevanceEngine


def test_intelligence_to_twin_simulation_readiness():
    engine = LocalThreatRelevanceEngine()
    rel = engine.compute_relevance(
        tenant_id="tenant_sim",
        threat_entity_id="camp_1",
        targeted_technologies=["NGINX"],
        tenant_inventory_techs=["NGINX"],
        exposed_assets=["srv_checkout"],
    )

    assert "srv_checkout" in rel.affected_local_assets
    assert rel.exposure_relevance_score > 50.0
