import pytest
from app.services.autonomous_defense.security_decision_engine import SecurityDecisionEngine

def test_security_decision_creation():
    engine = SecurityDecisionEngine()
    dec = engine.create_decision(
        decision_type="RESPONSE_RECOMMENDATION",
        recommendation="Isolate compromised container",
        evidence=["Process injection alert"],
        confidence=0.92,
        selected_action="CONTAINER_ISOLATE",
        expected_outcome="Stop exfiltration",
    )
    assert dec.decision_id is not None
    assert dec.confidence == 0.92
    assert dec.autonomy_level == "LEVEL_4"
