import pytest
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine

def test_indicator_normalization_varieties():
    engine = IndicatorIntelligenceEngine()
    norm_url = engine.normalize_value("  HTTP://EXAMPLE.COM/Path/  ", "URL")
    assert norm_url == "http://example.com/path"
    
    norm_hash = engine.normalize_value("  E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855  ", "HASH")
    assert norm_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
