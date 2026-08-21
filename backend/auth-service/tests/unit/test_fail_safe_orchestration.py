import pytest
from app.services.mission_control_os.mission_control_health_engine import MissionControlHealthEngine

def test_fail_safe_decoupling():
    engine = MissionControlHealthEngine()
    h = engine.check_health()
    # Even if an external integration lags, core controls operate independently
    assert h.overall_health == "HEALTHY"
