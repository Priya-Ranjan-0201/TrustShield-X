import pytest
from app.services.cyber_crisis_command.truthshield_security_copilot import TruthShieldSecurityCopilot

def test_multi_agent_disagreement_exposed():
    copilot = TruthShieldSecurityCopilot()
    agents = [
        {"agent": "AgentA", "conclusion": "Active Attack"},
        {"agent": "AgentB", "conclusion": "False Positive"}
    ]
    eval_res = copilot.evaluate_multi_agent_consensus(agents)
    assert eval_res["consensus_reached"] is False
    assert eval_res["status"] == "AGENT_DISAGREEMENT_EXPOSED"
    assert eval_res["requires_human_review"] is True
