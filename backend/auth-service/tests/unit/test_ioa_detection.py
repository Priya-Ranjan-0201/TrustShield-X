import pytest
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine

def test_ioa_indicator_of_attack_registration():
    engine = IndicatorIntelligenceEngine()
    ioa = engine.register_indicator(
        raw_value="powershell.exe -enc JABzAD0...",
        indicator_type="PROCESS",
        behavior_type="IOA_OBFUSCATED_COMMAND",
        confidence=0.89
    )
    assert ioa.behavior_type == "IOA_OBFUSCATED_COMMAND"
