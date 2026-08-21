import pytest
from app.services.threat_intelligence.threat_intelligence_fabric import ThreatIntelligenceFabric


def test_feed_ingestion_normalization_and_deduplication():
    fabric = ThreatIntelligenceFabric()
    raw = {
        "type": "ipv4-addr",
        "value": "203.0.113.88",
        "confidence": 0.95,
    }

    res = fabric.ingest_raw_intelligence(raw, source_id="src_crowdstrike_falcon", feed_format="STIX2")
    assert res["object"].canonical_value == "203.0.113.88"
    assert res["object"].object_type == "IP"
    assert res["deduplication"]["is_duplicate"] is False
