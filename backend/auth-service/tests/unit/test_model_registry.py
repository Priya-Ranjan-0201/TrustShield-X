import pytest
from app.services.ai_governance.model_registry_engine import ModelRegistryEngine

def test_model_registry_metadata():
    engine = ModelRegistryEngine()
    model = engine.get_model("mdl_c2_neural_classifier")
    assert model is not None
    assert model.architecture == "Transformer-DeBERTa-V3"
    assert model.risk_class == "HIGH"
