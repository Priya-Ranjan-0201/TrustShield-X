import pytest
from app.services.threat_intelligence.local_threat_relevance_engine import LocalThreatRelevanceEngine


def test_intelligence_impact_on_local_assets():
    engine = LocalThreatRelevanceEngine()
    rel = engine.compute_relevance(
        tenant_id="tenant_ecommerce",
        threat_entity_id="tio_c2_active",
        targeted_technologies=["REACT", "POSTGRES"],
        tenant_inventory_techs=["REACT", "POSTGRES"],
        exposed_assets=["srv_checkout_node_1", "srv_checkout_node_2"],
    )

    assert len(rel.affected_local_assets) == 2
    assert rel.overall_relevance_score > 75.0
