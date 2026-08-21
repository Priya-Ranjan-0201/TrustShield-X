import pytest
from app.services.global_defense.global_defense_coordination_engine import GlobalDefenseCoordinationEngine

def test_coordinated_threat_hunting_case_link():
    engine = GlobalDefenseCoordinationEngine()
    c = engine.get_case("coord_darkstorm_finance_defense")
    assert c is not None
    assert "Digital Twin Simulation Verification" in c.evidence
