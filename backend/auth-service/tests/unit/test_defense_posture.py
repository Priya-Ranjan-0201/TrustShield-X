import pytest
from app.services.adaptive_defense.defense_posture_engine import DefensePostureEngine


def test_defense_posture_transitions():
    engine = DefensePostureEngine()
    pos = engine.get_or_create_posture("tenant_a")
    assert pos.security_state == "NORMAL"
    assert pos.threat_level == "LOW"

    # Escalate to CRITICAL with 3 active incidents
    pos = engine.update_posture("tenant_a", threat_level="CRITICAL", active_incidents=3)
    assert pos.security_state == "CRITICAL"
    assert pos.threat_level == "CRITICAL"
    assert pos.posture_version == 2

    # Transition to HIGH_ALERT
    pos = engine.update_posture("tenant_a", threat_level="HIGH", active_incidents=1)
    assert pos.security_state == "HIGH_ALERT"
