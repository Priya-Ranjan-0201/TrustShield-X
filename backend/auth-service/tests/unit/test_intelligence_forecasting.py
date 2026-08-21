import pytest
from app.services.threat_intelligence.threat_forecast_engine import ThreatForecastEngine


def test_threat_forecasting_with_sufficient_and_insufficient_data():
    engine = ThreatForecastEngine()

    # Sufficient data
    fc_valid = engine.generate_forecast("Operation ShadowStrike", historical_data_points=20, growth_estimate=15.0)
    assert fc_valid.status == "PREDICTED"
    assert fc_valid.predicted_growth_rate_pct == 15.0

    # Insufficient data
    fc_empty = engine.generate_forecast("Unknown New Actor", historical_data_points=1)
    assert fc_empty.status == "NOT_ENOUGH_DATA"
