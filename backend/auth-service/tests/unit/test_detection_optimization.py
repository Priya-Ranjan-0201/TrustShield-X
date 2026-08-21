import pytest
from app.services.autonomous_defense.detection_optimization_engine import DetectionOptimizationEngine

def test_detection_optimization_list():
    engine = DetectionOptimizationEngine()
    rules = engine.list_rules()
    assert len(rules) >= 1
    assert rules[0].precision >= 0.90
