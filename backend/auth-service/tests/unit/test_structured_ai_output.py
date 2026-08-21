import pytest
from app.services.ai_governance.ai_output_validation_engine import AIOutputValidationEngine

def test_structured_ai_output_schema():
    engine = AIOutputValidationEngine()
    prov = engine.validate_claim_grounding("Valid claim", ["Log"], 0.90)
    assert prov.claim_id is not None
    assert prov.timestamp is not None
