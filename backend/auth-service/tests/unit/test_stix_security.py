import pytest
from app.services.threat_intelligence.intelligence_normalization_engine import IntelligenceNormalizationEngine


def test_stix_security_malformed_object_handling():
    engine = IntelligenceNormalizationEngine()

    malformed_stix = {
        "type": "unknown-weird-type",
        "pattern": "[file:hashes.'SHA-256' = '44d88612fea8a8f36de82e1278abb02f']",
        "confidence": 0.85,
    }
    obj = engine.normalize(malformed_stix, source_id="src_stix", feed_format="STIX2")

    assert obj.object_type == "INDICATOR"
    assert obj.status == "ACTIVE"
