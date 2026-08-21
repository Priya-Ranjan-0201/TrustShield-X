import pytest
import time
from app.services.global_defense.global_defense_coordination_engine import GlobalDefenseCoordinationEngine

def test_coordination_overview_latency():
    engine = GlobalDefenseCoordinationEngine()
    start = time.perf_counter()
    ov = engine.get_coordination_overview()
    latency_ms = (time.perf_counter() - start) * 1000.0
    assert ov is not None
    assert latency_ms < 50.0
