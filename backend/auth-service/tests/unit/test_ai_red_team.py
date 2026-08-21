import pytest
from app.services.ai_governance.ai_red_team_engine import AIRedTeamEngine

def test_ai_red_team_execution():
    engine = AIRedTeamEngine()
    summary = engine.run_red_team_suite()
    assert summary["bypasses"] == 0
    assert summary["mitigation_rate"] == 1.00
    assert summary["overall_status"] == "ALL_RED_TEAM_ATTACKS_CONTAINED"
