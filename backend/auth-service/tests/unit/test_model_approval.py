import pytest
from app.services.ai_governance.model_registry_engine import ModelRegistryEngine

def test_model_approval_status():
    engine = ModelRegistryEngine()
    m = engine.get_model("mdl_c2_neural_classifier")
    assert m.approval_status == "APPROVED"
    assert m.deployment_status == "DEPLOYED"
