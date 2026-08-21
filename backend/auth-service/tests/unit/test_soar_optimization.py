import pytest
from app.services.security_engineering.soar_optimization_engine import SOAROptimizationEngine

def test_soar_optimization():
    engine = SOAROptimizationEngine()
    res = engine.evaluate_playbook_performance()
    assert res["failed_executions_rate"] < 0.05
    assert len(res["recommendations"]) >= 1
