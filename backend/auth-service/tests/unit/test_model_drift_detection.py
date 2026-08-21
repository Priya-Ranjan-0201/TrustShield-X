import pytest
from app.services.autonomous_defense.model_governance_engine import ModelGovernanceEngine

def test_model_performance_drift_detected():
    engine = ModelGovernanceEngine()
    res = engine.evaluate_model_integrity("mdl_c2_neural_classifier", observed_precision=0.82)
    assert res["drift_status"] == "PERFORMANCE_DRIFT"
