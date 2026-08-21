import pytest
from app.services.mission_control_os.mission_workflow_orchestrator import MissionWorkflowOrchestrator

def test_response_orchestration_workflow_run():
    orchestrator = MissionWorkflowOrchestrator()
    wf = orchestrator.get_workflow("wf_threat_to_investigation_01")
    assert wf is not None
    assert wf.status == "RUNNING"
    assert wf.requires_four_eyes is True
