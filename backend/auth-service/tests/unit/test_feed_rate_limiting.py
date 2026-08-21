import pytest
from app.services.threat_intelligence_fusion.feed_ingestion_engine import FeedIngestionEngine

def test_feed_rate_limiting_and_deduplication():
    engine = FeedIngestionEngine()
    payload = {"data": "rate_limit_test"}
    res1 = engine.ingest_feed("src_rate", "COMMERCIAL", payload)
    assert res1["status"] == "INGESTED_SUCCESSFULLY"
    
    # Ingesting exact same payload triggers deduplication skip
    res2 = engine.ingest_feed("src_rate", "COMMERCIAL", payload)
    assert res2["status"] == "DUPLICATE_INGESTION_SKIPPED"
