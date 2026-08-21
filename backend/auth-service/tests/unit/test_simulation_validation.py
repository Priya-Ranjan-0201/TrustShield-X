import pytest
from app.services.cyber_digital_twin.digital_twin_validation_governance_engine import DigitalTwinValidationGovernanceEngine

def test_simulation_calibration_against_observation():
    engine = DigitalTwinValidationGovernanceEngine()
    cal = engine.calibrate_simulation(
        "CAL-01",
        "t1",
        predicted_outcome={"risk_score": 4.5},
        actual_observed_outcome={"risk_score": 4.8}
    )
    assert cal["accuracy_score"] >= 0.95
    assert cal["calibration_status"] == "CALIBRATED"
