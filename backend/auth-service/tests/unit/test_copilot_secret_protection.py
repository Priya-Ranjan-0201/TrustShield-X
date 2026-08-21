import pytest
from app.services.copilot.copilot_prompt_guard import CopilotPromptGuard


def test_copilot_secret_masking():
    guard = CopilotPromptGuard()
    raw = "User token is Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    sanitized = guard.filter_secret_leakage(raw)

    assert "REDACTED_SECRET_TOKEN" in sanitized
    assert "eyJhbGci" not in sanitized
