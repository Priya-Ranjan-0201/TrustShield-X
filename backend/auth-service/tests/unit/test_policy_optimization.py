import pytest
from app.services.security_engineering.policy_optimization_engine import PolicyOptimizationEngine

def test_policy_optimization():
    engine = PolicyOptimizationEngine()
    res = engine.analyze_policy_health()
    assert res["security_posture_weakened"] is False
    assert len(res["optimization_recommendations"]) >= 1
