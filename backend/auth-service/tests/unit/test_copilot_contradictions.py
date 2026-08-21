import pytest
from app.services.copilot.security_copilot_service import SecurityCopilot


def test_copilot_contradictions_display():
    copilot = SecurityCopilot()
    res = copilot.process_chat_message("sess_2", "Analyze CVE-2026-9942 and container logs")

    assert len(res.contradictions) >= 1
    assert "ev_audit_log_90" in res.contradictions[0]
