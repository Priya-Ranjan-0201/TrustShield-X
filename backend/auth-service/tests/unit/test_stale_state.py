import pytest
from app.services.mission_control_os.mission_blocker_engine import MissionBlockerEngine

def test_stale_state_blocks_automation():
    engine = MissionBlockerEngine()
    diag = engine.diagnose_blockers("task_01", [], {}, is_intelligence_stale=True)
    assert diag["has_blockers"] is True
    assert diag["blockers"][0]["category"] == "STALE_INTELLIGENCE"
