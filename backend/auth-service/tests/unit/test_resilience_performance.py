import pytest
import time
from app.services.resilience.cyber_resilience_engine import CyberResilienceEngine

def test_resilience_performance():
    engine = CyberResilienceEngine()
    start = time.perf_counter()
    overview = engine.get_complete_resilience_overview()
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1
    assert overview["overall_resilience_score"] > 0
