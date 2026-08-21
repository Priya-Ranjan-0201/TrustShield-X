import pytest
from app.services.cyber_digital_twin.cyber_simulation_scenario_engine import CyberSimulationScenarioEngine

def test_simulation_reproducibility():
    engine = CyberSimulationScenarioEngine()
    engine.create_scenario("SCEN-REP", "t1", "Rep Test", "Desc", "Obj")
    run1 = engine.execute_simulation_run("RUN-1", "SCEN-REP", "t1", "SNAP-01", random_seed=123)
    run2 = engine.execute_simulation_run("RUN-2", "SCEN-REP", "t1", "SNAP-01", random_seed=123)
    assert run1["results_summary"] == run2["results_summary"]
