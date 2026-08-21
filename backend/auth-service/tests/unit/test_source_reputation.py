import pytest
from app.services.federation.source_reputation_engine import SourceReputationEngine


def test_source_reputation_recalibration():
    engine = SourceReputationEngine()
    src = engine.register_feed("src_test_feed", "Test Feed Provider", initial_reliability=0.85)

    # 1. Successful verified indicators increase reputation
    for _ in range(10):
        engine.record_feedback_outcome("src_test_feed", is_verified=True)

    updated = engine.list_sources()
    test_src = next(s for s in updated if s.source_id == "src_test_feed")
    assert test_src.reliability_score >= 0.90
    assert test_src.verified_indicators_count == 10
