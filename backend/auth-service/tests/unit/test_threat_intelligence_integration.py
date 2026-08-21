import pytest
from app.services.cyber_digital_twin.attack_simulation_engine import AttackSimulationEngine

def test_threat_intelligence_feed_scenario_generation():
    engine = AttackSimulationEngine()
    sim = engine.run_attack_simulation("SIM-TI", "t1", "WEB-APP", adversary_profile="FIN7_FINANCIAL")
    assert sim["adversary_profile"] == "FIN7 Financial Syndicate"
