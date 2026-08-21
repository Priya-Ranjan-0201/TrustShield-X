import pytest
from app.services.mission_control_os.mission_task_engine import MissionTaskEngine

def test_mission_task_creation_and_update():
    engine = MissionTaskEngine()
    task = engine.create_task(
        title="Verify Patch on API Gateway",
        task_type="VALIDATE",
        owner="SECOPS_ENGINEER",
        priority="HIGH",
        sla_seconds=3600.0,
    )
    assert task.title == "Verify Patch on API Gateway"
    
    updated = engine.update_task_status(task.task_id, "IN_PROGRESS")
    assert updated.status == "IN_PROGRESS"
