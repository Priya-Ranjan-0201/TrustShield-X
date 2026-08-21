import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_tool_modes():
    copilot = TruthShieldSecurityCopilot()
    assert "READ_ONLY" in copilot.TOOL_EXECUTION_MODES
    assert "APPROVAL_REQUIRED" in copilot.TOOL_EXECUTION_MODES
