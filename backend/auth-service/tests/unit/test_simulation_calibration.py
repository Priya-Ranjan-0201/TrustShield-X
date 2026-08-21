import pytest
from app.services.digital_twin_lab.simulation_calibration_engine import SimulationCalibrationEngine

def test_simulation_calibration_and_error_scoring():
    engine = SimulationCalibrationEngine()
    rec = engine.record_calibration(
        scenario_id="scen_phishing_lateral_movement",
        predicted_outcome={"containment_time_seconds": 45.0},
        actual_outcome={"containment_time_seconds": 43.0},
    )
    assert rec.error_classification == "CORRECT"
    assert rec.calibration_score >= 0.95
