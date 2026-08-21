import pytest
from app.services.autonomous_defense.autonomous_soc_engine import AutonomousSOCEngine

def test_autonomous_soc_resilience_decoupled():
    engine = AutonomousSOCEngine()
    # Scorecard should execute smoothly without crashing even if individual sub-engines are empty
    card = engine.get_autonomous_defense_scorecard()
    assert card.system_health == "HEALTHY"
