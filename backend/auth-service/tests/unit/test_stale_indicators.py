import pytest
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine

def test_stale_indicator_detection():
    engine = IndicatorIntelligenceEngine()
    ind = engine.register_indicator("old-c2.org", "DOMAIN")
    res = engine.evaluate_indicator_quality(ind.indicator_id, days_since_last_seen=190)
    assert res["quality_state"] == "STALE"
