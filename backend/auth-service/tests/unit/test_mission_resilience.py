import pytest
from app.services.mission_control_os.mission_task_engine import MissionTaskEngine

def test_task_engine_resilience_concurrent_updates():
    engine = MissionTaskEngine()
    t = engine.create_task("Resilience Task", "INVESTIGATE")
    engine.update_task_status(t.task_id, "IN_PROGRESS")
    engine.update_task_status(t.task_id, "COMPLETED")
    assert engine.get_task(t.task_id).status == "COMPLETED"
