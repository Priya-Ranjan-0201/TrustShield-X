import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_forensics_mode():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("Analyze memory dump", "t1", "user1", mode="FORENSICS_ANALYST")
    assert res["mode"] == "FORENSICS_ANALYST"
