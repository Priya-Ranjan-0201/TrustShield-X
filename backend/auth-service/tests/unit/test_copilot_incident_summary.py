import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_incident_summary():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("Summarize this incident", "t1", "user1")
    assert "Confirmed" in res["answer"]
    assert "Suspected" in res["answer"]
