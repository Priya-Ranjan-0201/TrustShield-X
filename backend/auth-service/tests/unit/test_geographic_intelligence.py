import pytest
from app.services.threat_intelligence_fusion.threat_landscape_engine import ThreatLandscapeEngine

def test_geographic_intelligence_summary():
    engine = ThreatLandscapeEngine()
    summary = engine.get_landscape_summary()
    apac_target = next((r for r in summary["top_targeted_regions"] if r["region"] == "APAC"), None)
    assert apac_target is not None
    assert apac_target["primary_actor"] == "Ember Bear (APT-88)"
