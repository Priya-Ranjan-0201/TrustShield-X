import pytest
from app.services.autonomous_defense.detection_optimization_engine import DetectionOptimizationEngine

def test_security_regression_rejected():
    engine = DetectionOptimizationEngine()
    # Candidate increases FP reduction but drops recall from 0.92 to 0.75
    res = engine.evaluate_rule_optimization("rule_darkstorm_c2_entropy", candidate_precision=0.99, candidate_recall=0.75)
    assert res["is_approved"] is False
    assert res["status"] == "REJECTED"
    assert "UNSAFE_OPTIMIZATION" in res["reason"]
