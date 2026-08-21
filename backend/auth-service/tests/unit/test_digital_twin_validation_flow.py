import pytest
from app.services.autonomous_defense.digital_twin_validation_bridge import DigitalTwinValidationBridge

def test_digital_twin_pre_validation():
    bridge = DigitalTwinValidationBridge()
    sim = bridge.simulate_candidate_improvement("Candidate Rate Limit Rule")
    assert sim["simulation_status"] == "SIMULATED"
    assert sim["simulated_containment_rate"] >= 0.90
    assert sim["invariant_note"] == "SIMULATION_DOES_NOT_EQUAL_PRODUCTION_FACT"
