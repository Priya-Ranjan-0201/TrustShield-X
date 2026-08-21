import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.collective_defense_fabric import CollectiveDefenseFabric


def test_copilot_attribution_and_grounding_safety():
    fabric = CollectiveDefenseFabric()
    obj = ThreatIntelligenceObjectDTO(intelligence_type="IP", raw_indicator="198.51.100.77")

    campaign = fabric.campaign_graph.cluster_campaign("Copilot Test Campaign", [obj])

    # Invariant: AI/Copilot must not fabricate attribution if evidence is unconfirmed
    assert campaign.attribution_status == "ATTRIBUTION_UNCONFIRMED"
    assert campaign.attributed_actor is None
