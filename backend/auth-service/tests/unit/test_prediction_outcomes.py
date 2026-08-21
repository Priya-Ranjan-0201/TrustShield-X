import pytest
from app.services.predictive.prediction_calibration_engine import PredictionCalibrationEngine


def test_prediction_outcomes_and_brier_penalties():
    engine = PredictionCalibrationEngine()

    # Prediction 1: 0.90 prob, event OCCURRED (brier = 0.01)
    p1 = engine.record_prediction("Domain will be active", 0.90)
    engine.evaluate_outcome(p1.prediction_id, "OCCURRED")

    # Prediction 2: 0.80 prob, event DID_NOT_OCCUR (brier = 0.64)
    p2 = engine.record_prediction("False expansion claim", 0.80)
    engine.evaluate_outcome(p2.prediction_id, "DID_NOT_OCCUR")

    avg_brier = engine.get_average_brier_score()
    # (0.01 + 0.64) / 2 = 0.325
    assert avg_brier == 0.325
