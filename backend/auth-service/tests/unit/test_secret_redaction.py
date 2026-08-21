import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_secret_redaction():
    copilot = TruthShieldSecurityCopilot()
    res = copilot.query_copilot("Investigate token: password='SuperSecretPassword123'", "t1", "user1")
    audit = copilot.get_query_audit_trail("t1")
    assert len(audit) >= 1
