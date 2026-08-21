import pytest
from app.services.cyber_crisis_command.crisis_escalation_engine import CrisisEscalationEngine

def test_escalation_triggers():
    engine = CrisisEscalationEngine()
    res = engine.evaluate_escalation_triggers("C-ESC", "t1", "SEV_1", 150, 6, 2)
    assert res["escalated"] is True
    assert res["escalation_tier"] == "EXECUTIVE_CRISIS_BOARD"
