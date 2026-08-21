import pytest
from app.services.ai_governance.ai_output_validation_engine import AIOutputValidationEngine

def test_hallucination_ungrounded_flagged():
    engine = AIOutputValidationEngine()
    prov = engine.validate_claim_grounding(
        claim_text="The attacker is located in Country X",
        evidence_list=[],
        confidence=0.90,
    )
    assert prov.validation_status == "AI_OUTPUT_UNGROUNDED"
