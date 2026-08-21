import pytest
from app.services.resilience.cyber_resilience_engine import CyberResilienceEngine

def test_resilience_assessment():
    engine = CyberResilienceEngine()
    overview = engine.get_complete_resilience_overview()
    assert overview["critical_assets_count"] >= 3
    assert overview["critical_services_count"] >= 1
    assert overview["overall_resilience_score"] > 80.0
