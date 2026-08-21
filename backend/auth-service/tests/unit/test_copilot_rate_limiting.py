import pytest
from app.services.copilot.security_copilot_service import SecurityCopilot


def test_copilot_rapid_successive_queries():
    copilot = SecurityCopilot()
    for _ in range(10):
        res = copilot.process_chat_message("sess_rate", "Status check")
        assert res.answer != ""
