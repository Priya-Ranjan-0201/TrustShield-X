import pytest
from app.services.ai_governance.model_registry_engine import ModelRegistryEngine

def test_model_integrity_verification():
    engine = ModelRegistryEngine()
    res = engine.verify_model_integrity("mdl_c2_neural_classifier", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    assert res["is_verified"] is True
    assert res["status"] == "VERIFIED"
