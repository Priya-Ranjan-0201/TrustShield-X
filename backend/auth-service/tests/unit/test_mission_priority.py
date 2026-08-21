import pytest
from app.services.mission_control_os.mission_priority_engine import MissionPriorityEngine

def test_mission_priority_calculation():
    engine = MissionPriorityEngine()
    res = engine.evaluate_priority(
        severity_score=0.90,
        exposure_score=0.85,
        has_active_exploitation=True,
        has_failing_controls=True,
    )
    assert res["composite_score"] >= 0.85
    assert res["priority"] == "CRITICAL"
    assert res["requires_immediate_action"] is True
