import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_source_citation_format():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("Where was the probe detected?", "t1", "user1")
    src = res["sources"][0]
    assert "source" in src or isinstance(src, str)
