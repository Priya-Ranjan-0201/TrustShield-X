import pytest
from app.services.autonomous_defense.alert_optimization_engine import AlertOptimizationEngine

def test_false_positive_learning_rate():
    engine = AlertOptimizationEngine()
    metrics = engine.get_optimization_metrics()
    assert metrics.false_positive_rate == 0.04
