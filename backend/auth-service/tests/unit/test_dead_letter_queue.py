import pytest
from app.services.threat_intelligence_fusion.feed_ingestion_engine import FeedIngestionEngine

def test_dead_letter_queue_routing():
    engine = FeedIngestionEngine()
    # Empty/invalid payload
    res = engine.ingest_feed("src_malformed", "VENDOR", {})
    assert res["status"] == "ROUTED_TO_DEAD_LETTER_QUEUE"
    assert len(engine.get_dead_letter_queue()) >= 1
