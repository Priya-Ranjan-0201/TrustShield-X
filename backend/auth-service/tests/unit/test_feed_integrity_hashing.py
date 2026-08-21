import pytest
from app.services.threat_intelligence_fusion.feed_ingestion_engine import FeedIngestionEngine

def test_feed_content_integrity_hashing():
    engine = FeedIngestionEngine()
    payload = {"indicators": ["1.1.1.1"], "confidence": 0.9}
    res = engine.ingest_feed("src_test_hash", "ISAC", payload)
    assert len(res["content_hash"]) == 64
    assert res["record"].content_hash == res["content_hash"]
