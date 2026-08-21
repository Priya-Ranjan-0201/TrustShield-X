import pytest
import time
from app.services.mission_control_os.global_security_mission_control_engine import GlobalSecurityMissionControlEngine

def test_mission_overview_performance():
    engine = GlobalSecurityMissionControlEngine()
    start = time.perf_counter()
    ov = engine.get_mission_overview()
    latency_ms = (time.perf_counter() - start) * 1000.0
    assert ov is not None
    assert latency_ms < 50.0
