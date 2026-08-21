import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.global_campaign_graph_engine import GlobalCampaignGraphEngine


def test_multi_modal_campaign_expansion():
    graph_engine = GlobalCampaignGraphEngine()

    ind = [
        ThreatIntelligenceObjectDTO(intelligence_type="VOICE_SIGNATURE", raw_indicator="sig_v1"),
        ThreatIntelligenceObjectDTO(intelligence_type="QR_INDICATOR", raw_indicator="qr_code_v1"),
        ThreatIntelligenceObjectDTO(intelligence_type="APK_SIGNATURE", raw_indicator="apk_sig_v1"),
        ThreatIntelligenceObjectDTO(intelligence_type="DOMAIN", raw_indicator="infra-node-1.com"),
        ThreatIntelligenceObjectDTO(intelligence_type="IP", raw_indicator="198.51.100.44"),
    ]

    campaign = graph_engine.cluster_campaign("Multi Modal Surge", ind)
    assert campaign.expansion_warning is True
    assert len(campaign.modalities) >= 4
