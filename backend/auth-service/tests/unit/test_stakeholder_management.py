import pytest
from app.services.cyber_crisis_command.crisis_escalation_engine import CrisisEscalationEngine

def test_stakeholder_registration():
    engine = CrisisEscalationEngine()
    st = engine.register_stakeholder("C-STK", "t1", "Jane Doe", "CISO", "EMAIL")
    assert st["name"] == "Jane Doe"
    assert st["notification_status"] == "REGISTERED"
