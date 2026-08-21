import pytest
from app.services.mission_control_os.mission_sla_engine import MissionSLAEngine

def test_sla_engine_compliance():
    engine = MissionSLAEngine()
    res = engine.evaluate_task_sla("task_01", allocated_sla_seconds=1800.0, elapsed_seconds=600.0)
    assert res["is_compliant"] is True
    assert res["escalation_level"] == "NORMAL"
