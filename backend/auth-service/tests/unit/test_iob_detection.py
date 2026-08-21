import pytest
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine

def test_iob_indicator_of_behavior_registration():
    engine = IndicatorIntelligenceEngine()
    iob = engine.register_indicator(
        raw_value="Rapid metadata endpoint enumeration from unauthenticated IAM role",
        indicator_type="PROCESS",
        behavior_type="IOB_CLOUD_METADATA_ABUSE",
        confidence=0.91
    )
    assert iob.behavior_type == "IOB_CLOUD_METADATA_ABUSE"
