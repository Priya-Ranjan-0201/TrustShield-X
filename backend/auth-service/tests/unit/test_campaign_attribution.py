import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.global_campaign_graph_engine import GlobalCampaignGraphEngine


def test_attribution_safety_default_unconfirmed():
    graph_engine = GlobalCampaignGraphEngine()

    ind = [ThreatIntelligenceObjectDTO(intelligence_type="DOMAIN", raw_indicator="actor-infra.com")]
    campaign = graph_engine.cluster_campaign("Unnamed Campaign", ind)

    assert campaign.attribution_status == "ATTRIBUTION_UNCONFIRMED"
    assert campaign.attributed_actor is None


def test_attribution_requires_multi_evidence():
    graph_engine = GlobalCampaignGraphEngine()

    ind = [ThreatIntelligenceObjectDTO(intelligence_type="DOMAIN", raw_indicator="apt-infra.net")]
    # Insufficient evidence
    c1 = graph_engine.cluster_campaign("APT Wave", ind, attributed_actor="APT-X", actor_evidence=["Single IP overlap"])
    assert c1.attribution_status == "ATTRIBUTION_UNCONFIRMED"

    # Multi-source corroborated evidence
    c2 = graph_engine.cluster_campaign(
        "APT Wave Corroborated",
        ind,
        attributed_actor="APT-X",
        actor_evidence=["Signed malware certificate match", "Unique C2 protocol beaconing signature"],
    )
    assert c2.attribution_status == "PLAUSIBLE"
    assert c2.attributed_actor == "APT-X"
