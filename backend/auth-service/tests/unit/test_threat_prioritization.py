import pytest
from app.services.global_intelligence.global_threat_intelligence_fusion_engine import GlobalThreatIntelligenceFusionEngine

def test_threat_prioritization_aggregation():
    engine = GlobalThreatIntelligenceFusionEngine()
    overview = engine.get_global_intelligence_overview()
    assert overview["intelligence_accuracy_score"] == 0.96
    assert overview["feed_health_status"] == "HEALTHY"
