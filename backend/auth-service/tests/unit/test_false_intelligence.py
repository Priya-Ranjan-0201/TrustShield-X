import pytest
from app.services.global_intelligence.intelligence_normalization_engine import IntelligenceNormalizationEngine

def test_false_intelligence_unverified_labeling():
    engine = IntelligenceNormalizationEngine()
    rec = engine.normalize_record("src_untrusted", {"indicator": "rumor_c2.org", "confidence": 0.30})
    assert rec.confidence_score == 0.30
    assert rec.claim_status == "REPORTED"
