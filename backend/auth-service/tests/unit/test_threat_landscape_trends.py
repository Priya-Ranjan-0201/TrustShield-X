import pytest
from app.services.threat_intelligence_fusion.threat_landscape_engine import ThreatLandscapeEngine

def test_threat_landscape_trends():
    engine = ThreatLandscapeEngine()
    summary = engine.get_landscape_summary()
    assert "FINANCIAL_SERVICES" in summary["sectors_monitored"]
    assert "APAC" in summary["regions_monitored"]
    assert len(summary["top_targeted_sectors"]) >= 2
