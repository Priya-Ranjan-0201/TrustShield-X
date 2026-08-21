import pytest
from app.services.digital_twin_lab.security_scenario_engine import SecurityScenarioEngine

def test_deterministic_scenario_reproducibility():
    engine = SecurityScenarioEngine()
    sc1 = engine.get_scenario("scen_phishing_lateral_movement")
    assert sc1 is not None
    assert sc1.constraints["max_lateral_hops"] == 3
    assert sc1.initial_state_version == "v1.0.0-PROD-SYNC"
