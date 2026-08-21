import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_abac_context_evaluation():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("What is the risk?", "t1", "u1", context={"abac_policy": "STRICT_ALLOW"})
    assert res["status"] == "SUCCESS"
