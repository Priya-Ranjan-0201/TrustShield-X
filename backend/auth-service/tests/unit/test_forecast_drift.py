import pytest
from app.services.global_intelligence.forecast_calibration_engine import ForecastCalibrationEngine

def test_forecast_drift_monitoring():
    engine = ForecastCalibrationEngine()
    calibs = engine.list_calibrations()
    assert len(calibs) >= 1
    assert calibs[0]["accuracy_score"] == 0.96
