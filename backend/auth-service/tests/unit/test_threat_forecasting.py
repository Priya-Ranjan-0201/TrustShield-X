import pytest
from app.services.threat_intelligence_fusion.predictive_threat_intelligence_engine import PredictiveThreatIntelligenceEngine

def test_threat_forecasting_creation():
    engine = PredictiveThreatIntelligenceEngine()
    fc = engine.create_forecast(
        predicted_threat="Credential stuffing attack on customer login endpoints",
        forecast_horizon="24_HOURS",
        predicted_probability=0.88,
        evidence=["ev_credential_dump_forum"],
        assumptions=["Attackers hold valid credentials"]
    )
    assert fc.forecast_horizon == "24_HOURS"
    assert fc.state == "HIGH_CONFIDENCE_FORECAST"
