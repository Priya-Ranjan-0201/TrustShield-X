import pytest
import time
from app.services.digital_twin_lab.cyber_defense_digital_twin_engine import CyberDefenseDigitalTwinEngine

def test_twin_simulation_latency():
    engine = CyberDefenseDigitalTwinEngine()
    start = time.perf_counter()
    overview = engine.get_digital_twin_overview()
    duration_ms = (time.perf_counter() - start) * 1000.0
    assert overview is not None
    assert duration_ms < 100.0
