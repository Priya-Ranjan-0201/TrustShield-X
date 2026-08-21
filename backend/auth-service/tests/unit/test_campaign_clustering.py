import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.global_campaign_graph_engine import GlobalCampaignGraphEngine


def test_campaign_clustering_across_modalities():
    graph_engine = GlobalCampaignGraphEngine()

    ind1 = ThreatIntelligenceObjectDTO(intelligence_type="DOMAIN", raw_indicator="phishing-portal.com", source_id="SRC_1")
    ind2 = ThreatIntelligenceObjectDTO(intelligence_type="QR_INDICATOR", raw_indicator="qr_code_payload_xyz", source_id="SRC_2")
    ind3 = ThreatIntelligenceObjectDTO(intelligence_type="PAYMENT_IDENTIFIER", raw_indicator="fraud_upi_handle@bank", source_id="SRC_3")

    campaign = graph_engine.cluster_campaign(
        name="Cross-Modal Banking Fraud Wave",
        indicators=[ind1, ind2, ind3],
    )

    assert campaign.campaign_id.startswith("gcmp_")
    assert len(campaign.modalities) >= 3
    assert "QR_PHISHING" in campaign.modalities
    assert "FINANCIAL_FRAUD" in campaign.modalities
    assert len(campaign.indicators) == 3
