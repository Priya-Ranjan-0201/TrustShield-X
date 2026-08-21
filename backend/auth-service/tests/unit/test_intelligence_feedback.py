import pytest
from app.services.federation.source_reputation_engine import SourceReputationEngine


def test_intelligence_feedback_loop():
    engine = SourceReputationEngine()
    engine.register_feed("src_partner_feed", "Partner Threat Stream", initial_reliability=0.85)

    # 1. False positive feedback decreases reliability
    engine.record_feedback_outcome("src_partner_feed", is_false_positive=True)
    engine.record_feedback_outcome("src_partner_feed", is_false_positive=True)

    sources = engine.list_sources()
    src = next(s for s in sources if s.source_id == "src_partner_feed")
    assert src.false_positives_count == 2
