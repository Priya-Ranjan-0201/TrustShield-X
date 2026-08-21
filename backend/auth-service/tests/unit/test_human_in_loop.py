import pytest
from app.services.mission_control_os.mission_task_engine import MissionTaskEngine

def test_human_in_the_loop_task_ownership():
    engine = MissionTaskEngine()
    tasks = engine.list_tasks()
    assert len(tasks) >= 1
    assert tasks[0].owner == "SOC_ANALYST_LEAD"
