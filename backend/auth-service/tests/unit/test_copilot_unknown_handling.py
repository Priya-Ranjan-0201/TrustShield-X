import pytest
from app.services.copilot.security_copilot_service import SecurityCopilot


def test_copilot_unknown_handling_blind_spots():
    copilot = SecurityCopilot()
    res = copilot.process_chat_message("sess_3", "What are our blind spots and unknown areas?")

    assert len(res.unknown_areas) >= 1
    assert any("team owner" in u.lower() or "telemetry" in u.lower() for u in res.unknown_areas)
