import pytest
from app.services.ai_governance.ai_output_validation_engine import AIOutputValidationEngine

def test_ai_output_grounded_validation():
    engine = AIOutputValidationEngine()
    prov = engine.validate_claim_grounding(
        claim_text="DarkStorm utilizes port 8443",
        evidence_list=["Zeek flow log #12"],
        confidence=0.95,
    )
    assert prov.validation_status == "EVIDENCE_SUPPORTED"
