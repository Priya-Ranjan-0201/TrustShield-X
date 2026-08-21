import pytest
from app.services.hunting.predictive_defense_engine import PredictiveDefenseEngine
from app.services.hunting.prediction_calibration_engine import PredictionCalibrationEngine


def test_prediction_calibration_brier_score():
    pred_engine = PredictiveDefenseEngine()
    calib_engine = PredictionCalibrationEngine()

    p1 = pred_engine.forecast_threat_progression("HostA", "EXPOSURE_SPIKE", predicted_probability=0.90)
    p2 = pred_engine.forecast_threat_progression("HostB", "CAMPAIGN_EXPANSION", predicted_probability=0.80)

    # Record outcomes: p1 came true (CORRECT), p2 did not (INCORRECT)
    calib_engine.record_prediction_outcome(p1, "CORRECT")
    calib_engine.record_prediction_outcome(p2, "INCORRECT")

    metrics = calib_engine.calculate_calibration_metrics([p1, p2])
    assert metrics["resolved_count"] == 2
    assert metrics["accuracy"] == 0.5
    assert metrics["brier_score"] > 0.0
    assert metrics["status"] == "CALIBRATED"
