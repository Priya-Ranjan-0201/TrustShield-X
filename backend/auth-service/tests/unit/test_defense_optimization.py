import pytest
from app.services.cyber_digital_twin.defense_optimization_engine import DefenseOptimizationEngine

def test_defense_strategy_optimization():
    engine = DefenseOptimizationEngine()
    strat = engine.optimize_defense_strategy("OPT-01", "t1", "API-GW", "APT29", baseline_risk=8.5)
    assert strat["recommended_strategy"]["is_pareto_optimal"] is True
    assert strat["recommended_strategy"]["recommendation_rank"] == 1
    assert len(strat["candidate_comparisons"]) == 3
