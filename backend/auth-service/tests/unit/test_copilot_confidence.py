import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_explicit_confidence():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("Was data exfiltrated?", "t1", "user1", context={"exfiltration_evidence": None})
    assert res["confidence"] in {"HIGH_CONFIDENCE", "MEDIUM_CONFIDENCE", "LOW_CONFIDENCE", "NOT_VERIFIED"}
