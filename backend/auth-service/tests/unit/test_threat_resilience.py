import pytest
from app.services.resilience.resilience_digital_twin_engine import ResilienceDigitalTwinEngine

def test_threat_resilience():
    engine = ResilienceDigitalTwinEngine()
    sim = engine.simulate_attack_and_disruption("ast_pg_primary", "RANSOMWARE_ATTACK")
    assert sim["mode"] == "SIMULATED"
    assert len(sim["cascading_failures"]) > 0
