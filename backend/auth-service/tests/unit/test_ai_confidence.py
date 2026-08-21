import pytest
from app.services.ai_governance.ai_output_validation_engine import AIOutputValidationEngine

def test_ai_low_confidence_flagged():
    engine = AIOutputValidationEngine()
    prov = engine.validate_claim_grounding("Uncertain threat anomaly", ["Weak signal"], confidence=0.60)
    assert prov.validation_status == "AI_LOW_CONFIDENCE"
