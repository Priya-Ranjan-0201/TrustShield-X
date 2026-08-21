import pytest
from app.services.digital_twin_lab.defense_strategy_optimizer import DefenseStrategyOptimizer

def test_defense_strategy_optimization_and_ranking():
    engine = DefenseStrategyOptimizer()
    cmp_res = engine.compare_strategies("scen_phishing_lateral_movement")
    assert cmp_res.recommended_strategy == "STRATEGY_A_AUTOMATED_ISOLATION"
    assert cmp_res.reversibility == "FULLY_REVERSIBLE"
