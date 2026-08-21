import pytest
from app.services.mission_control_os.mission_blocker_engine import MissionBlockerEngine

def test_blocker_engine_diagnosis():
    engine = MissionBlockerEngine()
    diag = engine.diagnose_blockers(
        task_id="task_01",
        missing_approvals=["CISO"],
        dependency_statuses={"soar_gateway": "UNAVAILABLE"},
        is_intelligence_stale=True,
    )
    assert diag["has_blockers"] is True
    assert diag["blocker_count"] == 3
    assert diag["can_auto_proceed"] is False
