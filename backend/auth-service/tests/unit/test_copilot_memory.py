import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_memory_isolation():
    copilot = TruthShieldSecurityCopilot()
    copilot.query_copilot("Query 1", "tenant-A", "u1")
    copilot.query_copilot("Query 2", "tenant-B", "u2")
    audit_a = copilot.get_query_audit_trail("tenant-A")
    assert all(e["tenant_id"] == "tenant-A" for e in audit_a)
