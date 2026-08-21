import pytest
from app.services.mission_control_os.mission_workflow_orchestrator import MissionWorkflowOrchestrator

def test_mission_workflow_execution():
    orchestrator = MissionWorkflowOrchestrator()
    wf = orchestrator.run_workflow(
        name="CRITICAL_VULNERABILITY_RESPONSE",
        trigger_event="VULNERABILITY_DISCOVERED",
        steps=[{"step": 1, "action": "PATCH_VERIFY"}],
    )
    assert wf.name == "CRITICAL_VULNERABILITY_RESPONSE"
    assert wf.status == "RUNNING"
