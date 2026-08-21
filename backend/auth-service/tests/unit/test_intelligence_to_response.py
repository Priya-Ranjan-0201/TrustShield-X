import pytest
from app.services.threat_intelligence.local_threat_relevance_engine import LocalThreatRelevanceEngine


def test_intelligence_to_response_action_recommendation():
    engine = LocalThreatRelevanceEngine()
    rel = engine.compute_relevance(
        tenant_id="tenant_fin",
        threat_entity_id="camp_high_risk",
        targeted_technologies=["APACHE_LOG4J"],
        tenant_inventory_techs=["APACHE_LOG4J"],
        exposed_assets=["srv_ingress"],
    )

    assert rel.recommended_defensive_action == "APPLY_VIRTUAL_PATCH_AND_SIMULATE_CONTAINMENT"
