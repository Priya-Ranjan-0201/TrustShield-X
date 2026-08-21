import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_executive_briefing_mode():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("What is the leadership summary?", "t1", "exec1", mode="EXECUTIVE")
    assert "Executive Briefing" in res["answer"]
    assert "Business Impact" in res["answer"]
