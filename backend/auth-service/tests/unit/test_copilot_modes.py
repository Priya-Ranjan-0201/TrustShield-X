import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_copilot_9_modes():
    copilot = TruthShieldSecurityCopilot()
    modes = [
        "SOC_ANALYST", "INCIDENT_RESPONDER", "THREAT_HUNTER", "FORENSICS_ANALYST",
        "SECURITY_ENGINEER", "RISK_ANALYST", "COMPLIANCE_ANALYST", "EXECUTIVE", "CRISIS_COMMANDER"
    ]
    for m in modes:
        res = copilot.query_copilot("Status report", "t1", "user1", mode=m)
        assert res["mode"] == m
