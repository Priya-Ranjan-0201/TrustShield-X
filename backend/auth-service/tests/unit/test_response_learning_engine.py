import pytest
from app.services.autonomous_defense.response_optimization_engine import ResponseOptimizationEngine

def test_response_unverified_outcome():
    engine = ResponseOptimizationEngine()
    res = engine.evaluate_response_outcome(
        response_id="rsp_test_02",
        playbook_name="Fast WAF",
        containment_time_sec=45.0,
        recovery_time_sec=90.0,
        is_outcome_verified=False,
    )
    assert res.effectiveness == "OUTCOME_NOT_VERIFIED"
