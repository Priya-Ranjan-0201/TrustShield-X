import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_refuses_to_hallucinate_root_cause():
    copilot = TruthShieldSecurityCopilot()
    # Invariant: Never invent root cause when evidence is missing
    res = copilot.query_copilot("What was the root cause of this breach?", "t1", "user1", context={"root_cause": None})
    assert res["status"] == "ROOT_CAUSE_NOT_ESTABLISHED"
    assert res["confidence"] == "NOT_VERIFIED"
