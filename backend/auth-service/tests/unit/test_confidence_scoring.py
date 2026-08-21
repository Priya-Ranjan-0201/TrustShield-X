import pytest
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine

def test_indicator_confidence_scoring():
    engine = IndicatorIntelligenceEngine()
    ind = engine.register_indicator("10.0.0.1", "IPv4", confidence=0.40)
    eval_res = engine.evaluate_indicator_quality(ind.indicator_id)
    assert eval_res["quality_state"] == "LOW_CONFIDENCE"
