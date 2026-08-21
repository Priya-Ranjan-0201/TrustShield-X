import pytest
from app.services.hunting.predictive_defense_engine import PredictiveDefenseEngine


def test_trust_degradation_forecasting():
    engine = PredictiveDefenseEngine()

    pred = engine.forecast_threat_progression(
        target_subject="PaymentProcessorVendor",
        prediction_type="TRUST_DEGRADATION",
        horizon="SHORT_TERM",
        predicted_probability=0.81,
    )

    assert pred.prediction_type == "TRUST_DEGRADATION"
    assert pred.confidence >= 0.70
