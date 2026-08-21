import pytest
from app.services.ai_governance.ai_output_validation_engine import AIOutputValidationEngine

def test_ai_claim_provenance_metadata():
    engine = AIOutputValidationEngine()
    prov = engine.validate_claim_grounding("C2 beacon anomaly", ["Sigma alert"], 0.94)
    assert prov.model_id == "mdl_c2_neural_classifier"
    assert prov.model_version == "2.1.0"
