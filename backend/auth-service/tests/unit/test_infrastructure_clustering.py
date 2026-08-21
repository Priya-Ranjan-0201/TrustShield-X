import pytest
from app.services.threat_intelligence_fusion.campaign_clustering_engine import CampaignClusteringEngine

def test_infrastructure_clustering_verification():
    engine = CampaignClusteringEngine()
    cmp = engine.get_campaign("cmp_darkstorm_apac")
    assert "198.51.100.42" in cmp.infrastructure
