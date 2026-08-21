import pytest
from app.services.digital_twin_lab.simulation_calibration_engine import SimulationCalibrationEngine

def test_simulation_vs_reality_divergence_tracking():
    engine = SimulationCalibrationEngine()
    rec = engine.record_calibration(
        scenario_id="scen_large_drill",
        predicted_outcome={"containment_time_seconds": 10.0},
        actual_outcome={"containment_time_seconds": 90.0},
    )
    assert rec.error_classification == "UNDERPREDICTION"
    assert rec.bias_metric < 0.0
