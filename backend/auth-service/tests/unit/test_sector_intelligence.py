import pytest
from app.services.threat_intelligence_fusion.threat_landscape_engine import ThreatLandscapeEngine

def test_sector_intelligence_profile():
    engine = ThreatLandscapeEngine()
    profile = engine.get_sector_profile("Financial Services")
    assert profile["sector"] == "FINANCIAL_SERVICES"
    assert profile["threat_index"] >= 8.0
