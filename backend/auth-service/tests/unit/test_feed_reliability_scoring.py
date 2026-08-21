import pytest
from app.services.threat_intelligence_fusion.intelligence_source_registry import IntelligenceSourceRegistry

def test_feed_reliability_scoring():
    registry = IntelligenceSourceRegistry()
    scoring = registry.evaluate_source_scoring("src_cert_in_advisory")
    assert scoring["source_reliability"] == "A"
    assert scoring["freshness"] == "FRESH"
    assert scoring["approval_status"] == "APPROVED"
