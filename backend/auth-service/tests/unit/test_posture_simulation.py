import pytest
from app.services.simulation.simulation_scenario_engine import SimulationScenarioEngine
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService


def test_posture_delta_simulation():
    twin_service = DigitalSecurityTwinService()
    twin = twin_service.create_twin_from_snapshot("snap_pos", [])
    engine = SimulationScenarioEngine(twin_service=twin_service)

    run = engine.run_scenario(twin.twin_id, "ACCOUNT_TAKEOVER", simulated_threat_level=0.90)

    assert run.risk_delta > 0.0
    assert run.simulated_risk > run.baseline_risk
    assert run.exposure_delta > 0.0
