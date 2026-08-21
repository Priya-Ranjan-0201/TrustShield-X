import pytest
from app.services.mission_control_os.copilot_mission_control_bridge import CopilotMissionControlBridge

def test_copilot_mission_control_evidence_grounding():
    bridge = CopilotMissionControlBridge()
    ans = bridge.answer_operational_query("What is simulated?")
    assert ans["claim_status"] == "SIMULATED"
    assert "Digital Twin" in ans["evidence"][0]
