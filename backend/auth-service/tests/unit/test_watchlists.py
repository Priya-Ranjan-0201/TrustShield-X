import pytest
from app.services.global_intelligence.global_threat_intelligence_fusion_engine import GlobalThreatIntelligenceFusionEngine

def test_threat_watchlist_management():
    engine = GlobalThreatIntelligenceFusionEngine()
    w = engine.add_watchlist("INFRASTRUCTURE", "AS-64496")
    assert w["category"] == "INFRASTRUCTURE"
    assert w["target"] == "AS-64496"
    assert len(engine.list_watchlists()) >= 2
