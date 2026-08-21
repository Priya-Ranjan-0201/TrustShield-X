import pytest
from app.services.autonomous_defense.detection_optimization_engine import DetectionOptimizationEngine

def test_detection_drift_trigger():
    engine = DetectionOptimizationEngine()
    drift_status = engine.detect_rule_drift("rule_darkstorm_c2_entropy", false_positive_spike=True)
    assert drift_status == "DETECTION_DRIFT"
