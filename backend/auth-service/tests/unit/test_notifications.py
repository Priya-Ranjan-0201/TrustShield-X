import pytest
from app.services.cyber_crisis_command.crisis_escalation_engine import CrisisEscalationEngine

def test_notification_registration():
    engine = CrisisEscalationEngine()
    st = engine.register_stakeholder("C-NOTIF", "t1", "SecOps Manager", "SOC_LEAD", "WEBHOOK")
    assert st["channel"] == "WEBHOOK"
