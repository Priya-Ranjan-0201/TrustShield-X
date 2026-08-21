import pytest
from app.services.global_defense.coordination_sla_engine import CoordinationSLAEngine

def test_coordination_sla_compliance_evaluation():
    engine = CoordinationSLAEngine()
    sla = engine.evaluate_sla(
        coordination_id="coord_01",
        notification_seconds=100.0,
        ack_seconds=300.0,
        response_seconds=900.0,
        recovery_seconds=1800.0,
    )
    assert sla.is_compliant is True
    assert sla.notification_sla_seconds == 100.0
