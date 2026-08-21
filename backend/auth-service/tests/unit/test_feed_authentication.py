import pytest
from app.services.threat_intelligence_fusion.feed_ingestion_engine import FeedIngestionEngine

def test_feed_authentication_verification():
    engine = FeedIngestionEngine()
    # Invalid token check
    res_fail = engine.ingest_feed(
        source_id="src_test",
        source_type="COMMERCIAL",
        payload={"data": "test"},
        auth_token="INVALID_CREDENTIALS"
    )
    assert res_fail["status"] == "AUTHENTICATION_FAILED"
    
    # Valid auth
    res_ok = engine.ingest_feed(
        source_id="src_test",
        source_type="COMMERCIAL",
        payload={"data": "test_auth_ok"},
        auth_token="VALID_TOKEN_123"
    )
    assert res_ok["status"] == "INGESTED_SUCCESSFULLY"
