import pytest
from app.services.autonomous_defense.model_governance_engine import ModelGovernanceEngine

def test_model_poisoning_quarantine_flow():
    engine = ModelGovernanceEngine()
    res = engine.evaluate_model_integrity("mdl_c2_neural_classifier", observed_precision=0.50, is_poisoned=True)
    assert res["status"] == "QUARANTINED"
