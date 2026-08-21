import pytest
from app.services.cyber_digital_twin.cyber_simulation_scenario_engine import CyberSimulationScenarioEngine

def test_scenario_lifecycle_transitions():
    engine = CyberSimulationScenarioEngine()
    engine.create_scenario("SCEN-LIFE", "t1", "Test", "Desc", "Obj")
    
    # State transitions: DRAFT -> READY -> RUNNING -> COMPLETED
    ready = engine.update_scenario_status("SCEN-LIFE", "t1", "READY")
    assert ready["status"] == "READY"
    
    run = engine.execute_simulation_run("RUN-LIFE", "SCEN-LIFE", "t1", "SNAP-01")
    assert run["status"] == "COMPLETED"
