import pytest
from app.services.autonomous_defense.response_optimization_engine import ResponseOptimizationEngine

def test_response_effectiveness_evaluation():
    engine = ResponseOptimizationEngine()
    res = engine.evaluate_response_outcome(
        response_id="rsp_test_01",
        playbook_name="Fast WAF",
        containment_time_sec=45.0,
        recovery_time_sec=90.0,
        has_collateral_impact=False,
    )
    assert res.effectiveness == "RESPONSE_EFFECTIVE"
