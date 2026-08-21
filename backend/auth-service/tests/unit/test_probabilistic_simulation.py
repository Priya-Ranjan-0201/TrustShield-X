import pytest
from app.services.digital_twin_lab.probabilistic_simulation_engine import ProbabilisticSimulationEngine

def test_probabilistic_monte_carlo_simulation():
    engine = ProbabilisticSimulationEngine()
    res = engine.run_monte_carlo_simulation("scen_phishing_lateral_movement", iterations=1000)
    assert res["iterations_executed"] == 1000
    assert res["containment_probability_mean"] >= 0.90
    assert res["claim_status"] == "PREDICTED"
