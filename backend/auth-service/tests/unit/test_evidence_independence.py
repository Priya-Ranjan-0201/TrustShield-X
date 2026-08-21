import pytest
from app.services.knowledge_fabric.evidence_strength_engine import EvidenceStrengthEngine


def test_evidence_independence_duplicate_detection():
    engine = EvidenceStrengthEngine()

    # 10 duplicate copies of the same source
    dup_sources = ["SOURCE_EDR_SENSOR_1"] * 10
    indep_score_dup = engine.evaluate_independence(dup_sources)
    assert indep_score_dup == 0.1  # Only 1 unique out of 10

    # 4 distinct independent sources
    distinct_sources = ["SOURCE_EDR", "SOURCE_PCAP", "SOURCE_AUTH_LOG", "SOURCE_HONEYPOT"]
    indep_score_distinct = engine.evaluate_independence(distinct_sources)
    assert indep_score_distinct == 1.0
