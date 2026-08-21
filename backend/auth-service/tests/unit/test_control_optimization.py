import pytest
from app.services.autonomous_defense.control_optimization_engine import ControlOptimizationEngine

def test_control_optimization_inspection():
    engine = ControlOptimizationEngine()
    ctrls = engine.list_controls()
    assert len(ctrls) >= 2
    domains = [c.control_domain for c in ctrls]
    assert "PREVENTION" in domains
    assert "DETECTION" in domains
