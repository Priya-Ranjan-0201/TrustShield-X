import pytest
from app.services.threat_intelligence_fusion.campaign_clustering_engine import CampaignClusteringEngine

def test_campaign_timeline_tracking():
    engine = CampaignClusteringEngine()
    cmps = engine.list_campaigns(status="ACTIVE")
    assert len(cmps) >= 2
