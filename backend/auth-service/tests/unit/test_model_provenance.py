import pytest
from app.services.ai_governance.model_registry_engine import ModelRegistryEngine

def test_model_provenance_source():
    engine = ModelRegistryEngine()
    model = engine.get_model("mdl_c2_neural_classifier")
    assert model.source.startswith("s3://")
    assert model.version == "2.1.0"
