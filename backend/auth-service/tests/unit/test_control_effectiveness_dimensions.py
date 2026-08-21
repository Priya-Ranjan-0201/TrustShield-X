import pytest
from app.services.autonomous_defense.control_optimization_engine import ControlOptimizationEngine

def test_control_effectiveness_scoring():
    engine = ControlOptimizationEngine()
    waf = engine.get_control("ctrl_ingress_waf")
    assert waf.effectiveness_score >= 0.90
