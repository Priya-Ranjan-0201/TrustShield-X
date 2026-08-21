import pytest
from app.services.mission_control_os.mission_task_engine import MissionTaskEngine

def test_task_dependencies_enforcement():
    engine = MissionTaskEngine()
    t1 = engine.create_task("Step 1", "INVESTIGATE")
    t2 = engine.create_task("Step 2", "CONTAIN", dependencies=[t1.task_id])
    assert t2.status == "BLOCKED"
    
    # Cannot transition t2 to IN_PROGRESS while t1 is not COMPLETED
    with pytest.raises(ValueError, match="prerequisite dependencies"):
        engine.update_task_status(t2.task_id, "IN_PROGRESS")
        
    # Complete t1
    engine.update_task_status(t1.task_id, "COMPLETED")
    
    # Now t2 can proceed
    updated_t2 = engine.update_task_status(t2.task_id, "IN_PROGRESS")
    assert updated_t2.status == "IN_PROGRESS"
