import pytest
from app.services.autonomous_defense.model_governance_engine import ModelGovernanceEngine

def test_model_governance_registry():
    engine = ModelGovernanceEngine()
    models = engine.list_models()
    assert len(models) >= 1
    assert models[0].precision >= 0.95
    assert models[0].status == "DEPLOYED"
