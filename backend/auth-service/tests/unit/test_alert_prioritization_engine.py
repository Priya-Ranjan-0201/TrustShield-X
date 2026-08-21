import pytest
from app.services.mission_control_os.mission_priority_engine import MissionPriorityEngine

def test_alert_prioritization_multi_factor():
    engine = MissionPriorityEngine()
    res = engine.evaluate_priority(severity_score=0.90, exposure_score=0.85, has_active_exploitation=True)
    assert res["priority"] == "CRITICAL"
