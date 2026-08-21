import pytest
from app.services.digital_twin_lab.defense_strategy_optimizer import DefenseStrategyOptimizer

def test_pareto_frontier_calculation():
    engine = DefenseStrategyOptimizer()
    cmp_res = engine.compare_strategies("scen_phishing_lateral_movement")
    assert len(cmp_res.pareto_frontier) >= 2
    assert "STRATEGY_A_AUTOMATED_ISOLATION" in cmp_res.pareto_frontier
