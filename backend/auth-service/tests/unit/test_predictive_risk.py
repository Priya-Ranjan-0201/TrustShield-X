import pytest
from app.services.predictive.predictive_risk_engine import PredictiveRiskEngine


def test_predictive_risk_calculation():
    engine = PredictiveRiskEngine()
    risk_dto = engine.calculate_predictive_risk(
        entity_or_campaign_id="CAMP-2026-0891",
        current_observed_risk=65.0,
        campaign_velocity=1.85,
        anomaly_z_score=4.2,
        source_reliability=0.92,
        time_horizon="24H",
    )
    assert risk_dto.current_observed_risk == 65.0
    assert risk_dto.projected_risk > 65.0
    assert risk_dto.risk_delta > 0.0
    assert risk_dto.prediction_confidence >= 0.80
    assert len(risk_dto.supporting_factors) >= 1
