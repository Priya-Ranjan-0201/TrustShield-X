import pytest
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine

def test_indicator_lifecycle_transitions():
    engine = IndicatorIntelligenceEngine()
    ind = engine.register_indicator("198.51.100.99", "IPv4", confidence=0.95, sources=["s1", "s2"])
    eval_res = engine.evaluate_indicator_quality(ind.indicator_id, days_since_last_seen=0)
    assert eval_res["quality_state"] == "VERIFIED"
    
    # Stale transition
    eval_stale = engine.evaluate_indicator_quality(ind.indicator_id, days_since_last_seen=200)
    assert eval_stale["quality_state"] == "STALE"
    assert eval_stale["status"] == "EXPIRED"
