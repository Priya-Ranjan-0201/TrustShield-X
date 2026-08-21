import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_rbac_modes():
    copilot = TruthShieldSecurityCopilot()
    assert "COMPLIANCE_ANALYST" in copilot.COPILOT_MODES
    assert "SECURITY_ENGINEER" in copilot.COPILOT_MODES
