import pytest
from app.services.security_engineering.autonomous_security_engineering_engine import AutonomousSecurityEngineeringEngine

def test_copilot_security_engineering():
    fabric = AutonomousSecurityEngineeringEngine()
    overview = fabric.get_engineering_overview()
    assert overview["improvement_candidates_count"] >= 1
    assert overview["autonomy_level"] == "LEVEL_3_CONTROLLED_AUTOMATION"
