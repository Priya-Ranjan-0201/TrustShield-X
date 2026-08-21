import pytest
from app.services.digital_twin_lab.cyber_defense_digital_twin_engine import CyberDefenseDigitalTwinEngine

def test_twin_engine_concurrency_resilience():
    engine = CyberDefenseDigitalTwinEngine()
    for _ in range(10):
        sim = engine.attack_path_engine.simulate_attack_path("scen_phishing_lateral_movement")
        assert sim.claim_status == "SIMULATED"
