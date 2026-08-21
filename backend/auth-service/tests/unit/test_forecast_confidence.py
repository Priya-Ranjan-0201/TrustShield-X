import pytest
from app.services.global_intelligence.predictive_threat_forecasting_engine import PredictiveThreatForecastingEngine

def test_forecast_confidence_scoring():
    engine = PredictiveThreatForecastingEngine()
    fcst = engine.get_forecast("fcst_darkstorm_short_term")
    assert fcst is not None
    assert fcst.confidence_score == 0.88
