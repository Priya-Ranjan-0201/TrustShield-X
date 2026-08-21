import pytest
from app.services.mission_control_os.copilot_mission_control_bridge import CopilotMissionControlBridge

def test_knowledge_integration_in_copilot():
    bridge = CopilotMissionControlBridge()
    ans = bridge.answer_operational_query("What is happening right now?")
    assert len(ans["evidence"]) >= 1
    assert ans["claim_status"] == "OBSERVED"
