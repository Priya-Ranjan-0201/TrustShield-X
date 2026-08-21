import pytest
from app.services.soc.case_task_engine import CaseTaskEngine


def test_incident_task_assignment():
    engine = CaseTaskEngine()
    case = engine.create_case("tenant_tsk", "Botnet Outbreak", ["inc_bot_1"])
    task = engine.add_task(case.case_id, "inc_bot_1", "Dump memory on srv_checkout", "usr_forensics_lead")

    assert task.status == "TODO"
    assert task.owner == "usr_forensics_lead"

    updated_case = engine.get_case(case.case_id)
    assert updated_case is not None
    assert len(updated_case.tasks) == 1
