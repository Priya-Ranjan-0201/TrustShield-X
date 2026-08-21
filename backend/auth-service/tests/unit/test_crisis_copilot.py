import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_crisis_copilot_mode():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("What are our response options?", "t1", "user1", mode="CRISIS_COMMANDER")
    assert res["mode"] == "CRISIS_COMMANDER"
