import pytest
from app.services.global_defense.global_defense_coordination_engine import GlobalDefenseCoordinationEngine

def test_global_early_warning_overview():
    engine = GlobalDefenseCoordinationEngine()
    ov = engine.get_coordination_overview()
    assert ov["active_coordination_cases_count"] >= 1
    assert ov["collective_defense_score"] == 0.94
