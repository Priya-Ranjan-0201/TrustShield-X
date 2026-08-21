import pytest
from app.services.hunting.predictive_defense_engine import PredictiveDefenseEngine


def test_exposure_forecasting():
    engine = PredictiveDefenseEngine()

    pred = engine.forecast_threat_progression(
        target_subject="CloudInfrastructureGroup",
        prediction_type="EXPOSURE_ESCALATION",
        horizon="LONG_TERM",
        predicted_probability=0.68,
    )

    assert pred.horizon == "LONG_TERM"
    assert pred.predicted_probability == 0.68
