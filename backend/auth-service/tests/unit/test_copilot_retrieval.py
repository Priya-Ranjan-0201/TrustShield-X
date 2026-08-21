import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_rag_sources():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("Explain active alerts", "t1", "user1")
    assert len(res["sources"]) >= 1
