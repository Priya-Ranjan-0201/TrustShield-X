import pytest
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine

def test_diverse_ioc_types_support():
    engine = IndicatorIntelligenceEngine()
    types = ["IPv4", "IPv6", "DOMAIN", "URL", "HASH", "EMAIL", "CVE"]
    for t in types:
        dto = engine.register_indicator(f"sample_value_{t}", t)
        assert dto.indicator_type == t
