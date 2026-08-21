import pytest
from app.services.resilience.cyber_resilience_engine import CyberResilienceEngine

def test_copilot_resilience():
    engine = CyberResilienceEngine()
    overview = engine.get_complete_resilience_overview()
    assert "overall_resilience_score" in overview
