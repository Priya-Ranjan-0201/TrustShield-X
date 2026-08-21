import pytest
from app.services.cyber_digital_twin.attack_simulation_engine import AttackSimulationEngine

def test_non_destructive_attack_simulation():
    engine = AttackSimulationEngine()
    sim = engine.run_attack_simulation("SIM-ATK-01", "t1", "WEB-APP-INGRESS", adversary_profile="APT29_COZY_BEAR")
    assert sim["is_simulation"] is True
    assert sim["production_impact"] == "ZERO_MUTATION_SIMULATION_ONLY"
    assert len(sim["steps"]) == 3
