import pytest
from app.services.threat_intelligence_fusion.campaign_clustering_engine import CampaignClusteringEngine

def test_temporal_correlation_in_campaigns():
    engine = CampaignClusteringEngine()
    cmp = engine.get_campaign("cmp_darkstorm_apac")
    assert cmp is not None
    assert cmp.first_seen is not None
    assert cmp.last_seen is not None
