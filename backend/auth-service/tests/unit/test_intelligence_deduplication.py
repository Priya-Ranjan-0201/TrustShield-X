import pytest
from app.services.global_intelligence.intelligence_deduplication_engine import IntelligenceDeduplicationEngine
from app.services.global_intelligence.intelligence_normalization_engine import IntelligenceNormalizationEngine

def test_intelligence_deduplication_and_provenance_merging():
    norm_engine = IntelligenceNormalizationEngine()
    r1 = norm_engine.normalize_record("src_a", {"indicator": "bad-domain.com", "confidence": 0.80})
    r2 = norm_engine.normalize_record("src_b", {"indicator": "bad-domain.com", "confidence": 0.95})
    
    dedup = IntelligenceDeduplicationEngine()
    merged = dedup.deduplicate_records([r1, r2])
    assert len(merged) == 1
    assert merged[0].confidence_score == 0.95
    assert len(merged[0].provenance) == 2
