import pytest
from app.services.cyber_digital_twin.attack_simulation_engine import AttackSimulationEngine

def test_attack_chain_step_containment():
    engine = AttackSimulationEngine()
    sim = engine.run_attack_simulation("SIM-CHAIN-01", "t1", "DB-INGRESS")
    assert sim["contained"] is True
    assert any(s.get("prevented_by_control") for s in sim["steps"])
