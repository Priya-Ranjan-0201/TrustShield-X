import pytest
from app.services.mission_control_os.mission_workflow_orchestrator import MissionWorkflowOrchestrator

def test_workflow_versioning():
    orchestrator = MissionWorkflowOrchestrator()
    wf = orchestrator.get_workflow("wf_threat_to_investigation_01")
    assert wf.version == "1.0.0"
