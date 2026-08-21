import pytest
from app.services.autonomous_defense.alert_optimization_engine import AlertOptimizationEngine

def test_alert_optimization_metrics():
    engine = AlertOptimizationEngine()
    metrics = engine.get_optimization_metrics()
    assert metrics.true_positive_rate >= 0.90
    assert metrics.false_positive_rate <= 0.10
    assert metrics.optimization_status == "OPTIMAL"
