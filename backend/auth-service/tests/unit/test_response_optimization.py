import pytest
from app.services.autonomous_defense.response_optimization_engine import ResponseOptimizationEngine

def test_response_optimization_metrics():
    engine = ResponseOptimizationEngine()
    rsp = engine.get_response_metrics("rsp_darkstorm_waf")
    assert rsp is not None
    assert rsp.effectiveness == "RESPONSE_EFFECTIVE"
    assert rsp.containment_time_sec < 60.0
