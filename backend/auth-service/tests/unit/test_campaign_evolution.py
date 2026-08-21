import pytest
from app.services.global_intelligence.threat_campaign_correlation_engine import ThreatCampaignCorrelationEngine

def test_campaign_evolution_tracking():
    engine = ThreatCampaignCorrelationEngine()
    cmp_obj = engine.get_campaign("cmp_darkstorm_2026")
    assert cmp_obj is not None
    assert cmp_obj.evolution_status in ["NEW", "EXPANDING", "STABLE", "DECLINING"]
