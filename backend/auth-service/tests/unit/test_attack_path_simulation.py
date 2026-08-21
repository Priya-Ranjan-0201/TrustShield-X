import pytest
from app.services.simulation.simulation_scenario_engine import SimulationScenarioEngine
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService


def test_simulated_attack_paths():
    twin_service = DigitalSecurityTwinService()
    twin = twin_service.create_twin_from_snapshot("snap_ap", [])
    engine = SimulationScenarioEngine(twin_service=twin_service)

    run = engine.run_scenario(twin.twin_id, "MALWARE_CAMPAIGN", target_asset="CorporateEndpoint")
    assert len(run.simulated_attack_paths) >= 1
    # Check that all path nodes carry explicit SIMULATED classification
    for p in run.simulated_attack_paths:
        assert p["classification"] == "SIMULATED"
