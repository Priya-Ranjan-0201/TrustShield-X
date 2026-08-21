import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_sigma_rule_generation():
    copilot = TruthShieldSecurityCopilot()
    rule = copilot.generate_detection_rule("APT29 Mimikatz", "t1")
    assert rule["format"] == "SIGMA_YAML"
    assert rule["syntax_valid"] is True
    assert rule["status"] == "CANDIDATE_AWAITING_APPROVAL"
