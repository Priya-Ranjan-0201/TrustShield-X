import pytest
from app.services.global_intelligence.intelligence_normalization_engine import IntelligenceNormalizationEngine

def test_intelligence_schema_validation():
    engine = IntelligenceNormalizationEngine()
    rec = engine.normalize_record("src_01", {"indicator": "198.51.100.22", "severity": "MEDIUM", "confidence": 0.88})
    assert rec.severity == "MEDIUM"
    assert rec.confidence_score == 0.88
