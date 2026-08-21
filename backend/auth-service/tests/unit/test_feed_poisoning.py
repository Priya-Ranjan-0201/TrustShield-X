import pytest
from app.services.global_intelligence.intelligence_source_manager import IntelligenceSourceManager

def test_feed_poisoning_quarantine():
    mgr = IntelligenceSourceManager()
    q = mgr.quarantine_malformed_feed("src_global_exchange", "Impossible timestamps & volumetric spike", {"count": 100000})
    assert q["source_id"] == "src_global_exchange"
    health = mgr.get_feed_health("src_global_exchange")
    assert health["poisoning_alerts"] == 1
