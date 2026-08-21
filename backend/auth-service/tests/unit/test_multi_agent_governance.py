import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_multi_agent_governance_unanimous():
    copilot = TruthShieldSecurityCopilot()
    agents = [
        {"agent": "ForensicsAgent", "conclusion": "Malware contained"},
        {"agent": "RiskAgent", "conclusion": "Malware contained"}
    ]
    eval_res = copilot.evaluate_multi_agent_consensus(agents)
    assert eval_res["consensus_reached"] is True
    assert eval_res["status"] == "UNANIMOUS_SUPPORT"
