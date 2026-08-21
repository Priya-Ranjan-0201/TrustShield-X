import pytest
from app.services.security_engineering.autonomous_security_engineering_engine import AutonomousSecurityEngineeringEngine

def test_improvement_resilience():
    engine = AutonomousSecurityEngineeringEngine()
    for _ in range(50):
        overview = engine.get_engineering_overview()
        assert overview["security_gaps_count"] >= 1
