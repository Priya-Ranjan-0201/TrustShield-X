import pytest
from app.services.autonomous_defense.autonomous_soc_engine import AutonomousSOCEngine

def test_autonomous_soc_scorecard():
    engine = AutonomousSOCEngine()
    card = engine.get_autonomous_defense_scorecard("default_tenant")
    assert card.autonomy_level == "LEVEL_4"
    assert card.detection_quality_score >= 0.90
    assert card.system_health == "HEALTHY"
