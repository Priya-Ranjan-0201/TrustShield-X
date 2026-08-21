import pytest
from app.services.threat_intelligence_fusion.feed_ingestion_engine import FeedIngestionEngine

def test_feed_circuit_breaker():
    engine = FeedIngestionEngine()
    engine.trip_circuit_breaker("src_broken_feed")
    res = engine.ingest_feed("src_broken_feed", "COMMERCIAL", {"data": "test"})
    assert res["status"] == "CIRCUIT_BREAKER_ACTIVE"
    
    engine.reset_circuit_breaker("src_broken_feed")
    res_ok = engine.ingest_feed("src_broken_feed", "COMMERCIAL", {"data": "test_after_reset"})
    assert res_ok["status"] == "INGESTED_SUCCESSFULLY"
