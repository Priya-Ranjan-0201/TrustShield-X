import pytest
from app.services.resilience.cyber_resilience_engine import CyberResilienceEngine

def test_resilience_load():
    engine = CyberResilienceEngine()
    for _ in range(50):
        overview = engine.get_complete_resilience_overview()
        assert overview["critical_assets_count"] >= 3
