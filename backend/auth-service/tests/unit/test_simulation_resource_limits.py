import pytest
from app.services.digital_twin_lab.probabilistic_simulation_engine import ProbabilisticSimulationEngine

def test_simulation_resource_limit_capping():
    engine = ProbabilisticSimulationEngine()
    res = engine.run_monte_carlo_simulation("scen_phishing_lateral_movement", iterations=100000)
    assert res["iterations_executed"] <= 5000
