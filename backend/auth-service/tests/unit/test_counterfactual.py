import pytest
from app.services.resilience_twin.counterfactual_analysis_engine import CounterfactualAnalysisEngine


def test_counterfactual_comparative_evaluation():
    engine = CounterfactualAnalysisEngine()
    comp = engine.compare_scenarios(
        baseline_risk=30.0,
        strategy_a_risk=15.0,
        strategy_b_risk=20.0,
        strategy_c_risk=8.0,
    )

    assert comp.lowest_residual_risk_strategy == "STRATEGY_C"
    assert comp.comparison_label == "SIMULATED"
    assert comp.strategy_c_risk == 8.0
