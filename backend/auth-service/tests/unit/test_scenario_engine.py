import pytest
from app.services.cyber_digital_twin.cyber_simulation_scenario_engine import CyberSimulationScenarioEngine

def test_scenario_creation():
    engine = CyberSimulationScenarioEngine()
    scen = engine.create_scenario(
        scenario_id="SCEN-01",
        tenant_id="t1",
        name="Ransomware Outbreak",
        description="Simulates LockBit ransomware propagation",
        objective="Validate endpoint isolation",
        simulation_mode="ATTACK_SIMULATION"
    )
    assert scen["scenario_id"] == "SCEN-01"
    assert scen["status"] == "DRAFT"
    assert scen["simulation_mode"] == "ATTACK_SIMULATION"
