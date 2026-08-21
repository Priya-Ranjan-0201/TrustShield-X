import pytest
from app.services.hunting.predictive_defense_engine import PredictiveDefenseEngine


def test_campaign_expansion_forecasting():
    engine = PredictiveDefenseEngine()

    pred = engine.forecast_threat_progression(
        target_subject="CAMP-2026-0891",
        prediction_type="CAMPAIGN_EXPANSION",
        horizon="MEDIUM_TERM",
        predicted_probability=0.74,
        confidence=0.79,
        assumptions=["Campaign actor maintains active registrar automated domain generation."],
    )

    assert pred.prediction_type == "CAMPAIGN_EXPANSION"
    assert pred.horizon == "MEDIUM_TERM"
