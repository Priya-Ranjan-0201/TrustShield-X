import pytest
from app.services.ai_governance.model_registry_engine import ModelRegistryEngine

def test_model_risk_classification():
    engine = ModelRegistryEngine()
    m = engine.get_model("mdl_c2_neural_classifier")
    assert m.risk_class in ("LOW", "MODERATE", "HIGH", "CRITICAL")
