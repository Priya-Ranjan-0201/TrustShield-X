import pytest
from app.services.global_intelligence.threat_campaign_correlation_engine import ThreatCampaignCorrelationEngine

def test_campaign_clustering_and_correlation():
    engine = ThreatCampaignCorrelationEngine()
    cmp_obj = engine.correlate_campaign(
        name="Storm-2026 Infiltration",
        indicators=["198.51.100.44", "evil.net"],
        techniques=["T1078", "T1055"],
    )
    assert cmp_obj.name == "Storm-2026 Infiltration"
    assert cmp_obj.evolution_status == "EXPANDING"
    assert cmp_obj.confidence_score >= 0.90
