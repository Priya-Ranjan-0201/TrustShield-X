import pytest
import time
from app.services.security_engineering.autonomous_security_engineering_engine import AutonomousSecurityEngineeringEngine

def test_improvement_performance():
    engine = AutonomousSecurityEngineeringEngine()
    start = time.perf_counter()
    overview = engine.get_engineering_overview()
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1
    assert overview["improvement_candidates_count"] >= 1
