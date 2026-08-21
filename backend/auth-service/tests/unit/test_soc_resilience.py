import pytest
from app.services.resilience.cyber_resilience_engine import CyberResilienceEngine

def test_soc_resilience():
    engine = CyberResilienceEngine()
    overview = engine.get_complete_resilience_overview()
    assert overview["critical_services_count"] >= 1
