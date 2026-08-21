import pytest
from app.services.mission_control_os.security_posture_engine import SecurityPostureEngine

def test_posture_trend_monitoring():
    engine = SecurityPostureEngine()
    p = engine.evaluate_posture()
    assert p.overall_trend in ["IMPROVING", "STABLE", "DEGRADING", "UNKNOWN"]
