import pytest
from app.services.threat_intelligence_fusion.multi_source_corroboration_engine import MultiSourceCorroborationEngine

def test_syndicated_feed_amplification_defense():
    engine = MultiSourceCorroborationEngine()
    # 3 feeds copying the exact same text verbatim
    copied_claims = [
        {"source_id": "feed_1", "content": "Exact same syndicated press release text."},
        {"source_id": "feed_2", "content": "Exact same syndicated press release text."},
        {"source_id": "feed_3", "content": "Exact same syndicated press release text."},
    ]
    res = engine.calculate_corroboration(copied_claims)
    assert res["is_syndicated_reproduction"] is True
    assert res["effective_independent_sources"] == 1
    assert res["assessment"] == "SINGLE_OR_SYNDICATED_SOURCE"
