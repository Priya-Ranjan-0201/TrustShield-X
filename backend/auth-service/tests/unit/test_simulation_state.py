import pytest
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService


def test_simulation_state_lifecycle():
    service = DigitalSecurityTwinService()
    twin = service.create_twin_from_snapshot("snap_state", [])

    # Transition to SIMULATED_COMPROMISED
    service.transition_state(twin.twin_id, "SIMULATED_COMPROMISED", simulated_risk_score=85.0)
    assert twin.state == "SIMULATED_COMPROMISED"

    # Transition to CONTAINED_SIMULATION
    service.transition_state(twin.twin_id, "CONTAINED_SIMULATION", simulated_risk_score=45.0)
    assert twin.state == "CONTAINED_SIMULATION"
