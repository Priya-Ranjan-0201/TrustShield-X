import pytest
from app.services.hunting.predictive_defense_engine import PredictiveDefenseEngine
from app.services.hunting.prediction_calibration_engine import PredictionCalibrationEngine


def test_prediction_feedback_outcome_recording():
    pred_engine = PredictiveDefenseEngine()
    calib_engine = PredictionCalibrationEngine()

    pred = pred_engine.forecast_threat_progression("DomainXYZ", "INFRASTRUCTURE_REUSE")
    assert pred.actual_outcome == "UNRESOLVED"

    updated = calib_engine.record_prediction_outcome(pred, "PARTIALLY_CORRECT")
    assert updated.actual_outcome == "PARTIALLY_CORRECT"
    assert updated.outcome_observed_at is not None
