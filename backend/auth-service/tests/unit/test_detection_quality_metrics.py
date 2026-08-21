import pytest
from app.services.autonomous_defense.detection_optimization_engine import DetectionOptimizationEngine

def test_detection_quality_precision_recall():
    engine = DetectionOptimizationEngine()
    rule = engine.list_rules()[0]
    assert rule.precision == 0.96
    assert rule.recall == 0.92
    assert rule.detection_latency_ms < 50.0
