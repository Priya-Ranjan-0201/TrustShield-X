import pytest
from app.services.autonomous_defense.detection_optimization_engine import DetectionOptimizationEngine

def test_false_negative_rule_optimization():
    engine = DetectionOptimizationEngine()
    res = engine.evaluate_rule_optimization("rule_darkstorm_c2_entropy", candidate_precision=0.98, candidate_recall=0.94)
    assert res["is_approved"] is True
    assert res["status"] == "VALIDATED"
