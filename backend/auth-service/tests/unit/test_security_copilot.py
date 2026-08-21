import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_basic_query():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("What is the status of the crisis?", "t1", "user1")
    assert res["status"] == "SUCCESS"
    assert res["confidence"] == "HIGH_CONFIDENCE"
    assert len(res["sources"]) > 0
