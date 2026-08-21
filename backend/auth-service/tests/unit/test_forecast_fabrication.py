import pytest
from app.services.global_intelligence.predictive_threat_forecasting_engine import PredictiveThreatForecastingEngine

def test_forecast_fabrication_rejection():
    engine = PredictiveThreatForecastingEngine()
    with pytest.raises(ValueError, match="FORECAST_NOT_SUPPORTED"):
        engine.generate_forecast("Arbitrary Forecast", "SHORT_TERM", "Fabricated outcome", evidence=[])
