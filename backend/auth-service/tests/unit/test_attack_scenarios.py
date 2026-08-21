import pytest
from app.services.digital_twin_lab.attack_path_simulation_engine import AttackPathSimulationEngine

def test_multi_stage_attack_path_simulation():
    engine = AttackPathSimulationEngine()
    sim = engine.simulate_attack_path("scen_phishing_lateral_movement")
    assert len(sim.stages) == 5
    assert sim.stages[0]["stage"] == "INITIAL_ACCESS"
    assert sim.stages[-1]["stage"] == "OBJECTIVE"
    assert sim.claim_status == "SIMULATED"
