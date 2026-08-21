import pytest
from app.services.federation.source_reputation_engine import SourceReputationEngine


def test_stix_taxii_parsing():
    engine = SourceReputationEngine()
    stix_json = {
        "id": "indicator--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
        "pattern": "[domain-name:value = 'banking-trojan-drop.ru']",
        "confidence": 92,
    }
    parsed = engine.parse_stix_taxii_indicator(stix_json)
    assert parsed["intelligence_type"] == "DOMAIN"
    assert parsed["confidence"] == 0.92
    assert parsed["stix_id"].startswith("indicator--")
