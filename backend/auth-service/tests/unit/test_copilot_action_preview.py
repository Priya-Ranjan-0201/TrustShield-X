import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_action_preview_recommendation():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("Recommend containment action", "t1", "user1")
    assert "Recommended Action" in res["answer"]
