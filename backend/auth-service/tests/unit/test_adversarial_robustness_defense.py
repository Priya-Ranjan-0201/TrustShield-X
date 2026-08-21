import pytest
from app.services.autonomous_defense.model_governance_engine import ModelGovernanceEngine

def test_model_adversarial_poisoning_quarantine():
    engine = ModelGovernanceEngine()
    res = engine.evaluate_model_integrity("mdl_c2_neural_classifier", observed_precision=0.90, is_poisoned=True)
    assert res["status"] == "QUARANTINED"
    assert res["auto_rollback"] is True
