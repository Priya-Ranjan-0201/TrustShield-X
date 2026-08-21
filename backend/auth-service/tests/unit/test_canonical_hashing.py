import pytest
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine

def test_canonical_hashing_consistency():
    engine = IndicatorIntelligenceEngine()
    ind1 = engine.register_indicator("bad-domain.com", "DOMAIN")
    ind2 = engine.register_indicator("BAD-DOMAIN.COM ", "DOMAIN")
    assert ind1.canonical_hash == ind2.canonical_hash
