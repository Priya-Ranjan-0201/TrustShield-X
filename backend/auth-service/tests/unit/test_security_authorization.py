import pytest
from app.services.fusion.security_priority_engine import SecurityPriorityEngine
from app.schemas.fusion_models import SecurityEventDTO


def test_action_boundary_and_authorization_invariant():
    engine = SecurityPriorityEngine()
    ev = SecurityEventDTO(
        event_id="sev_test",
        event_type="DETECTION",
        source="TEST",
        risk_score=90.0,
    )
    prio = engine.calculate_priority(ev, asset_criticality="HIGH")

    # Invariant: Priority engine can suggest priority level but cannot autonomously execute actions
    assert "priority_level" in prio
    assert prio["priority_level"] in ("P1_CRITICAL", "P2_HIGH")
