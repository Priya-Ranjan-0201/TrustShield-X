import pytest
from app.services.threat_intelligence_fusion.predictive_threat_intelligence_engine import PredictiveThreatIntelligenceEngine

def test_forecast_calibration_brier_score():
    engine = PredictiveThreatIntelligenceEngine()
    fc = engine.get_forecast("fc_darkstorm_surge_7d")
    assert fc is not None
    
    # Event verified empirically
    res = engine.record_forecast_outcome(fc.forecast_id, actual_occurred=True, verification_evidence=["ev_real_world_pcap"])
    assert res["state"] == "VERIFIED_EVENT"
    assert res["brier_score"] <= 0.10
