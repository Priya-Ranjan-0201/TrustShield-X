import pytest
from app.services.simulation.response_strategy_simulation_engine import ResponseStrategySimulationEngine


def test_response_candidate_simulation():
    engine = ResponseStrategySimulationEngine()
    strategies = engine.evaluate_strategies({"incident_id": "inc_2026_091"})

    assert len(strategies) >= 2
    for s in strategies:
        assert s.strategy_id.startswith("strat_")
        assert s.simulated_risk_reduction > 0.0
        assert s.reversibility in ("HIGH", "MEDIUM", "LOW")
