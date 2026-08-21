import pytest
from app.services.ai_governance.ai_security_governance_engine import AISecurityGovernanceEngine

def test_model_evaluation_metrics():
    engine = AISecurityGovernanceEngine()
    m = engine.model_engine.get_model("mdl_c2_neural_classifier")
    assert m is not None
