import pytest
from app.schemas.cyber_resilience_twin_models import DefenseStrategyCandidateDTO
from app.services.resilience_twin.defense_strategy_optimizer import DefenseStrategyOptimizer


def test_pareto_strategy_optimization():
    optimizer = DefenseStrategyOptimizer()

    candidates = [
        DefenseStrategyCandidateDTO(
            strategy_id="strat_1",
            name="Balanced Defense",
            risk_reduction=85.0,
            service_disruption=10.0,
            implementation_cost=15.0,
        ),
        DefenseStrategyCandidateDTO(
            strategy_id="strat_2",
            name="Heavy Lockout",
            risk_reduction=88.0,
            service_disruption=80.0,
            implementation_cost=60.0,
        ),
        DefenseStrategyCandidateDTO(
            strategy_id="strat_3",
            name="Weak Control",
            risk_reduction=30.0,
            service_disruption=50.0,
            implementation_cost=50.0,
        ),
    ]

    optimized = optimizer.optimize_strategies(candidates)
    strat_1 = next(c for c in optimized if c.strategy_id == "strat_1")
    assert strat_1.is_pareto_optimal is True

    strat_3 = next(c for c in optimized if c.strategy_id == "strat_3")
    assert strat_3.is_pareto_optimal is False
