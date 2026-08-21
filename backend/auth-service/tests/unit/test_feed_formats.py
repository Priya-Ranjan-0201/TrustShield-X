import pytest
from app.services.threat_intelligence_fusion.feed_ingestion_engine import FeedIngestionEngine

def test_feed_formats_support():
    engine = FeedIngestionEngine()
    formats = ["STIX", "TAXII", "JSON", "CSV", "RSS"]
    for idx, fmt in enumerate(formats):
        res = engine.ingest_feed(
            source_id=f"src_{fmt.lower()}",
            source_type="OPEN_SOURCE",
            payload={"format": fmt, "indicators": [f"192.168.1.{idx + 10}"]},
            format_type=fmt
        )
        assert res["status"] == "INGESTED_SUCCESSFULLY"
