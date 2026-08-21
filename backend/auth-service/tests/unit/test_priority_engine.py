import pytest
from app.services.fusion.security_priority_engine import SecurityPriorityEngine
from app.schemas.fusion_models import SecurityEventDTO


def test_security_priority_calculation():
    engine = SecurityPriorityEngine()
    crit_event = SecurityEventDTO(
        event_id="sev_p1",
        event_type="DETECTION",
        source="APK_PARSER",
        severity="CRITICAL",
        risk_score=95.0,
        trust_score=20.0,
        exposure_score=85.0,
        confidence=0.98,
    )

    prio = engine.calculate_priority(crit_event, asset_criticality="CRITICAL", campaign_velocity=1.8)
    assert prio["priority_score"] >= 85.0
    assert prio["priority_level"] == "P1_CRITICAL"
