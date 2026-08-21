import pytest
from app.services.cyber_digital_twin.attack_simulation_engine import AttackSimulationEngine

def test_adversary_emulation_profile():
    engine = AttackSimulationEngine()
    sim = engine.run_attack_simulation("SIM-ADV-01", "t1", "API-GW", adversary_profile="LOCKBIT_RANSOMWARE")
    assert sim["adversary_profile"] == "LockBit 3.0 Ransomware Operator"
    assert len(sim["mitre_attack_mappings"]) > 0
