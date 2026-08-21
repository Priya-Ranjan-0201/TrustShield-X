import pytest
from app.services.threat_intelligence_fusion.threat_intelligence_fusion_engine import ThreatIntelligenceFusionEngine

def test_threat_intelligence_fusion_e2e_closed_loop():
    engine = ThreatIntelligenceFusionEngine()
    overview = engine.get_overview()
    assert overview["phase"] == 33
    assert overview["sources_count"] >= 3
    assert overview["active_campaigns_count"] >= 2
    assert overview["early_warnings_count"] >= 1
    assert overview["forecasts_count"] >= 2
    assert overview["feed_health"] == "OPTIMAL"
