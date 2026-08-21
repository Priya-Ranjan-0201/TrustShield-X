import pytest
import time
from app.services.autonomous_defense.autonomous_soc_engine import AutonomousSOCEngine

def test_autonomous_soc_performance():
    engine = AutonomousSOCEngine()
    start = time.perf_counter()
    card = engine.get_autonomous_defense_scorecard()
    duration_ms = (time.perf_counter() - start) * 1000.0
    assert card is not None
    assert duration_ms < 50.0
