import pytest
from app.services.global_intelligence.predictive_threat_forecasting_engine import PredictiveThreatForecastingEngine

def test_predictive_threat_forecasting():
    engine = PredictiveThreatForecastingEngine()
    fcst = engine.generate_forecast(
        subject="DarkStorm Credential Attack Trend",
        horizon="SHORT_TERM",
        prediction="Expected 30% increase in token stuffing attacks.",
        evidence=["Observed C2 burst", "Historical 72h periodicity"],
    )
    assert fcst.horizon == "SHORT_TERM"
    assert fcst.confidence_score >= 0.80
    assert fcst.calibration_status == "CALIBRATED"
