import pytest
from app.services.global_intelligence.intelligence_normalization_engine import IntelligenceNormalizationEngine

def test_intelligence_normalization_and_hashing():
    engine = IntelligenceNormalizationEngine()
    norm = engine.normalize_record("src_01", {"value": "phishing.evil.com", "severity": "CRITICAL"})
    assert norm.indicator == "phishing.evil.com"
    assert len(norm.evidence_hashes) == 1
    assert norm.provenance[0]["source_id"] == "src_01"
