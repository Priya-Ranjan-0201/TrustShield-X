import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_threat_hunt_tagging():
    copilot = TruthShieldSecurityCopilot()
    hunt = copilot.generate_hunt_hypothesis("Encoded PowerShell", "t1")
    assert hunt["status"] == "AI_GENERATED"
    assert hunt["requires_validation"] is True
