import pytest
from app.services.threat_intelligence_fusion.campaign_clustering_engine import CampaignClusteringEngine

def test_campaign_clustering_invariants_no_single_ioc_merge():
    engine = CampaignClusteringEngine()
    # Darkstorm and GhostViper have no multi-factor overlap
    res = engine.evaluate_campaign_merge_eligibility("cmp_darkstorm_apac", "cmp_ghostviper_cloud")
    assert res["allowed"] is False
    assert res["status"] in ("INSUFFICIENT_CORROBORATION", "MERGE_REJECTED_SINGLE_INDICATOR_OVERLAP")
