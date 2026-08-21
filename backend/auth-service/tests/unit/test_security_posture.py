import pytest
from app.services.mission_control_os.security_posture_engine import SecurityPostureEngine

def test_security_posture_8_dimensions():
    engine = SecurityPostureEngine()
    p = engine.evaluate_posture()
    assert p.threat_posture >= 0.90
    assert p.exposure_posture >= 0.90
    assert p.control_posture >= 0.90
    assert p.incident_posture >= 0.90
    assert p.response_posture >= 0.90
    assert p.recovery_posture >= 0.90
    assert p.governance_posture >= 0.90
    assert p.resilience_posture >= 0.90
